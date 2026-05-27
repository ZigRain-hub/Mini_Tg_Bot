from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8794735228:AAHI77zmR-IIm7JeP6-zuyDhz9QzM_rWdWk"
ADMIN_ID = 8226208121

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
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bug))
    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
