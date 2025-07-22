from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from together import Together
import os
import re
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
# Static files mounting commented out because no static directory needed
# app.mount("/static", StaticFiles(directory="static"), name="static")

API_KEY = os.getenv("API_KEY")
client = Together(api_key=API_KEY)

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

html_page = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Text Humanizer</title>
    <style>
        body {{
            background: #eaf4fc;
            font-family: Arial, sans-serif;
            padding: 40px;
            color: #333;
        }}
        h1 {{
            text-align: center;
            color: #1976d2;
        }}
        form {{
            max-width: 700px;
            margin: auto;
            padding: 20px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        textarea {{
            width: 100%;
            height: 200px;
            padding: 10px;
            font-size: 16px;
            border-radius: 6px;
            border: 1px solid #ccc;
            resize: vertical;
        }}
        button {{
            background: #1976d2;
            color: #fff;
            border: none;
            padding: 12px 20px;
            font-size: 16px;
            border-radius: 6px;
            cursor: pointer;
        }}
        .result {{
            max-width: 700px;
            margin: 30px auto;
            background: #f0f8ff;
            padding: 20px;
            border-radius: 6px;
            white-space: pre-wrap;
            line-height: 1.6em;
        }}
    </style>
</head>
<body>
    <h1>Humanize Your AI Text</h1>
    <form action="/rewrite" method="post">
        <p><strong>Paste your AI-generated text (between 100 and 500 words):</strong></p>
        <textarea name="user_input" placeholder="Paste your text here..."></textarea><br><br>
        <button type="submit">Rewrite Text</button>
    </form>
    {result}
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def homepage():
    # No dynamic content on homepage
    return html_page.format(result="")

@app.post("/rewrite", response_class=HTMLResponse)
async def rewrite_text(user_input: str = Form(...)):
    word_count = len(re.findall(r'\b\w+\b', user_input))

    if word_count < 100:
        message = "<div class='result'>❗ Please provide more than 100 words (up to 500).</div>"
        return html_page.format(result=message)

    if word_count > 500:
        message = "<div class='result'>❗ Your text exceeds 500 words. Please shorten it.</div>"
        return html_page.format(result=message)

    try:
        response = client.chat.completions.create(
            model="lgai/exaone-deep-32b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        rewritten = response.choices[0].message.content.strip()
        message = f"<div class='result'><strong>Rewritten Text:</strong><br><br>{rewritten}</div>"
        return html_page.format(result=message)

    except Exception as e:
        error_message = f"<div class='result'>⚠️ Error while rewriting: {e}</div>"
        return html_page.format(result=error_message)
