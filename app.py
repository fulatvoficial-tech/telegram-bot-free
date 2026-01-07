import os
import threading
import logging
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot online 🚀"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("👉 /start recebido")
    await update.message.reply_text("✅ Bot respondeu ao /start!")

def start_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    print("🚀 Iniciando Flask + Bot")

    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()

    app.run(host="0.0.0.0", port=8080)
