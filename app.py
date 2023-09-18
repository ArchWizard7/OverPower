from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/developer")
def developer_page():
    return render_template("developer.html")


@app.route("/navbar")
def navbar():
    return render_template("navbar.html")


@app.route("/login")
def login():
    return render_template("login.html")




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
