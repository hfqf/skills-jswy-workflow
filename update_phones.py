# -*- coding: utf-8 -*-
import sqlite3
db_path = r'C:\Users\hfqf1\.openclaw\workspace\clues.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 更新今天线索的手机号 (第一页)
updates = [
    ('18018066856', '202603031417010647'),
    ('19334125383', '202603031412020573'),
    ('18913312664', '202603031406590471'),
    ('18994522903', '202603031359250081'),
    ('15996353708', '202603031357590053'),
    ('17301591800', '202603031350489961'),
    ('19962042207', '202603031327049603'),
    ('18667231309', '202603031314499424'),
    ('19702268065', '202603031243519048'),
    ('18202446694', '202603031155597738'),
]

for phone, clue_no in updates:
    cursor.execute('UPDATE clues SET phone = ? WHERE clueNo = ?', (phone, clue_no))
    print(f'Updated: {clue_no} -> {phone}')

conn.commit()
conn.close()
print('\nDatabase updated successfully!')
