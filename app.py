from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isim = db.Column(db.String(100))
    telefon = db.Column(db.String(50))
    kaynak = db.Column(db.String(50))
    tarih = db.Column(db.String(50))
    notlar = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        isim = request.form["isim"]
        telefon = request.form["telefon"]
        kaynak = request.form["kaynak"]
        tarih = request.form["tarih"]
        notlar = request.form["not"]

        new_lead = Lead(isim=isim, telefon=telefon, kaynak=kaynak, tarih=tarih, notlar=notlar)
        db.session.add(new_lead)
        db.session.commit()
        return redirect("/")

    leads = Lead.query.all()
    return render_template("index.html", leads=leads)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

