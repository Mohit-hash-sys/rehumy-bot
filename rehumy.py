import os
import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from together import Together

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Keys (HIDE YOUR KEY IN ENV ON RENDER)
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
TOGETHER_API_KEY = os.getenv("API_KEY")

# Setup Together client
client = Together(api_key=TOGETHER_API_KEY)

# System prompt for rewriting
SYSTEM_PROMPT = """
You are a rewriting engine.  When you transform any input text, obey these rules exactly:

Rewrite each and every sentence into simple form from the given text use loose grammar sentence structure.

2. Sentence mechanics:
• Remove all commas STRICTLY, from the paragraphs, instead, use Indian-style conjunctions like 'as', 'so', 'since', 'but also', 'not only but also', 'along with', 'such as', 'or else', etc.
• Each sentence must have at least seven words.
• Write only in different paragraph form (no lists or bullets).
write sentences into very clear and simple english with no hard words.
• Allow inconsistent tone and natural rhythm—vary sentence length and cadence.
• use simple, clear and  very easy vocabulary always.

3. Prohibitions (strict—no exceptions):
• never Use vague words and vague phrases.
• No complex sentences.
• No native-English style or idioms.
• No tight/academic grammar or balanced clauses.
• No informal or slang words (e.g. “gonna,” “cool,” “wanna”).

Preserve Paragraph Count:
If the user gives 2 paragraphs, return 2 paragraphs. Keep paragraph breaks in the same position as in the input.

Don't Add or Remove Ideas:
Stick to the original meaning. Don’t add new points or remove anything the user included, just write in very simple english with good vocam. but keep english simple, easy and correct.
"""

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! Please paste your AI-generated text (between 100 and 500 words) to rewrite it into simple English. Make sure it's clean and under the limit!"
    )

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Paste any AI-generated text (100–500 words) and I’ll simplify it. Just send the message directly. Nothing else is needed!"
    )

# Handle user messages
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    word_count = len(re.findall(r'\b\w+\b', text))

    if word_count < 100:
        await update.message.reply_text("❗ Please provide more than 100 words (up to 500).")
        return
    if word_count > 500:
        await update.message.reply_text("❗ Your text exceeds 500 words. Please shorten it.")
        return

    await update.message.reply_text("⏳ Rewriting your text... Please wait...")

    try:
        response = client.chat.completions.create(
            model="lgai/exaone-deep-32b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ]
        )
        rewritten = response.choices[0].message.content.strip()
        await update.message.reply_text(rewritten)

    except Exception as e:
        logger.error(f"API error: {e}")
        await update.message.reply_text("⚠️ Something went wrong while rewriting. Try again later.")

# Main function
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
