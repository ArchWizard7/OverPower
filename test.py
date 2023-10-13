import mysql.connector as mydb
import json

conn = mydb.connect(
    host="localhost",
    port=3306,
    user="root",
    password="BTcfrLkK1FFU",
    database="overpower"
)

cur = conn.cursor(dictionary=True)
cur.execute("SELECT id, title FROM musics LIMIT 100;")
data = cur.fetchall()

json_data = json.dumps(data, indent=4, ensure_ascii=False)

print(json_data)
