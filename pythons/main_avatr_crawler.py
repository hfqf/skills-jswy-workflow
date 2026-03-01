#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿维塔线索抓取完整执行脚本
按照《阿维塔线索抓取完整操作指南》实现
"""

import requests
import sqlite3
import json
import os
from datetime import datetime

# 注意：实际使用时需要从浏览器获取最新的token
# 这里只是一个示例token，需要替换为实际有效的token
TOKEN = "YOUR_ACTUAL_TOKEN_HERE"

def get_auth_headers(token):
    """获取认证headers"""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'login-token': token
    }

def create_database():
    """创建SQLite数据库和表"""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    db_path = os.path.join(desktop_path, 'clues.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建线索表（16个核心字段）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clues (
        id TEXT PRIMARY KEY,
        clueNo TEXT,
        phone TEXT,
        nickName TEXT,
        clueStatusName TEXT,
        createTime TEXT,
        assignUser TEXT,
        shopName TEXT,
        purchaseIntentionText TEXT,
        testDriveFlag TEXT,
        sourceFirstChannelText TEXT,
        sourceSecondChannelText TEXT,
        sourceThirdChannelText TEXT,
        remarkLatest TEXT,
        lastTouchTime TEXT,
        nextTouchTime TEXT
    );
    """)
    
    # 创建跟进记录表（10个核心字段）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS follow_records (
        id INTEGER PRIMARY KEY,
        clueNo TEXT,
        planTime TEXT,
        remark TEXT,
        touchSonStatusName TEXT,
        saleUser TEXT,
        shopName TEXT,
        touchTypeText TEXT,
        touchPurposeText TEXT,
        touchResultText TEXT,
        UNIQUE(clueNo, planTime)
    );
    """)
    
    conn.commit()
    conn.close()
    return db_path

def get_current_date_range():
    """获取当前日期范围"""
    today = datetime.now().strftime("%Y-%m-%d")
    start_time = f"{today} 00:00:00"
    end_time = f"{today} 23:59:59"
    return start_time, end_time

def save_clues_to_db(clues, db_path):
    """保存线索数据到数据库（去重处理）"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for clue in clues:
        cursor.execute("""
            INSERT OR REPLACE INTO clues VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            clue.get("id"),
            clue.get("clueNo"),
            clue.get("phone"),
            clue.get("nickName"),
            clue.get("clueStatusName"),
            clue.get("createTime"),
            clue.get("assignUser"),
            clue.get("shopName"),
            clue.get("purchaseIntentionText"),
            clue.get("testDriveFlag"),
            clue.get("sourceFirstChannelText"),
            clue.get("sourceSecondChannelText"),
            clue.get("sourceThirdChannelText"),
            clue.get("remarkLatest"),
            clue.get("lastTouchTime"),
            clue.get("nextTouchTime")
        ))
    
    conn.commit()
    conn.close()

def extract_clues_data(token, db_path):
    """抓取全量线索数据"""
    headers = get_auth_headers(token)
    start_time, end_time = get_current_date_range()
    
    page_no = 1
    page_size = 10
    total_processed = 0
    
    while True:
        payload = {
            "sortType": "createTimeDesc",
            "pageNo": page_no,
            "pageSize": page_size,
            "searchType": 10,
            "current": page_no,
            "startTime": start_time,
            "endTime": end_time,
            "isTouchNone": 0
        }
        
        try:
            response = requests.post(
                "https://admin.avatr.com/crm/v2/clue/search/pageEsClue",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    result = data.get("result", {})
                    clues = result.get("result", [])
                    actual_count = len(clues)
                    
                    print(f"Page {page_no}, got {actual_count} records")
                    
                    if clues:
                        save_clues_to_db(clues, db_path)
                        total_processed += actual_count
                    
                    # 关键：基于实际数据长度判断是否继续
                    if actual_count < page_size:
                        print(f"Clue extraction completed! Total processed: {total_processed}")
                        break
                    else:
                        page_no += 1
                else:
                    print(f"API error: {data.get('message', 'Unknown error')}")
                    break
            else:
                print(f"HTTP error: {response.status_code}")
                break
        except Exception as e:
            print(f"Request failed: {str(e)}")
            break
    
    return total_processed

def get_all_clue_nos(db_path):
    """从数据库获取所有clueNo"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT clueNo FROM clues")
    clue_nos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return clue_nos

def save_follow_records_to_db(records, db_path):
    """保存跟进记录到数据库（去重处理）"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for record in records:
        cursor.execute("""
            INSERT OR REPLACE INTO follow_records 
            (id, clueNo, planTime, remark, touchSonStatusName, saleUser, shopName, touchTypeText, touchPurposeText, touchResultText)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.get("id"),
            record.get("clueNo"),
            record.get("planTime"),
            record.get("remark"),
            record.get("touchSonStatusName"),
            record.get("saleUser"),
            record.get("shopName"),
            record.get("touchTypeText"),
            record.get("touchPurposeText"),
            record.get("touchResultText")
        ))
    
    conn.commit()
    conn.close()

def extract_follow_up_records(clue_nos, token, db_path):
    """提取所有线索的跟进记录"""
    headers = get_auth_headers(token)
    total_records = 0
    
    for i, clue_no in enumerate(clue_nos):
        print(f"Processing clue {i+1}/{len(clue_nos)}: {clue_no}")
        
        # 使用简单的参数，只包含clueNo
        payload = {
            "clueNo": clue_no
        }
        
        try:
            response = requests.post(
                "https://admin.avatr.com/crm/v2/clue/pageClueTouchPlan",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("code") == 0:
                    result = data.get("result", {})
                    records = result.get("result", [])
                    if records:
                        save_follow_records_to_db(records, db_path)
                        total_records += len(records)
                        print(f"  Got {len(records)} follow-up records")
                    else:
                        print(f"  No follow-up records found")
                else:
                    print(f"  API error: {data.get('message', 'Unknown error')}")
            else:
                print(f"  HTTP error: {response.status_code}")
                
        except Exception as e:
            print(f"  Error processing clue {clue_no}: {str(e)}")
    
    return total_records

def main():
    """主执行函数"""
    print("Starting Avatr clue extraction...")
    
    # 检查token是否已设置
    if TOKEN == "YOUR_ACTUAL_TOKEN_HERE":
        print("Error: Please replace TOKEN with your actual token from browser cookies")
        print("   Get token by executing: document.cookie in browser console")
        return
    
    # 步骤1: 创建数据库
    db_path = create_database()
    print(f"Database created: {db_path}")
    
    # 步骤2: 抓取线索数据
    print("🔍 Fetching clue data...")
    total_clues = extract_clues_data(TOKEN, db_path)
    
    if total_clues == 0:
        print("No clue data retrieved")
        return
    
    print(f"Successfully extracted {total_clues} clues!")
    
    # 步骤3: 获取所有clueNo
    clue_nos = get_all_clue_nos(db_path)
    print(f"📋 Found {len(clue_nos)} clues to process for follow-up records")
    
    # 步骤4: 抓取跟进记录
    print("Fetching follow-up records...")
    total_records = extract_follow_up_records(clue_nos, TOKEN, db_path)
    
    print(f"Follow-up records extraction completed!")
    print(f"Total records: {total_records}")
    print(f"Database location: {db_path}")
    print("Complete extraction finished!")

if __name__ == "__main__":
    main()