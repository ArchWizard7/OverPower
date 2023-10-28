from flask import Flask, render_template, request, session, url_for, redirect
import mysql.connector as mydb
import hashlib
from datetime import datetime
import requests
from PIL import Image
import io
import json
import math
import base64
from decimal import Decimal

app = Flask(__name__)

# app.secret_key = secrets.token_hex(32)
# app.secret_key = "0123456789ABCDEF0123456789ABCDEF"
app.secret_key = "01839749127492797979537903792750"

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


def rating(const, score):
    if score >= 1009000:
        return Decimal(const) + Decimal(2.15)
    elif 1007500 <= score <= 1008999:
        return (Decimal(const) + Decimal(2.0)) + ((Decimal(score) - Decimal(1007500)) / 10000)
    elif 1005000 <= score <= 1007499:
        return (Decimal(const) + Decimal(1.5)) + ((Decimal(score) - Decimal(1005000)) / 5000)
    elif 1000000 <= score <= 1004999:
        return (Decimal(const) + Decimal(1.0)) + ((Decimal(score) - Decimal(1000000)) / 10000)
    elif 990000 <= score <= 999999:
        return (Decimal(const) + Decimal(0.6)) + ((Decimal(score) - Decimal(990000)) / 25000)
    elif 975000 <= score <= 989999:
        return Decimal(const) + ((Decimal(score) - Decimal(975000)) / 25000)
    elif 925000 <= score <= 974999:
        return (Decimal(const) - Decimal(3.0)) + ((Decimal(score) - Decimal(925000)) / (Decimal(50000) / Decimal(3)))
    elif 900000 <= score <= 924999:
        return (Decimal(const) - Decimal(5.0)) + ((Decimal(score) - Decimal(900000)) / 12500)
    elif 800000 <= score <= 899999:
        return (Decimal(const) - Decimal(5.0)) * (Decimal(0.5) + (Decimal(score) - Decimal(800000)) / Decimal(200000))
    elif 500000 <= score <= 799999:
        return (Decimal(const) - Decimal(5.0)) * (Decimal(score) - Decimal(500000)) / 600000
    else:
        return 0


def diff_format(diff):
    if (diff * 10) % 10 >= 5:
        return f"{int(diff)}+"
    else:
        return f"{int(diff)}"


@app.route("/")
@app.route("/index")
def index():
    try:
        username = session["username"]

        total_op = {
            "POSSESSION": 0.0,
            "BAS": 0.0, "ADV": 0.0, "EXP": 0.0, "MAS": 0.0, "ULT": 0.0,
            "POPS&ANIME": 0.0, "niconico": 0.0, "東方Project": 0.0, "VARIETY": 0.0, "イロドリミドリ": 0.0, "ゲキマイ": 0.0, "ORIGINAL": 0.0,
            "10": 0.0, "10+": 0.0, "11": 0.0, "11+": 0.0, "12": 0.0, "12+": 0.0, "13": 0.0, "13+": 0.0, "14": 0.0, "14+": 0.0, "15": 0.0,
            "A～G": 0.0, "H～N": 0.0, "O～U": 0.0, "V～Z": 0.0, "あ行": 0.0, "か行": 0.0, "さ行": 0.0, "た行": 0.0, "な行": 0.0, "は行": 0.0, "ま行": 0.0, "や行": 0.0, "ら行": 0.0, "わ行": 0.0, "数字": 0.0
        }

        max_op = {
            "POSSESSION": 0.0,
            "BAS": 0.0, "ADV": 0.0, "EXP": 0.0, "MAS": 0.0, "ULT": 0.0,
            "POPS&ANIME": 0.0, "niconico": 0.0, "東方Project": 0.0, "VARIETY": 0.0, "イロドリミドリ": 0.0, "ゲキマイ": 0.0, "ORIGINAL": 0.0,
            "10": 0.0, "10+": 0.0, "11": 0.0, "11+": 0.0, "12": 0.0, "12+": 0.0, "13": 0.0, "13+": 0.0, "14": 0.0, "14+": 0.0, "15": 0.0,
            "A～G": 0.0, "H～N": 0.0, "O～U": 0.0, "V～Z": 0.0, "あ行": 0.0, "か行": 0.0, "さ行": 0.0, "た行": 0.0, "な行": 0.0, "は行": 0.0, "ま行": 0.0, "や行": 0.0, "ら行": 0.0, "わ行": 0.0, "数字": 0.0
        }

        title_to_genre = {}
        title_to_const = {}
        title_to_ruby = {}

        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM musics")
        musics = cursor.fetchall()

        for row in musics:
            title = row['title']

            title_to_genre[title] = row["genre"]
            title_to_ruby[title] = row["ruby"]

            title_to_const[f"{title}_BAS"] = row["basic-const"]
            title_to_const[f"{title}_ADV"] = row["advanced-const"]
            title_to_const[f"{title}_EXP"] = row["expert-const"]
            title_to_const[f"{title}_MAS"] = row["master-const"]
            title_to_const[f"{title}_ULT"] = row["ultima-const"]

        cursor.execute(f"SELECT * FROM {username.lower()}")
        results = cursor.fetchall()

        # print(results)

        if len(results) <= 0:
            return render_template("no_data.html", msg="データが存在しません", level="danger")

        count = 0

        for row in results:
            title = str(row["id"])
            difficulty = str(title[(len(title) - 3):])
            score = int(row["score"])
            ramp = str(row["ramp"])
            locked = int(row["locked"])

            if locked == 0:
                max_temp = (title_to_const[title] + 3) * 5
                max_op[difficulty] += max_temp

                additional = 0.0

                if ramp == "FC":
                    additional1 = 0.5
                elif ramp == "AJ":
                    additional1 = 1.0
                else:
                    additional1 = 0.0

                if score >= 1010000:
                    additional = (title_to_const[title] + 3) * 5
                elif 1007501 <= score <= 1009999:
                    additional = (title_to_const[title] + 2) * 5 + additional1 + ((score - 1007500) * 0.0015)
                elif 975000 <= score <= 1007500:
                    additional = (float(rating(title_to_const[title], score)) * 5) + additional1

                additional = additional * 10000
                additional = round(additional)
                additional -= (additional % 50)
                additional /= 10000

                if "_MAS" in title or "_ULT" in title:
                    title2 = title[:(len(title) - 4)]
                    genre = title_to_genre[title2]
                    diff = diff_format(title_to_const[title])
                    ruby = title_to_ruby[title2]

                    max_op["POSSESSION"] += max_temp
                    total_op["POSSESSION"] += additional

                    max_op[genre] += max_temp
                    max_op[diff] += max_temp
                    max_op[ruby] += max_temp
                    total_op[genre] += additional
                    total_op[diff] += additional
                    total_op[ruby] += additional

                    count += 1
                    print(f"{count}\\t{title}\\t{float(rating(title_to_const[title], score))}\\t{additional}")

                total_op[difficulty] += additional

        print(total_op)
        print(max_op)

        return render_template("index.html", total_op=total_op, max_op=max_op)
    except KeyError:
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

        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed}'")
        user = cur.fetchone()

        if user:
            session["loggedin"] = True
            session["username"] = user["username"]
            return redirect(url_for("index"))
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

            cur.execute(f"CREATE TABLE {username} LIKE user_template")
            cur.execute(f"INSERT INTO users VALUES ('{username}', '{email}', '{hashed}', '{created_at}')")
            conn.commit()

            session["loggedin"] = True
            session["username"] = username
            return redirect(url_for("index"))

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
