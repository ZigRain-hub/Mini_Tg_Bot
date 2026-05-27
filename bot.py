from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread
import os

TOKEN = "8794735228:AAHI77zmR-IIm7JeP6-zuyDhz9QzM_rWdWk"
ADMIN_ID = 8226208121

# --- Веб-сервер для Render (чтобы не падал по таймауту) ---
app_flask = Flask(__name__)

@app_flask.route('/')
def health_check():
    return "Bot is running!"

def run_web_server():
    port = int(os.environ.get('PORT', 10000))
    app_flask.run(host='0.0.0.0', port=port)

# --- Твой Telegram бот ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Привет! Нашёл баг в игре? Просто напиши сюда подробности."
    )

async def handle_bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    msg = f"🐛 Баг от @{user.username or 'нет_ника'}\nID: {user.id}\n\n{text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
    await update.message.reply_text("✅ Отправлено! Спасибо.")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bug))
    print("🤖 Бот запущен!")
    application.run_polling()

if __name__ == "__main__":
    # Запускаем веб-сервер в отдельном потоке
    web_thread = Thread(target=run_web_server)
    web_thread.start()
    # Запускаем бота
    main()

