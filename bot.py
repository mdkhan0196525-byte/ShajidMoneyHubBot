import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes


class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheck)
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(
            "🚀 Open Mini App",
            web_app=WebAppInfo(
                url="https://mdkhan0196525-byte.github.io/shajid-money-hub/"
            )
        )],
        [InlineKeyboardButton(
            "👥 Join Telegram Group",
            url="https://t.me/OnlineEarningAlltime4t4"
        )]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to Shajid Money Hub! 🎉\n\n"
        "আমাদের Online Earning Community-তে স্বাগতম!\n\n"
        "নিচের বাটনে ক্লিক করো:",
        reply_markup=reply_markup
    )


threading.Thread(target=run_server, daemon=True).start()

app = Application.builder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
