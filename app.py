from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    with sqlite3.connect("data.db") as con:
        con.execute("CREATE TABLE IF NOT EXISTS leads (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, source TEXT, follow_up TEXT, note TEXT)")

@app.route("/")
def index():
    with sqlite3.connect("data.db") as con:
        leads = con.execute("SELECT * FROM leads ORDER BY id DESC").fetchall()
    return render_template("index.html", leads=leads)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    phone = request.form["phone"]
    source = request.form["source"]
    follow_up = request.form["follow_up"]
    note = request.form["note"]
    with sqlite3.connect("data.db") as con:
        con.execute("INSERT INTO leads (name, phone, source, follow_up, note) VALUES (?, ?, ?, ?, ?)", 
                    (name, phone, source, follow_up, note))
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)
