# -*- coding: utf-8 -*-
import sqlite3
db_path = r'C:\Users\hfqf1\.openclaw\workspace\clues.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 更新第二页的手机号
updates = [
    ('13913031077', '202603031154317724'),
    ('18119819223', '202603031045286088'),
    ('15025334533', '202603030950412998'),
    ('18228010610', '202603030929582475'),
    ('13401830188', '202603030902368969'),
    ('15336873915', '202603030732018589'),
    ('15050866303', '202603030713018535'),
    ('15050866303', '202603030712018529'),
    ('15368638446', '202603030448438371'),
    ('15683658974', '202603030341058322'),
]

for phone, clue_no in updates:
    cursor.execute('UPDATE clues SET phone = ? WHERE clueNo = ?', (phone, clue_no))
    print(f'Updated: {clue_no} -> {phone}')

conn.commit()
conn.close()
print('\nDatabase updated successfully!')
