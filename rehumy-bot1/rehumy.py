from flask import Flask, request
import requests

app = Flask(__name__)
TOKEN = "7636482341:AAFn7ARpEH7J3ORhm8ctCUMSMS8i9aswbBg"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route('/')
def index():
    return "Rehumy Bot is Live"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        requests.post(TELEGRAM_API_URL, data={
            "chat_id": chat_id,
            "text": f"You said: {text}"
        })
    return {"ok": True}

if __name__ == "__main__":
    app.run()
