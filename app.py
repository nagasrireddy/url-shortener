from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(6), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        if not URL.query.filter_by(short_code=code).first():
            return code

@app.route('/', methods=['GET', 'POST'])
def index():
    shortened_url = None
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_code = generate_short_code()
        new_url = URL(original_url=original_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        shortened_url = request.host_url + short_code
        return render_template('index.html', shortened_url=shortened_url, success=True)
    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if url_entry:
        url_entry.clicks += 1
        db.session.commit()
        return redirect(url_entry.original_url)
    else:
        return 'Invalid URL', 404

@app.route('/analytics')
def analytics():
    urls = URL.query.all()
    return render_template('analytics.html', urls=urls)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=10000)

