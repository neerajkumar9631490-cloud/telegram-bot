import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

# ====== KEYS ======
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not TELEGRAM_BOT_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("Missing API keys")

# ====== MEMORY ======
user_history = {}

# ====== AI FUNCTION ======
def ask_ai(user_id, prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    if user_id not in user_history:
        user_history[user_id] = [
            {
                "role": "system",
                "content": "You are NGX AI. Reply in clean Telegram Markdown with bullet points only."
            }
        ]

    user_history[user_id].append({"role": "user", "content": prompt})
    user_history[user_id] = user_history[user_id][-12:]

    data = {
        "model": "openai/gpt-oss-120b:free",
        "messages": user_history[user_id]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        reply = response.json()["choices"][0]["message"]["content"]

        user_history[user_id].append({"role": "assistant", "content": reply})

        return reply

    except:
        return "⚠️ AI error. Try again later."

# ====== MENU BUTTON ======
def get_menu():
    keyboard = [
        [InlineKeyboardButton("🤖 Ask AI", callback_data="ask_ai")],
        [InlineKeyboardButton("🧠 Clear Memory", callback_data="clear_memory")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== START ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Welcome to NGX AI Bot!*\n\nTap below to continue 👇",
        parse_mode="Markdown",
        reply_markup=get_menu()
    )

# ====== MENU COMMAND ======
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 *Main Menu*",
        parse_mode="Markdown",
        reply_markup=get_menu()
    )

# ====== CALLBACK HANDLER ======
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # 🤖 Ask AI
    if query.data == "ask_ai":
        await query.message.reply_text("✍️ Send me your question now.")

    # 🧠 Clear memory
    elif query.data == "clear_memory":
        user_history[user_id] = []
        await query.message.reply_text("🧠 Memory cleared!")

    # ℹ️ Help
    elif query.data == "help":
        await query.message.reply_text(
            "ℹ️ *Help Menu*\n\n"
            "• Use Ask AI to chat 🤖\n"
            "• Use Clear Memory to reset chat 🧠\n"
            "• Just type message to talk directly",
            parse_mode="Markdown"
        )

# ====== MESSAGE HANDLER ======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.message.from_user.id
    user_message = update.message.text

    wait = await update.message.reply_text("⏳ Thinking...")

    reply = ask_ai(user_id, user_message)

    try:
        await context.bot.delete_message(update.effective_chat.id, wait.message_id)
    except:
        pass

    await update.message.reply_text(reply, parse_mode="Markdown")

# ====== MAIN ======
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ NGX AI Bot running with menu...")
    app.run_polling()

# ====== RUN ======
if __name__ == "__main__":
    main()        "role": "user",
        "content": prompt
    })

    # Limit history (last 10 messages)
    user_history[user_id] = user_history[user_id][-10:]

    data = {
        "model": "openai/gpt-oss-120b:free",
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

    # 👇 Send waiting message
    wait_msg = await update.message.reply_text("Ngx is thinking...")

    # Get AI reply
    reply = ask_ai(user_id, user_message)

    # 👇 Delete waiting message
    try:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=wait_msg.message_id
        )
    except:
        pass  # ignore if can't delete

    # 👇 Send final reply
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
