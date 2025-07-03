from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if not URL.query.filter_by(short_code=code).first():
            return code

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    short_url = None

    if request.method == 'POST':
        original_url = request.form.get('original_url')
        if not original_url:
            message = "❌ Please enter a valid URL."
        else:
            short_code = generate_short_code()
            new_url = URL(original_url=original_url, short_code=short_code)
            db.session.add(new_url)
            db.session.commit()
            short_url = request.host_url + short_code
            message = "✅ URL shortened successfully!"

    return render_template('index.html', short_url=short_url, message=message)

@app.route('/<short_code>')
def redirect_to_original(short_code):
    url = URL.query.filter_by(short_code=short_code).first_or_404()
    url.clicks += 1
    db.session.commit()
    return redirect(url.original_url)

@app.route('/analytics')
def analytics():
    urls = URL.query.all()
    return render_template('analytics.html', urls=urls)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
