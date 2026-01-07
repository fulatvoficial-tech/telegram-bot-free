import os
import sqlite3
import threading
from flask import Flask
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# =========================
# CONFIGURAÇÕES
# =========================
BOT_TOKEN = "8563258420:AAFf-wMvt9KDbWkCxWr5HekE2EsS3pspJpE"
GRUPO_PRIVADO_LINK = "https://t.me/+kirwhn-Ctiw2Yjcx"
LINK_COMPARTILHAR = "https://t.me/share/url?url=https://t.me/+kirwhn-Ctiw2Yjcx&text=🔥%20Olha%20isso..."

MAX_COMPARTILHAMENTOS = 5
DB_NAME = "users.db"

# =========================
# FLASK (KEEP ALIVE)
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot VIP rodando 🚀"

# =========================
# DATABASE
# =========================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def get_count(user_id: int) -> int:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT count FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

def increment_count(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (user_id, count)
        VALUES (?, 1)
        ON CONFLICT(user_id) DO UPDATE SET count = count + 1
    """, (user_id,))
    conn.commit()
    conn.close()

# =========================
# BOT HANDLERS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔗 Compartilhar convite", url=LINK_COMPARTILHAR)],
        [InlineKeyboardButton("✅ Já compartilhei", callback_data="shared")]
    ]

    text = (
        "🔥 Gostou do que viu, meu amor?\n\n"
        "Antes de entrar, preciso que você compartilhe esse convite 💋\n"
        "São só *5 vezes*… depois eu libero tudo pra você.\n\n"
        "👇 Clica abaixo:"
    )

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def shared(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    increment_count(user_id)
    count = get_count(user_id)

    if count < MAX_COMPARTILHAMENTOS:
        mensagens = {
            1: "Ainda falta um pouquinho… 😘",
            2: "Tá ficando quente agora… 🔥",
            3: "Só mais um pouco, meu amor… 💋",
            4: "Último passo… eu prometo 😈"
        }
        await query.edit_message_text(
            mensagens.get(count, "Continua…"),
            reply_markup=query.message.reply_markup
        )
    else:
        keyboard = [
            [InlineKeyboardButton("🔓 Acessar grupo VIP", url=GRUPO_PRIVADO_LINK)]
        ]
        await query.edit_message_text(
            "🔥 Prontinho…\n"
            "Você mereceu.\n\n"
            "Clica abaixo e entra no grupo VIP 💋",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# =========================
# BOT START
# =========================
def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(shared, pattern="shared"))
    application.run_polling()

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    init_db()

    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
