from flask import Flask, request
import requests
import os

BOT_TOKEN = os.getenv("BOT_KEY")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)

def send_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    requests.post(f"{URL}/sendMessage", data=data)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.lower() == "/start":
            send_message(chat_id, "👋 Welcome! I'm your Rehumy Bot. How can I help you?")
        else:
            send_message(chat_id, f"You said: {text}")
    return "ok"


