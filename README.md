# 🔗 URL Shortener with Analytics

A clean and scalable URL shortener built using Flask, with built-in click tracking and analytics. This project mimics real-world systems like Bitly and TinyURL.

[![Deploy on Render](https://img.shields.io/badge/Deploy-Render-blue?style=flat-square&logo=render)](https://url-shortener1-dqzy.onrender.com)
[![GitHub stars](https://img.shields.io/github/stars/nagasrireddy/url-shortener?style=social)](https://github.com/nagasrireddy/url-shortener)

---

## 🚀 Live Demo

👉 [Live Project](https://url-shortener1-dqzy.onrender.com)

---

## ✨ Features

- 🔗 Shorten long URLs
- 📈 Track visits & click count
- 🖥️ Clean and responsive frontend
- 🗂️ SQLite-based lightweight DB
- 📊 Basic analytics dashboard
- 💾 Persistent storage
- ⚙️ Ready for Docker, Redis & PostgreSQL integration

---

## 🖼️ Screenshots

| Home | Shorten Success | Analytics Dashboard |
|------|------------------|---------------------|
| ![Home](static/screenshots/home.png) | ![Shortened](static/screenshots/shorten-success.png) | ![Analytics](static/screenshots/analytics.png) |

---

## 🧱 Tech Stack

- **Frontend:** HTML, CSS, Jinja2
- **Backend:** Flask (Python)
- **Database:** SQLite (upgradable to PostgreSQL)
- **Deployment:** Render
- **Server:** Gunicorn

---

## 🛠️ How to Run Locally

```bash
# Clone the repository
git clone https://github.com/nagasrireddy/url-shortener.git
cd url-shortener

# Create virtual environment
python -m venv venv
# Activate it
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py


