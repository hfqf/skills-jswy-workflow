import sqlite3
import os

def create_database():
    """创建SQLite数据库和表"""
    # 在当前工作目录创建数据库
    db_path = os.path.join(os.getcwd(), 'clues.db')
    
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

if __name__ == "__main__":
    db_path = create_database()
    print(f"数据库创建成功: {db_path}")