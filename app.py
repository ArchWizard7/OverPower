from flask import Flask, render_template, request, session
import mysql.connector as mydb
import hashlib
from datetime import datetime
import requests
from PIL import Image
import io
import json
import base64

app = Flask(__name__)

# app.secret_key = secrets.token_hex(32)
app.secret_key = "0123456789ABCDEF0123456789ABCDEF"

conn = mydb.connect(
    host="localhost",
    port=3306,
    user="root",
    password="BTcfrLkK1FFU",
    database="overpower"
)

conn.ping(reconnect=True)

print(conn.is_connected())


def url_to_base64(url):
    response = requests.get(url)

    if response.status_code != 200:
        url = "http://localhost:5000/static/img/debug.png"  # 画像のURLを指定
        response = requests.get(url)

    # レスポンスから画像データを取得
    image_data = response.content

    # 画像をPillowのImageオブジェクトに変換してリサイズ
    original_image = Image.open(io.BytesIO(image_data))
    resized_image = original_image.resize((128, 128))

    # リサイズされた画像をBase64形式に変換
    buffered = io.BytesIO()
    resized_image.save(buffered, format="PNG")
    base64_image = base64.b64encode(buffered.getvalue()).decode()

    # Base64形式の画像データを使って何かをする
    # 例えば、Flaskを使ってWebアプリケーションのAPIで返すなど
    return f"data:image/png;base64,{base64_image}"


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


# noinspection PyTypeChecker
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hash_obj = hashlib.sha256()
        hash_obj.update(password.encode("utf-8"))
        hashed = hash_obj.hexdigest()

        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed}'")
        user = cur.fetchone()

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

        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT * FROM users WHERE username = '{username}' OR email = '{email}'")
        user = cur.fetchone()

        if user:
            msg = "そのアカウントは既に存在します"
        else:
            now = datetime.now()
            created_at = now.strftime('%Y/%m/%d %H:%M:%S')

            cur.execute(f"INSERT INTO users VALUES ('{username}', '{email}', '{hashed}', '{created_at}')")
            cur.execute(f"CREATE TABLE {username.lower()} LIKE user_template")
            conn.commit()

            session["loggedin"] = True
            session["username"] = username
            msg = "アカウント登録に成功しました"
            return render_template("index.html", msg=msg, level="success")

    return render_template("signup.html", msg=msg, level="danger")


@app.route("/developer")
def developer_page():
    msg = ""

    return render_template("developer.html", msg=msg, success=False)


@app.route("/music-list")
def music_list():
    args = request.args

    # ページ番号
    num = 1

    if args.get("p") is not None:
        num = int(args.get("p"))

    limit = 100
    offset = (num - 1) * 100

    cur = conn.cursor(dictionary=True)
    cur.execute(f"SELECT * FROM musics ORDER BY id LIMIT {limit} OFFSET {offset}")
    musics = cur.fetchall()

    return render_template("music-list.html", musics=musics, num=num, max_page=13)


@app.route("/navbar")
def navbar():
    return render_template("navbar.html")


@app.route("/register-music", methods=["POST"])
def register_music():
    msg = """
    <i class="bi-check-circle-fill"></i>
    楽曲の挿入に成功しました
    """

    form = request.form

    identifier = form["id"]
    title = form["title"]
    ruby = form["ruby"]
    artist = form["artist"]
    genre = form["genre"]
    version = form["version"]
    bpm = form["bpm"]
    jacket_url = form["jacket-url"]
    basic_const = form["basic-const"]
    advanced_const = form["advanced-const"]
    expert_const = form["expert-const"]
    master_const = form["master-const"]
    ultima_const = form["ultima-const"]
    expert_nd = form["expert-nd"]
    master_nd = form["master-nd"]
    ultima_nd = form["ultima-nd"]

    jacket_base64 = url_to_base64(jacket_url)

    # print(form)

    cur = conn.cursor(dictionary=True)

    # UPDATE
    # print("[ UPDATE ]")
    # print(f"UPDATE musics SET id = (id + 1) WHERE (id >= {identifier})")

    cur.execute(f"UPDATE musics SET id = (id + 1) WHERE (id >= {identifier})")
    conn.commit()

    # INSERT
    # print("[ INSERT ]")
    # print(f"""INSERT INTO musics VALUES (
    # '{identifier}', '{title}', '{ruby}', '{artist}', '{genre}', '{version}', '{bpm}', '{jacket_base64}',
    # '{basic_const}', '{advanced_const}', '{expert_const}', '{master_const}', '{ultima_const}',
    # '{expert_nd}', '{master_nd}', '{ultima_nd}'
    # )
    # """)

    cur.execute(f"""INSERT INTO musics VALUES (
    '{identifier}', '{title}', '{ruby}', '{artist}', '{genre}', '{version}', '{bpm}', '{jacket_base64}',
    '{basic_const}', '{advanced_const}', '{expert_const}', '{master_const}', '{ultima_const}',
    '{expert_nd}', '{master_nd}', '{ultima_nd}'
    )
    """)
    conn.commit()

    return render_template("developer.html", msg=msg, success=True)


@app.route("/delete-music")
def delete_music():
    msg = """
    <i class="bi-check-circle-fill"></i>
    楽曲の削除に成功しました
    """

    args = request.args
    identifier = int(args.get("id"))

    cur = conn.cursor(dictionary=True)

    # DELETE
    # print("[ DELETE ]")
    # print(f"DELETE FROM musics WHERE id = '{identifier}'")

    cur.execute(f"DELETE FROM musics WHERE id = '{identifier}'")
    conn.commit()

    # UPDATE
    # print("[ UPDATE ]")
    # print(f"UPDATE musics SET id = (id - 1) WHERE (id >= {identifier + 1})")

    cur.execute(f"UPDATE musics SET id = (id - 1) WHERE (id >= {identifier + 1})")
    conn.commit()

    return render_template("music-list.html", msg=msg, success=True, num=1, max_page=13)


@app.route("/get-musics")
def get_musics():
    args = request.args

    # ページ番号
    num = 1

    if args.get("p") is not None:
        num = int(args.get("p"))

    limit = 100
    offset = (num - 1) * 100

    cur = conn.cursor(dictionary=True)
    cur.execute(f"SELECT * FROM musics ORDER BY id LIMIT {limit} OFFSET {offset}")
    musics = cur.fetchall()
    json_data = json.dumps(musics, indent=4, ensure_ascii=False)

    return json_data, 200, {
        "Content-Type": "application/json"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
