# 🔗 URL Shortener with Analytics

A clean and scalable URL shortener built using Flask, with built-in click tracking and analytics. This project mimics real-world systems like Bitly and TinyURL.

> 🚀 **Live Demo**  
👉 [https://url-shortener1-dqzy.onrender.com](https://url-shortener1-dqzy.onrender.com)

---

## ✨ Features

- 🔗 Shorten long URLs
- 📈 Track visits & click count
- 🖥️ Clean and responsive frontend
- 🗂️ SQLite-based lightweight DB
- 📊 Analytics dashboard
- 💾 Persistent storage
- 🔒 Ready for Docker, Redis & PostgreSQL integration

---

## 🖼️ Screenshots

### 🔘 Home Page (URL Shortener)

![Home Page](static/screenshots/home.png)

---

### 📊 Analytics Dashboard

![Analytics Page](static/screenshots/analytics.png)

---

## 🧱 Tech Stack

- **Frontend:** HTML, CSS, Jinja2
- **Backend:** Flask
- **Database:** SQLite (PostgreSQL coming soon)
- **Deployment:** Render (Free Tier)
- **WSGI Server:** Gunicorn

---

## 🛠️ How to Run Locally

```bash
# Clone the repository
git clone https://github.com/nagasrireddy/url-shortener.git
cd url-shortener

# Create virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py



