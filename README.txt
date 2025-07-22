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
curl -F "url=https://your-url.onrender.com/7636482341:AAFn7ARpEH7J3ORhm8ctCUMSMS8i9aswbBg" https://api.telegram.org/bot7636482341:AAFn7ARpEH7J3ORhm8ctCUMSMS8i9aswbBg/setWebhook
```

Replace `https://your-url.onrender.com` with your actual Render app URL.
