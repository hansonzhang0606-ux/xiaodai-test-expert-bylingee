#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
花名册身份验证脚本

从 MySQL agent_team_roster 表查询测试人员身份，支持盲输入+精确匹配。
替代 config/team_roster.yaml 文件读取方式，解决 web 端测试环境找不到配置文件的问题。

用法：
    python verify_team_member.py --name "张三"
    python verify_team_member.py --name "张三" --biz-line "效贷"

输出（JSON）：
    匹配成功: {"verified": true, "name": "张三", "biz_line": "效贷", "role": "功能测试"}
    匹配失败: {"verified": false, "name": "张三", "message": "不在花名册中"}
    连接错误: {"verified": false, "error": "MySQL连接失败: ...", "message": "花名册读取失败"}
"""

import argparse
import json
import os
import sys

# 尝试导入 mysql_helper（同一目录下）
try:
    from mysql_helper import load_mysql_config, get_connection
except ImportError:
    # 如果直接运行，尝试从同目录加载
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    try:
        from mysql_helper import load_mysql_config, get_connection
    except ImportError:
        print(json.dumps({
            "verified": False,
            "error": "mysql_helper 模块未找到",
            "message": "花名册读取失败，无法完成身份验证。"
        }, ensure_ascii=False))
        sys.exit(1)


def verify_member(name, biz_line="效贷", config_path=None):
    """
    查询 MySQL agent_team_roster 表验证身份

    Args:
        name: 待验证的姓名（已去除首尾空格）
        biz_line: 业务线名称
        config_path: time_tracking_config.yaml 路径

    Returns:
        dict: 验证结果
    """
    if config_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "..", "config", "time_tracking_config.yaml")

    try:
        conn = get_connection(config_path)
    except Exception as e:
        return {
            "verified": False,
            "error": f"MySQL连接失败: {e}",
            "message": "花名册读取失败，无法完成身份验证。"
        }

    try:
        with conn.cursor() as cursor:
            sql = (
                "SELECT name, biz_line, role, employee_id "
                "FROM agent_team_roster "
                "WHERE biz_line = %s AND name = %s AND active = 1"
            )
            cursor.execute(sql, (biz_line, name))
            row = cursor.fetchone()

            if row:
                return {
                    "verified": True,
                    "name": row["name"],
                    "biz_line": row["biz_line"],
                    "role": row["role"]
                }
            else:
                return {
                    "verified": False,
                    "name": name,
                    "message": f'"{name}"不在{biz_line}测试团队花名册中，你无法使用本专家。'
                }
    except Exception as e:
        # 检查是否是表不存在
        error_msg = str(e)
        if "Table" in error_msg and "doesn't exist" in error_msg:
            return {
                "verified": False,
                "error": "agent_team_roster 表不存在，请先执行 scripts/init_mysql.sql",
                "message": "花名册读取失败，无法完成身份验证。"
            }
        return {
            "verified": False,
            "error": f"查询失败: {e}",
            "message": "花名册读取失败，无法完成身份验证。"
        }
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="花名册身份验证")
    parser.add_argument("--name", required=True, help="待验证的姓名")
    parser.add_argument("--biz-line", default="效贷", help="业务线名称（默认: 效贷）")
    parser.add_argument("--config", default=None, help="time_tracking_config.yaml 路径")
    args = parser.parse_args()

    name = args.name.strip()
    result = verify_member(name, args.biz_line, args.config)
    print(json.dumps(result, ensure_ascii=False))

    if result.get("verified"):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
