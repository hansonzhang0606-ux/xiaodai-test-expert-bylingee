#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
腾讯文档智能表格 API 直调模块
通过 HTTP API 直接读写智能表格，不依赖 MCP 连接器。

用法:
    from tencent_docs_api import add_record, fetch_all_records, test_connection
    
    # 写入一条记录
    add_record(config_path, record_dict)
    
    # 读取全部记录
    records = fetch_all_records(config_path)
    
    # 测试连接
    result = test_connection(config_path)

配置（.time_tracking_config.yaml）:
    storage_mode: "tencent"
    tencent_docs:
      access_token: "你的access_token"
      doc_id: "智能表格文档ID"
      sheet_id: "工作表ID"
      base_url: "https://docs.qq.com/openapi"  # API地址，可调整
      field_mapping:
        - json_key: "employee"
          field: "员工姓名"
          value_type: "text_value"
        - json_key: "time_saved_hours"
          field: "节省小时数"
          value_type: "number_value"
        ...
"""

import json
import os
import sys
from datetime import datetime

try:
    import requests
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False
    print("ERROR: requests 未安装。请运行: pip install requests", file=sys.stderr)


def load_config(config_path):
    """从配置文件读取腾讯文档配置"""
    try:
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        return config.get("tencent_docs", {})
    except Exception as e:
        print(f"ERROR: 读取配置失败: {e}", file=sys.stderr)
        return {}


def _get_headers(config):
    """构建请求头"""
    token = config.get("access_token", "")
    if not token:
        raise ValueError("腾讯文档 access_token 未配置")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _get_urls(config):
    """构建 API URL"""
    base_url = config.get("base_url", "https://docs.qq.com/openapi")
    doc_id = config.get("doc_id", "")
    sheet_id = config.get("sheet_id", "")
    if not doc_id or not sheet_id:
        raise ValueError("腾讯文档 doc_id 或 sheet_id 未配置")
    
    # RESTful 风格 URL（可根据实际 API 文档调整）
    records_url = f"{base_url}/v1/smartdata/{doc_id}/sheets/{sheet_id}/records"
    return records_url


def _build_field_values(record, config):
    """将记录字典转为腾讯文档 field_values 格式"""
    field_mapping = config.get("field_mapping", [])
    field_values = []
    
    for mapping in field_mapping:
        json_key = mapping.get("json_key", "")
        field_name = mapping.get("field", "")
        value_type = mapping.get("value_type", "text_value")
        optional = mapping.get("optional", False)
        
        if not json_key or not field_name:
            continue
        
        value = record.get(json_key, "")
        if value == "" and optional:
            continue
        
        if value_type == "number_value":
            try:
                num_value = float(value) if value != "" else 0.0
            except (ValueError, TypeError):
                num_value = 0.0
            field_values.append({
                "field": field_name,
                "number_value": num_value
            })
        else:
            # text_value 格式
            field_values.append({
                "field": field_name,
                "text_value": {
                    "items": [{"text": str(value), "type": "text"}]
                }
            })
    
    return field_values


def _parse_field_values(field_values, config):
    """将腾讯文档 field_values 格式转回记录字典"""
    field_mapping = config.get("field_mapping", [])
    # 反向映射: field_name -> json_key
    field_to_key = {m.get("field", ""): m.get("json_key", "") for m in field_mapping}
    
    record = {}
    for fv in field_values:
        field_name = fv.get("field", "")
        json_key = field_to_key.get(field_name, field_name)
        
        if "text_value" in fv:
            items = fv.get("text_value", {}).get("items", [])
            if items:
                record[json_key] = items[0].get("text", "")
            else:
                record[json_key] = ""
        elif "number_value" in fv:
            record[json_key] = float(fv.get("number_value", 0))
        else:
            record[json_key] = str(fv.get("value", ""))
    
    return record


def add_record(config_path, record):
    """向智能表格追加一条记录
    
    Args:
        config_path: 配置文件路径
        record: 记录字典
        
    Returns:
        dict: {"success": bool, "message": str}
    """
    if not _HAS_REQUESTS:
        return {"success": False, "message": "requests 库未安装"}
    
    try:
        config = load_config(config_path)
        headers = _get_headers(config)
        url = _get_urls(config)
        field_values = _build_field_values(record, config)
        
        body = {
            "records": [{"field_values": field_values}]
        }
        
        resp = requests.post(url, headers=headers, json=body, timeout=15)
        
        if resp.status_code in (200, 201):
            return {"success": True, "message": "腾讯文档写入成功"}
        else:
            error_msg = f"HTTP {resp.status_code}"
            try:
                error_data = resp.json()
                error_msg += f": {error_data.get('message', resp.text[:200])}"
            except:
                error_msg += f": {resp.text[:200]}"
            return {"success": False, "message": f"腾讯文档写入失败: {error_msg}"}
            
    except requests.Timeout:
        return {"success": False, "message": "腾讯文档 API 超时"}
    except requests.ConnectionError as e:
        return {"success": False, "message": f"腾讯文档连接失败: {e}"}
    except Exception as e:
        return {"success": False, "message": f"腾讯文档写入异常: {e}"}


def fetch_all_records(config_path):
    """从智能表格读取全部记录
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        list[dict]: 记录列表
    """
    if not _HAS_REQUESTS:
        print("ERROR: requests 库未安装", file=sys.stderr)
        return []
    
    try:
        config = load_config(config_path)
        headers = _get_headers(config)
        url = _get_urls(config)
        
        all_records = []
        offset = 0
        limit = 500  # 每页500条
        
        while True:
            params = {"offset": offset, "limit": limit}
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            
            if resp.status_code != 200:
                print(f"ERROR: 腾讯文档读取失败 HTTP {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
                return []
            
            data = resp.json()
            raw_records = data.get("records", data.get("data", {}).get("records", []))
            
            if not raw_records:
                break
            
            for raw in raw_records:
                field_values = raw.get("field_values", [])
                record = _parse_field_values(field_values, config)
                record["record_id"] = raw.get("record_id", "")
                all_records.append(record)
            
            # 检查是否还有更多
            total = data.get("total", len(all_records))
            if offset + limit >= total:
                break
            offset += limit
        
        return all_records
        
    except Exception as e:
        print(f"ERROR: 腾讯文档读取异常: {e}", file=sys.stderr)
        return []


def test_connection(config_path):
    """测试腾讯文档 API 连接
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        dict: {"success": bool, "message": str}
    """
    if not _HAS_REQUESTS:
        return {"success": False, "message": "requests 库未安装"}
    
    try:
        config = load_config(config_path)
        
        # 检查必要配置
        token = config.get("access_token", "")
        doc_id = config.get("doc_id", "")
        sheet_id = config.get("sheet_id", "")
        
        if not token:
            return {"success": False, "message": "access_token 未配置"}
        if not doc_id:
            return {"success": False, "message": "doc_id 未配置"}
        if not sheet_id:
            return {"success": False, "message": "sheet_id 未配置"}
        
        # 尝试读取1条记录测试连接
        headers = _get_headers(config)
        url = _get_urls(config)
        params = {"offset": 0, "limit": 1}
        
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            total = data.get("total", 0)
            return {"success": True, "message": f"腾讯文档连接正常，当前共 {total} 条记录"}
        elif resp.status_code == 401:
            return {"success": False, "message": "access_token 无效或已过期"}
        elif resp.status_code == 404:
            return {"success": False, "message": "doc_id 或 sheet_id 不正确"}
        else:
            return {"success": False, "message": f"HTTP {resp.status_code}: {resp.text[:200]}"}
            
    except requests.Timeout:
        return {"success": False, "message": "腾讯文档 API 超时"}
    except requests.ConnectionError:
        return {"success": False, "message": "网络连接失败"}
    except Exception as e:
        return {"success": False, "message": f"连接异常: {e}"}
