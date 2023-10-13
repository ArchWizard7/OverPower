import mysql.connector as mydb

conn = mydb.connect(
    host="localhost",
    port=3306,
    user="root",
    password="BTcfrLkK1FFU",
    database="overpower"
)

cur = conn.cursor(dictionary=True)
cur.execute("SELECT * FROM musics LIMIT 1;")
data = cur.fetchall()

print(data)

for row in data:
    print(row)

