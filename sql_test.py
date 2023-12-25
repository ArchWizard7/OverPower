import mysql.connector

conn = mysql.connector.connect(
    user="root",
    password="BTcfrLkK1FFU",
    host="localhost",
    database="overpower"
)

cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM musics LIMIT 1")

musics = cursor.fetchall()

print(musics)
