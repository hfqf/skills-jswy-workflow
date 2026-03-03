# -*- coding: utf-8 -*-
import sqlite3
db = r'C:\Users\hfqf1\.openclaw\workspace\clues.db'
conn = sqlite3.connect(db)
c = conn.cursor()
# 检查今天有多少线索
c.execute("SELECT COUNT(*) FROM clues WHERE createTime LIKE '2026-03-03%'")
print('Today clues:', c.fetchone()[0])
# 检查已解密的
c.execute("SELECT clueNo, phone FROM clues WHERE createTime LIKE '2026-03-03%' ORDER BY createTime")
for row in c.fetchall():
    print(row[0], '|', row[1])
conn.close()
