import sqlite3

conn = sqlite3.connect("/root/projects/mysite/db.sqlite3")

cur = conn.cursor()

S = "SELECT id FROM pybo_question WHERE id="+"6"
cur.execute(S)

rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()

if rows==[]:
    print('null')
else:
    print(rows)
