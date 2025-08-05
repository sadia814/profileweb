document.getElementById("open-chat").addEventListener("click", () => {
  document.getElementById("chatbox").classList.remove("hidden");
});

// Enable sending message with Enter key
document
  .getElementById("userInput")
  .addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  });

function appendMessage(sender, message) {
  const chatlog = document.getElementById("chatlog");
  const messageBubble = document.createElement("div");
  messageBubble.className = `chat-bubble ${sender}`;
  const time = new Date().toLocaleTimeString();
  messageBubble.textContent = `${sender === "bot" ? "sadiaAI" : "You"} (${time}): ${message}`;
  chatlog.appendChild(messageBubble);
  chatlog.scrollTop = chatlog.scrollHeight;
}

function sendMessage() {
  const inputField = document.getElementById("userInput");
  const userInput = inputField.value.trim();
  if (!userInput) return;

  appendMessage("user", userInput);
  inputField.value = "";

  fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userInput }),
  })
    .then((response) => response.json())
    .then((data) => {
      const botResponse = data.response || "Sorry, I didn't understand that.";
      appendMessage("bot", botResponse);
    })
    .catch(() => {
      appendMessage(
        "bot",
        "Sorry, the server is not responding. Try again later.",
      );
    });
}

