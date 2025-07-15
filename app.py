from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from urllib.parse import urlparse
from datetime import datetime
import string
import random
import os
from pathlib import Path

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-strong-secret-key-here'
# Replace your current SQLALCHEMY_DATABASE_URI with:
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    f"sqlite:///{os.path.join(os.path.dirname(__file__), 'instance', 'shortener.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ... after your imports and app configuration ...

# Helper Functions
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except:
        return False

def ensure_proper_url(url):
    """Ensure the URL has a proper scheme (http/https)"""
    parsed = urlparse(url)
    if not parsed.scheme:
        return 'http://' + url
    return url

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        short = ''.join(random.choices(chars, k=length))
        if not URL.query.filter_by(short_url=short).first():
            return short

# ... rest of your code (models, routes, etc.) ...

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except:
        return False

# Helper Functions
def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        short = ''.join(random.choices(chars, k=length))
        if not URL.query.filter_by(short_url=short).first():
            return short

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    urls = db.relationship('URL', backref='user', lazy=True)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2000), nullable=False)
    short_url = db.Column(db.String(50), unique=True, nullable=False, index=True)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# 4. FORM CLASSES - ADD THEM HERE
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500
# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please login to shorten URLs', 'danger')
            return redirect(url_for('login'))
        
        original_url = request.form.get('original_url', '').strip()
        custom_url = request.form.get('custom_url', '').strip()
        
        if not original_url:
            flash('URL is required', 'danger')
            return redirect(url_for('index'))
            
        if not is_valid_url(original_url):
            flash('Invalid URL format', 'danger')
            return redirect(url_for('index'))
            
        if len(original_url) > 2000:
            flash('URL too long (max 2000 chars)', 'danger')
            return redirect(url_for('index'))
        
        short_url = custom_url if custom_url else generate_short_url()
        
        if URL.query.filter_by(short_url=short_url).first():
            flash('Short URL already exists', 'danger')
            return redirect(url_for('index'))
        
        proper_url = ensure_proper_url(original_url)
        new_url = URL(
            original_url=proper_url,
            short_url=short_url,
            user_id=current_user.id
        )
        
        try:
            db.session.add(new_url)
            db.session.commit()
            return render_template('shortened.html', 
                                short_url=short_url,
                                original_url=proper_url)
        except Exception as e:
            db.session.rollback()
            flash('Error creating short URL', 'danger')
            return redirect(url_for('index'))
    
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_short_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    url.clicks += 1
    db.session.commit()
    return redirect(url.original_url)

@app.route('/analytics')
@login_required
def analytics():
    urls = URL.query.filter_by(user_id=current_user.id).all()
    return render_template('analytics.html', urls=urls)

# Auth Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        
        flash('Invalid email or password', 'danger')
    
    return render_template('login.html', form=form) # Make sure to pass the form

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('register.html', form=form)

# Add this right before db.create_all()
with app.app_context():
    db_dir = os.path.join(os.path.dirname(__file__), 'instance')
    os.makedirs(db_dir, exist_ok=True)  # This creates the directory if it doesn't exist
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)