from flask import Flask, render_template, request, redirect, url_for
import string
import random
import sqlite3
import os

app = Flask(__name__, static_folder='static')

# Ensure instance directory exists
if not os.path.exists("instance"):
    os.makedirs("instance")

# Initialize SQLite database
conn = sqlite3.connect('instance/urls.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        short_url TEXT NOT NULL UNIQUE,
        visits INTEGER DEFAULT 0
    )
''')
conn.commit()

def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choices(characters, k=length))
        cursor.execute("SELECT * FROM urls WHERE short_url = ?", (short_url,))
        if not cursor.fetchone():
            return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_url = generate_short_url()

        cursor.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)",
                       (original_url, short_url))
        conn.commit()

        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_short_url(short_url):
    cursor.execute("SELECT original_url, visits FROM urls WHERE short_url = ?", (short_url,))
    result = cursor.fetchone()
    if result:
        original_url, visits = result
        cursor.execute("UPDATE urls SET visits = ? WHERE short_url = ?", (visits + 1, short_url))
        conn.commit()
        return redirect(original_url)
    return 'Invalid URL', 404

@app.route('/analytics')
def analytics():
    cursor.execute("SELECT original_url, short_url, visits FROM urls")
    data = cursor.fetchall()
    return render_template('analytics.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
