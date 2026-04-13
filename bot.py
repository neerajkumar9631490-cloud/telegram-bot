import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# ====== LOAD API KEYS ======
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ====== SAFETY CHECK ======
if not TELEGRAM_BOT_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("API keys missing! Check Railway variables.")

# ====== USER MEMORY STORAGE ======
user_history = {}

# ====== OpenRouter Function ======
def ask_ai(user_id, prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Initialize user history if not exists
    if user_id not in user_history:
        user_history[user_id] = [
            {
                "role": "system",
                "content": "You are NGX AI, a helpful chatbot designed by NGX. Give clear, simple, and useful answers."
            }
        ]

    # Add user message
    user_history[user_id].append({
        "role": "user",
        "content": prompt
    })

    # Limit history (last 10 messages)
    user_history[user_id] = user_history[user_id][-10:]

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": user_history[user_id]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]

            # Save AI reply
            user_history[user_id].append({
                "role": "assistant",
                "content": reply
            })

            return reply
        else:
            return "⚠️ AI Error: Try again later."

    except Exception:
        return "⚠️ Server busy. Please try again."

# ====== START COMMAND ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to NGX AI Bot!\n\n"
        "Now I remember your conversation 🧠\nAsk me anything 🚀"
    )

# ====== MESSAGE HANDLER ======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.message.from_user.id
    user_message = update.message.text

    reply = ask_ai(user_id, user_message)

    await update.message.reply_text(reply)

# ====== MAIN FUNCTION ======
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()

# ====== RUN ======
if __name__ == "__main__":
    main()
# ====== MAIN FUNCTION ======
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()

# ====== RUN ======
if __name__ == "__main__":
    main()
