
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import re  # ✅ You correctly pointed out this was missing

app = Flask(__name__)
CORS(app)

# ✅ Ensure database and table exist
def initialize_db():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").lower().strip()

    if not message or len(message) < 2:
        response = "Hi there! Try asking me about Sadia’s skills, projects, or contact info."
    elif "hello" in message or re.search(r"\bhi\b", message):
        response = "Hello there! I am Sadia's assistant, how can I help you?"
    elif "hey" in message:
        response = "Hey! I am Sadia's assistant, how can I help you?"
    elif "skills" in message or "skill" in message:
        response = "Sadia is skilled in HTML, CSS, JavaScript, React, and learning Python."
    elif any(word in message for word in ["your name", "introduction", "intro", "yourself", "who are you", "give me your intro", "introduce"]):
        response = "Hi! I'm Sadia, a Software Engineering student passionate about web development, backend, and AI integration."
    elif "projects" in message:
        response = "Check out Sadia’s projects on GitHub: https://github.com/sadia814"
    elif "contact" in message:
        response = "You can contact Sadia at sadiaabdulmajeed4545@gmail.com or on LinkedIn."
    elif "education" in message or "study" in message:
        response = "Sadia is pursuing a BS in Software Engineering at UCP."
    elif any(word in message for word in ["experience", "internship", "internships", "intern", "training"]):
        response = "Sadia has worked on academic and personal projects, and is actively looking for internship opportunities."
    elif "interests" in message or "passion" in message:
        response = "Sadia is passionate about web development, Python, AI, and creating impactful digital solutions."
    elif "goals" in message or "future" in message:
        response = "Sadia aims to become a full-stack developer and explore AI integration in web platforms."
    else:
        response = "I'm not sure how to answer that. Try asking about skills, projects, or contact."

    # ✅ Save to SQLite
    try:
        conn = sqlite3.connect("chat_history.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chat_history (user_message, bot_response)
            VALUES (?, ?)
        ''', (message, response))
        conn.commit()
        conn.close()
        print(f"✅ Chat saved: {message} → {response}")
    except Exception as e:
        print("❌ Failed to save chat:", e)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

