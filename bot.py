import os
import asyncio
from threading import Thread
from flask import Flask
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем переменные из .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# --- Flask приложение для Render ---
flask_app = Flask(__name__)

@flask_app.route('/')
def health_check():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    flask_app.run(host='0.0.0.0', port=port)

# --- Команды бота ---
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

# --- Запуск бота ---
def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bug))
    print("🤖 Бот запущен и слушает сообщения...")
    app.run_polling()

if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    # Запускаем бота в основном потоке
    run_bot()
