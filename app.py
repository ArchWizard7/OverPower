from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import secrets
import hashlib
from datetime import datetime

app = Flask(__name__)

# app.secret_key = secrets.token_hex(32)
app.secret_key = "0123456789ABCDEF0123456789ABCDEF"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "BTcfrLkK1FFU"
app.config["MYSQL_DB"] = "overpower"

mysql = MySQL(app)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hash_obj = hashlib.sha256()
        hash_obj.update(password.encode("utf-8"))
        hashed = hash_obj.hexdigest()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed}'")
        user = cursor.fetchone()

        if user:
            session["loggedin"] = True
            session["username"] = user["username"]
            msg = "ログインに成功しました"
            return render_template("index.html", msg=msg, level="success")
        else:
            msg = "メールアドレス もしくは パスワード が間違っています"

    return render_template("login.html", msg=msg, level="danger")


@app.route("/logout")
def logout():
    session.pop("loggedin", None)
    session.pop("username", None)
    return render_template("index.html", msg="ログアウトしました", level="success")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    msg = ""

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hash_obj = hashlib.sha256()
        hash_obj.update(password.encode("utf-8"))
        hashed = hash_obj.hexdigest()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"SELECT * FROM users WHERE username = '{username}' OR email = '{email}'")
        user = cursor.fetchone()

        if user:
            msg = "そのアカウントは既に存在します"
        else:
            now = datetime.now()
            created_at = now.strftime('%Y/%m/%d %H:%M:%S')

            cursor.execute(f"INSERT INTO users VALUES ('{username}', '{email}', '{hashed}', '{created_at}')")
            mysql.connection.commit()

            session["loggedin"] = True
            session["username"] = username
            msg = "アカウント登録に成功しました"
            return render_template("index.html", msg=msg, level="success")

    return render_template("signup.html", msg=msg, level="danger")


@app.route("/developer")
def developer_page():
    return render_template("developer.html")


@app.route("/navbar")
def navbar():
    return render_template("navbar.html")





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
