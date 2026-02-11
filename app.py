import os
import sqlite3
import logging
from pathlib import Path

from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, analyze_emotion

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = os.environ.get("DATABASE_PATH", str(BASE_DIR / "talking.db"))

app = Flask(__name__)

# SECURITY: do not hardcode in public repos
app.secret_key = os.environ.get("SECRET_KEY", "dev_only_change_me")

# Server-side session storage (good for small projects)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    schema_file = BASE_DIR / "schema.sql"
    if not schema_file.exists():
        logger.warning("schema.sql not found; skipping init_db()")
        return
    with get_db_connection() as conn, open(schema_file, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
        conn.commit()


@app.before_first_request
def _startup():
    init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            flash("Please input username and password.")
            return redirect("/login")

        with get_db_connection() as conn:
            row = conn.execute(
                "SELECT id, username, password_hash FROM users WHERE username = ?",
                (username,),
            ).fetchone()

        if row is None or not check_password_hash(row["password_hash"], password):
            flash("Wrong username or password.")
            return redirect("/login")

        session["user_id"] = row["id"]
        return redirect("/")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        confirmation = request.form.get("confirmation") or ""

        if not username or not password or not confirmation:
            flash("Please fill in the information completely.")
            return redirect("/register")

        if password != confirmation:
            flash("Passwords are not the same.")
            return redirect("/register")

        password_hash = generate_password_hash(password)

        try:
            with get_db_connection() as conn:
                conn.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash),
                )
                conn.commit()
        except sqlite3.IntegrityError:
            flash("Username already exists.")
            return redirect("/register")

        flash("Registration successful. Please log in.")
        return redirect("/login")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/analyze", methods=["POST"])
@login_required
def analyze():
    user_input = (request.form.get("message") or "").strip()
    if not user_input:
        flash("Please enter a message to analyze.")
        return redirect("/")

    emotion = analyze_emotion(user_input)

    recommendations = {
        "sad": {"title": "Melancholy Melody 🎧", "url": "/static/music/sad.mp3"},
        "happy": {"title": "Cheerful Rhythm 😊", "url": "/static/music/happy.mp3"},
        "angry": {"title": "Cool Down 🎸", "url": "/static/music/angry.mp3"},
        "calm": {"title": "Peaceful Piano 🌿", "url": "/static/music/calm.mp3"},
        "anxious": {"title": "Breathe and Relax 🌲", "url": "/static/music/anxious.mp3"},
        "hopeful": {"title": "Gentle Hope ☀️", "url": "/static/music/hopeful.mp3"},
        "bored": {"title": "Lazy Afternoon Tea 🎵", "url": "/static/music/bored.mp3"},
    }

    suggestion = recommendations.get(emotion, recommendations["calm"])
    suggestion_title = suggestion["title"]
    music_url = suggestion["url"]

    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO songs (user_id, title, emotion) VALUES (?, ?, ?)",
            (session["user_id"], suggestion_title, emotion),
        )
        conn.commit()

    comforts = {
        "sad": "Don’t be sad — the moon is quietly listening to your story 🌙",
        "happy": "Your smile makes the whole world brighter ☀️",
        "angry": "Take a deep breath — everything will be fine 🍃",
        "calm": "Keep your heart peaceful — that’s your true beauty 🌿",
        "anxious": "Slow down your breath, life will soon treat you gently 🌊",
        "hopeful": "The light you believe in is slowly drawing near ✨",
        "bored": "Even in ordinary days, there are small moments of joy ☕",
    }
    comfort = comforts.get(
        emotion,
        "No matter how you feel right now, you deserve to be treated with kindness 💫",
    )

    return render_template(
        "result.html",
        user_input=user_input,
        emotion=emotion,
        suggestion_title=suggestion_title,
        music_url=music_url,
        comfort=comfort,
    )


@app.route("/playlist")
@login_required
def playlist():
    with get_db_connection() as conn:
        songs = conn.execute(
            "SELECT title, emotion, created_at FROM songs WHERE user_id = ? ORDER BY id DESC",
            (session["user_id"],),
        ).fetchall()
    return render_template("playlist.html", songs=songs)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)

