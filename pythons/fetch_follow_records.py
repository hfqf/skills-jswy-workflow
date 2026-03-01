import requests
import sqlite3
import json
import os
from datetime import datetime

# Token from browser cookies
token = "eyJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50SWQiOiI3MDQ2ODk3NjJAcXEuY29tIiwic3ViIjoiYm9zcyIsInNvdXJjZSI6InRoaXJkX2xvZ2luX3NvdXJjZV8wIiwiZXhwIjoxNzc0OTU2MTMzfQ.-RI90BTfq1AOGNt2GnUH04bFWxZ5PpuS4yY9Bn_nhVI"

def get_auth_headers(token):
    """获取认证headers"""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'login-token': token
    }

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
    print("Starting follow-up records extraction...")
    
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    db_path = os.path.join(desktop_path, 'clues.db')
    
    # 获取所有clueNo
    clue_nos = get_all_clue_nos(db_path)
    print(f"Found {len(clue_nos)} clues to process")
    
    if not clue_nos:
        print("No clues found in database")
        return
    
    # 抓取跟进记录
    total_records = extract_follow_up_records(clue_nos, token, db_path)
    
    print(f"Follow-up records extraction completed!")
    print(f"Total records: {total_records}")
    print(f"Database location: {db_path}")

if __name__ == "__main__":
    main()