import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheck)
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Shajid Money Hub! 🎉\n\n"
        "আমাদের Online Earning Community-তে স্বাগতম!\n\n"
        "গ্রুপে যোগ দিতে নিচের লিংকে যাও:\n"
        "https://t.me/OnlineEarningAlltime4t4"
    )

threading.Thread(target=run_server, daemon=True).start()

app = Application.builder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
