# PROJECT TITLE: TALKING TO THE MOON

> ***“When you talk to the moon, it listens.”***
> ***A web app that understands your emotions and recommends soothing music.***
### Video Demo:  <(https://youtu.be/cidxwCb9ed4)>
---

## Descriptions

This app is a Flask-based web application that uses **Google Gemini AI** to analyze users’ emotions from text input.
It then recommends mood-based music (from local MP3 files) and offers comforting words.
Registered users can also log in, save their favorite songs, and revisit their playlists.


### Features

- **Emotion Analysis** — Detects emotional tone from text using Gemini AI.
- **Music Recommendation** — Plays emotion-based local MP3 music.
- **Comfort Messages** — Shows a soothing quote based on the detected mood.
- **User Accounts** — Register, log in, log out, and list history songs.
- **Playlist History** — View all songs recommended based on your past moods.

---

### Tech Stack

| Technology | Purpose |
|-------------------------|-----------------------|
| **Python (Flask)**      | Backend web framework |
| **SQLite3 (CS50 SQL)**  | Database for users and songs |
| **Google Gemini API**   | Emotion detection engine |
| **HTML / CSS / Jinja2** | Frontend templates |
| **Flask-Session** | User session management |

---

### Project Structure
project/
│
├── app.py # Main Flask application
├── helpers.py # Login validation and emotion analysis
├── templates/ # HTML templates
│ ├── index.html(Home page of the web where user can input their mood)
│ ├── login.html(user login)
│ ├── layout.html
│ ├── register.html(new user register)
│ ├── result.html(show the result of analysing users' mood)
│ └── playlist.html(save the record of songs)
│
├── static/
│ ├── scripts.js
│ ├── style.css
│ └── music/ # Local audio files (MP3)
│   ├── sad.mp3
│   ├── happy.mp3
│   ├── calm.mp3
│   ├── anxious.mp3
│   ├── hopeful.mp3
│   ├── bored.mp3
│   └── angry.mp3
│
└── talking.db # SQLite database

### Brief Introduction
#### app.py
This backend doc include 6 routers which are: /index(home page), /login, /logout, /register, /playlist and /analyse. It helps processing the logic of my whole app, such as user login, database reading and writing, calling Gemini API to analyze emotions, select music, etc.

#### helpers.py
This doc is a backend utility module that provides two main functions to the Flask web application: user authentication control — ensures that only logged-in users can access certain routes and emotion analysis using Gemini AI — communicates with Google’s Gemini API to analyze users’ text input and identify their emotional state.

#### talking.db
This doc is a SQLite database file. It saves the username and encrypted password into the users table of talking.db. It records who the user is, what they listened to, and their emotions at the time they are using.

#### templates
In the templates folder, it includes all the frontend html file which are index.html, layout.html, login.html, playlist.html, register.html and result.html.And layout.html is the base template of all the other html files.

#### static
In the static folder are the documents where I wrote the javascript and css and also store the local music mp3 file. I use Javascript and css to make my website more dynamic and beautiful to use.
