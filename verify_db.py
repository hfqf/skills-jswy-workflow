# -*- coding: utf-8 -*-
import sqlite3
db_path = r'C:\Users\hfqf1\.openclaw\workspace\clues.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('=== 线索表记录 ===')
cursor.execute('SELECT clueNo, phone, nickName, shopName, createTime FROM clues ORDER BY createTime DESC')
for row in cursor.fetchall():
    print(f'{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}')

count = cursor.execute('SELECT COUNT(*) FROM clues').fetchone()[0]
print(f'\n总计: {count} 条线索')

print('\n=== 跟进记录表记录 ===')
count2 = cursor.execute('SELECT COUNT(*) FROM follow_records').fetchone()[0]
print(f'总计: {count2} 条跟进记录')

conn.close()
