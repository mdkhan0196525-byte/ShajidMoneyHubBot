import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Shajid Money Hub! 🎉\n\n"
        "আমাদের Online Earning Community-তে স্বাগতম!\n\n"
        "গ্রুপে যোগ দিতে নিচের লিংকে যাও:\n"
        "https://t.me/OnlineEarningAlltime4t4"
    )

app = Application.builder().token(
    os.environ["BOT_TOKEN"]
).build()

app.add_handler(CommandHandler("start", start))
app.run_polling()
