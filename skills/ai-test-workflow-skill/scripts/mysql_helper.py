#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL 时间追踪数据操作工具
提供连接管理、插入记录、查询全量数据等功能。
被 record_time_saved.py 和 generate_time_analytics.py 共用。
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta

try:
    import pymysql
    import pymysql.cursors
except ImportError:
    print("ERROR: pymysql 未安装。请运行: pip install pymysql", file=sys.stderr)
    sys.exit(1)


def load_mysql_config(config_path):
    """从 time_tracking_config.yaml 读取 MySQL 连接配置"""
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML 未安装。请运行: pip install pyyaml", file=sys.stderr)
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    mysql_cfg = config.get("mysql", {})
    if not mysql_cfg.get("host"):
        raise ValueError("MySQL 配置缺失：.time_tracking_config.yaml 中 mysql.host 未设置")

    return {
        "host": mysql_cfg.get("host", "127.0.0.1"),
        "port": mysql_cfg.get("port", 3306),
        "user": mysql_cfg.get("user", "root"),
        "password": mysql_cfg.get("password", ""),
        "database": mysql_cfg.get("database", "testing_metrics"),
        "table": mysql_cfg.get("table", "agent_time_tracking"),
        "charset": mysql_cfg.get("charset", "utf8mb4"),
    }


def get_connection(config_path):
    """获取 MySQL 连接"""
    cfg = load_mysql_config(config_path)
    return pymysql.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        charset=cfg["charset"],
        cursorclass=pymysql.cursors.DictCursor,
    )


def insert_record(config_path, record):
    """插入一条时间追踪记录到 MySQL

    Args:
        config_path: time_tracking_config.yaml 路径
        record: dict，包含以下字段：
            - timestamp: ISO 格式时间戳
            - date: YYYY-MM-DD
            - biz_line: 业务线
            - employee: 员工姓名
            - user_story: 用户故事
            - step: 步骤名称
            - step_code: 步骤编码
            - time_saved_hours: 节省小时数
            - time_saved_pd: 节省人天数
            - total_hours: 折算总小时
            - remark: 备注（可选）

    Returns:
        dict: {"success": bool, "message": str, "record_id": int}
    """
    try:
        conn = get_connection(config_path)
        cursor = conn.cursor()

        sql = """
            INSERT INTO agent_time_tracking
                (timestamp, date, biz_line, biz_line_code, employee, user_story,
                 step, step_code, time_saved_hours, time_saved_pd,
                 total_hours, remark)
            VALUES (%(timestamp)s, %(date)s, %(biz_line)s, %(biz_line_code)s,
                    %(employee)s, %(user_story)s, %(step)s, %(step_code)s,
                    %(time_saved_hours)s, %(time_saved_pd)s,
                    %(total_hours)s, %(remark)s)
        """

        params = {
            "timestamp": record.get("timestamp", datetime.now().astimezone().isoformat()),
            "date": record.get("date", datetime.now().strftime("%Y-%m-%d")),
            "biz_line": record.get("biz_line", "效贷"),
            "biz_line_code": record.get("biz_line_code", "XD"),
            "employee": record.get("employee", ""),
            "user_story": record.get("user_story", ""),
            "step": record.get("step", ""),
            "step_code": record.get("step_code", ""),
            "time_saved_hours": float(record.get("time_saved_hours", 0)),
            "time_saved_pd": float(record.get("time_saved_pd", 0)),
            "total_hours": float(record.get("total_hours", 0)),
            "remark": record.get("remark", ""),
        }

        cursor.execute(sql, params)
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()

        return {"success": True, "message": "MySQL 写入成功", "record_id": record_id}

    except pymysql.Error as e:
        return {"success": False, "message": f"MySQL 写入失败: {e}", "record_id": -1}
    except Exception as e:
        return {"success": False, "message": f"未知错误: {e}", "record_id": -1}


def fetch_all_records(config_path, biz_line=None, employee=None):
    """查询时间追踪记录

    Args:
        config_path: time_tracking_config.yaml 路径
        biz_line: 业务线过滤（可选）
        employee: 员工姓名过滤（可选）

    Returns:
        list[dict]: 记录列表
    """
    try:
        conn = get_connection(config_path)
        cursor = conn.cursor()

        sql = "SELECT * FROM agent_time_tracking WHERE 1=1"
        params = {}

        if biz_line:
            sql += " AND biz_line = %(biz_line)s"
            params["biz_line"] = biz_line

        if employee:
            sql += " AND employee = %(employee)s"
            params["employee"] = employee

        sql += " ORDER BY timestamp ASC"

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()

        # 转换 Decimal/Datetime 为 JSON 可序列化格式
        records = []
        for row in rows:
            record = {}
            for key, value in row.items():
                if hasattr(value, "isoformat"):
                    record[key] = value.isoformat()
                elif hasattr(value, "as_tuple"):
                    record[key] = float(value)
                else:
                    record[key] = value
            records.append(record)

        return records

    except pymysql.Error as e:
        print(f"ERROR: MySQL 查询失败: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"ERROR: 未知错误: {e}", file=sys.stderr)
        return []


def init_table(config_path):
    """初始化数据库表（如果不存在则创建）

    Args:
        config_path: time_tracking_config.yaml 路径

    Returns:
        dict: {"success": bool, "message": str}
    """
    sql_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "init_mysql.sql")
    try:
        with open(sql_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        conn = get_connection(config_path)
        cursor = conn.cursor()

        # 执行建表 SQL（支持多语句）
        for statement in sql_script.split(";"):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

        conn.commit()
        conn.close()

        return {"success": True, "message": "MySQL 表初始化成功"}
    except Exception as e:
        return {"success": False, "message": f"MySQL 表初始化失败: {e}"}


def test_connection(config_path):
    """测试 MySQL 连接是否正常

    Args:
        config_path: time_tracking_config.yaml 路径

    Returns:
        dict: {"success": bool, "message": str}
    """
    try:
        conn = get_connection(config_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()

        if result:
            return {"success": True, "message": "MySQL 连接正常"}
        else:
            return {"success": False, "message": "MySQL 连接异常：无响应"}
    except Exception as e:
        return {"success": False, "message": f"MySQL 连接失败: {e}"}
