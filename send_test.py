from bs4 import BeautifulSoup
import mysql.connector

conn = mysql.connector.connect(
    user="root",
    password="BTcfrLkK1FFU",
    host="localhost",
    database="overpower"
)


def update_database(username, difficulty, html_body):
    soup = BeautifulSoup(html_body, "html.parser")
    cursor = conn.cursor(dictionary=True)

    musics = soup.select("div .musiclist_box")

    for row in musics:
        title = row.find(class_="music_title").text.replace("'", "''").replace("&#039;", "''")
        score = 0
        clear = "NONE"
        ramp = "NONE"
        full_chain = "NONE"

        if row.find("span", class_="text_b") is not None:
            score = int(row.find("span", class_="text_b").text.replace(",", ""))

        if row.find(class_="play_musicdata_icon") is not None:
            icon = row.find(class_="play_musicdata_icon")
            images = icon.findAll("img")

            for image in images:
                text = image["src"].replace("https://new.chunithm-net.com/chuni-mobile/html/mobile/images/icon_", "").replace(".png", "")

                if text == "failed":
                    clear = "FAILED"
                elif text == "clear":
                    clear = "CLEAR"
                elif text == "hard":
                    clear = "HARD"
                elif text == "absolute":
                    clear = "ABSOLUTE"
                elif text == "absolutep":
                    clear = "ABSOLUTE+"
                elif text == "catastrophy":
                    clear = "CATASTROPHY"
                elif text == "fullcombo":
                    ramp = "FC"
                elif text == "alljustice":
                    ramp = "AJ"
                elif text == "fullchain2":
                    full_chain = "GOLD"
                elif text == "fullchain":
                    full_chain = "PLATINUM"

            if score == 1010000:
                ramp = "AJC"

        query = f"""INSERT INTO {username.lower()} (id, score, clear, ramp, full_chain, locked) VALUES ('{title}_{difficulty}', '{score}', '{clear}', '{ramp}', '{full_chain}', '0') ON DUPLICATE KEY UPDATE score = VALUES(score), clear = VALUES(clear), ramp = VALUES(ramp), full_chain = VALUES(full_chain)"""

        # print(query)
        cursor.execute(query)

    conn.commit()
    print(f"{difficulty} is done! :)")


difficulties = [
    "BAS",
    "ADV",
    "EXP",
    "MAS",
    "ULT",
]

for difficulty in difficulties:
    with open(f"./static/{difficulty}.html", "r", encoding="utf-8") as file:
        body = file.read()
        update_database("archwizard7", difficulty, body)
