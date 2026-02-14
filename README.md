# 🌙 Talking to the Moon

> “When you talk to the moon, it listens.”
>
> A Flask web application that analyzes user emotions using Google Gemini AI
> and recommends mood-based music with personalized comfort messages.

---

## 🎬 Demo

Video demonstration of the application:  
https://youtu.be/cidxwCb9ed4

---

## 📌 Overview

**Talking to the Moon** is a full-stack web application that:

1. Accepts user text input
2. Uses Google Gemini API (LLM-based inference) to classify emotional tone
3. Recommends music based on detected mood
4. Displays a comfort message
5. Stores user history for logged-in users

The application demonstrates integration of:

- LLM-based emotion classification
- User authentication
- Database persistence
- Dynamic template rendering

---

## ✨ Features

- 🔍 **Emotion Detection**  
  Classifies text into one of:  
  `happy`, `sad`, `angry`, `calm`, `anxious`, `hopeful`, `bored`

- 🎵 **Mood-Based Music Recommendation**  
  Plays local audio files based on emotional state

- 💬 **Comfort Messaging**  
  Displays a customized supportive message

- 👤 **User Authentication**
  - Register
  - Login
  - Logout

- 📜 **Playlist History**
  - Stores past emotional states
  - Displays recommendation history

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|----------|
| **Python (Flask)** | Backend web framework |
| **SQLite3** | Persistent data storage |
| **Google Gemini API** | Emotion classification |
| **Jinja2** | Template rendering |
| **Flask-Session** | Server-side session management |
| **HTML / CSS / JS** | Frontend interface |

---

## 🗂 Project Structure

MiniWebApplication/
│
├── app.py
├── helpers.py
├── schema.sql
├── requirements.txt
├── .env.example
├── .gitignore
│
├── templates/
│ ├── layout.html
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── result.html
│ └── playlist.html
│
└── static/
├── style.css
├── scripts.js
└── music/



---

## 🔐 Security Considerations

- Passwords are hashed using `werkzeug.security`
- Session data is stored server-side
- API keys are loaded from environment variables
- Emotion output is restricted to a fixed whitelist
- Fallback logic ensures safe handling of unexpected model responses
- SQL queries use parameterized statements to prevent SQL injection

---

## 🗄 Database Schema

### users
- id (INTEGER, primary key)
- username (TEXT, unique)
- password_hash (TEXT)
- created_at (TEXT)

### songs
- id (INTEGER, primary key)
- user_id (INTEGER, foreign key → users.id)
- title (TEXT)
- emotion (TEXT)
- created_at (TEXT)

---

## 🚀 Running Locally

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt


### 2️⃣ Set environment variables

Mac / Linux:

export GEMINI_API_KEY="your_api_key"
export SECRET_KEY="a_random_secret_key"
export PORT=8000

Windows PowerShell:

$env:GEMINI_API_KEY="your_api_key"
$env:SECRET_KEY="a_random_secret_key"
$env:PORT="8000"


3️⃣ Run the application

python app.py


Visit:
http://127.0.0.1:8000


🔮 Future Improvements

Deploy to cloud platform (Render / Fly.io)

Replace SQLite with PostgreSQL

Add user profile settings

Improve UI/UX design

Add visualization for mood history




👩‍💻 Author

Naomi Li
MiniWebApplication — 2026
