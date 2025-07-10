from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('crm.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    leads = conn.execute('SELECT * FROM leads').fetchall()
    conn.close()
    return render_template('index.html', leads=leads)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    phone = request.form['phone']
    source = request.form['source']
    followup = request.form['followup']
    note = request.form['note']
    conn = get_db_connection()
    conn.execute('INSERT INTO leads (name, phone, source, followup, note) VALUES (?, ?, ?, ?, ?)',
                 (name, phone, source, followup, note))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/lead/<int:lead_id>', methods=['GET', 'POST'])
def lead_detail(lead_id):
    conn = get_db_connection()
    lead = conn.execute('SELECT * FROM leads WHERE id = ?', (lead_id,)).fetchone()

    if request.method == 'POST':
        note = request.form['new_note']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('INSERT INTO notes (lead_id, note, timestamp) VALUES (?, ?, ?)', (lead_id, note, timestamp))
        conn.commit()

    notes = conn.execute('SELECT * FROM notes WHERE lead_id = ? ORDER BY timestamp DESC', (lead_id,)).fetchall()
    conn.close()
    return render_template('lead_detail.html', lead=lead, notes=notes)

def init_db():
    conn = get_db_connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS leads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        phone TEXT,
                        source TEXT,
                        followup TEXT,
                        note TEXT
                    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lead_id INTEGER,
                        note TEXT,
                        timestamp TEXT
                    )""")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
