# Rehumy Telegram Bot (Webhook)

## 🛠 How to Deploy on Render.com (Free Plan)

1. Go to [https://render.com](https://render.com) & create an account
2. Click **New Web Service**
3. Connect your GitHub (or upload ZIP after pushing)
4. Use the following settings:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn rehumy:app`
5. After deployment, copy the Render URL (e.g. `https://rehumy.onrender.com`)
6. Set the webhook with this command:

```
curl -F "url=https://rehumy.onrender.com/$BOT_KEY" https://api.telegram.org/bot$BOT_KEY/setWebhook

```

Replace `https://your-url.onrender.com` with your actual Render app URL.
