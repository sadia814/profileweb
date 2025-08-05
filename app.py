from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import re
import os

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)


# Serve frontend
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").lower().strip()

    # Generate response
    if not message or len(message) < 2:
        response = "Hi there! Try asking me about Sadia’s skills, projects, or contact info."
    elif "hello" in message or re.search(r"\bhi\b", message):
        response = "Hello there! I am Sadia's assistant, how can I help you?"
    elif "hey" in message:
        response = "Hey! I am Sadia's assistant, how can I help you?"
    elif "skills" in message or "skill" in message:
        response = "Sadia is skilled in HTML, CSS, JavaScript, React, and learning Python."
    elif any(word in message for word in [
            "your name", "introduction", "intro", "yourself", "who are you",
            "give me your intro", "introduce"
    ]):
        response = "Hi! I'm Sadia, a Software Engineering student passionate about web development, backend, and AI integration."
    elif "projects" in message:
        response = "Check out Sadia’s projects on GitHub: https://github.com/sadia814"
    elif "contact" in message:
        response = "You can contact Sadia at sadiaabdulmajeed4545@gmail.com or on LinkedIn."
    elif any(word in message for word in ["education", "degree", "study"]):
        response = "Sadia is pursuing a BS in Software Engineering at UCP."
    elif any(
            word in message for word in
        ["experience", "internship", "internships", "intern", "training"]):
        response = "Sadia has worked on academic and personal projects, and is actively looking for internship opportunities."
    elif "interests" in message or "passion" in message:
        response = "Sadia is passionate about web development, Python, AI, and creating impactful digital solutions."
    elif "goals" in message or "future" in message:
        response = "Sadia aims to become a full-stack developer and explore AI integration in web platforms."
    else:
        response = "I'm not sure how to answer that. Try asking about skills, projects, or contact."

    # Save chat to a text file
    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(f"User: {message}\n")
        file.write(f"SadiaAI: {response}\n\n")

    return jsonify({"response": response})


# Password-protected chat history view
@app.route("/history", methods=["GET", "POST"])
def history():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "sadia123":  # change this password if needed
            try:
                with open("chat_history.txt", "r", encoding="utf-8") as file:
                    content = file.read().replace("\n", "<br>")
            except FileNotFoundError:
                content = "No chats saved yet."

            html = f"""
                <h2>Chat History</h2>
                <div style='padding:10px;border:1px solid #ccc;margin-bottom:20px;'>{content}</div>
                <form action="/clear-history" method="post">
                    <input type="password" name="password" placeholder="Enter admin password" required>
                    <button type="submit">Clear Chat History</button>
                </form>
            """
            return html
        else:
            return "<h3>Wrong password!</h3><a href='/history'>Try again</a>"

    return """
        <h2>Admin Login - Chat History</h2>
        <form method="post">
            <input type="password" name="password" placeholder="Enter admin password" required>
            <button type="submit">View Chat History</button>
        </form>
    """


# Password-protected chat history clear
@app.route("/clear-history", methods=["POST"])
def clear_history():
    password = request.form.get("password")
    if password == "sadia123":
        open("chat_history.txt", "w").close()
        return "<h3>Chat history cleared!</h3><a href='/history'>Go back</a>"
    else:
        return "<h3>Wrong password!</h3><a href='/history'>Try again</a>"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)


