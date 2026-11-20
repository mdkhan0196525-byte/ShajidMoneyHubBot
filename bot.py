import os
import json
import hmac
import hashlib
import time
import threading
import urllib.parse
import urllib.request

from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
GROUP = "@OnlineEarningAlltime4t4"

def verify_init_data(init_data):
    data = dict(urllib.parse.parse_qsl(init_data))
    received_hash = data.pop("hash", None)

    if not received_hash:
        return None

    check_string = "\n".join(
        f"{key}={value}" for key, value in sorted(data.items())
    )

    secret = hmac.new(
        b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256
    ).digest()

    calculated_hash = hmac.new(
        secret, check_string.encode(), hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        return None

    try:
        auth_date = int(data["auth_date"])
        if time.time() - auth_date > 86400:
            return None
        user = json.loads(data["user"])
        return user["id"]
    except (KeyError, ValueError, TypeError):
        return None


def check_membership(user_id):
    url = (
        f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
        f"?chat_id={urllib.parse.quote(GROUP)}&user_id={user_id}"
    )

    with urllib.request.urlopen(url, timeout=15) as response:
        result = json.loads(response.read())

    if not result.get("ok"):
        return False

    member = result["result"]
    status = member.get("status")

    return (
        status in ("creator", "administrator", "member")
        or (status == "restricted" and member.get("is_member"))
    )


class HealthCheck(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin",
                         "https://mdkhan0196525-byte.github.io")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_json(200, {"ok": True})

    def do_GET(self):
        self.send_json(200, {"ok": True, "message": "Bot is running"})

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path != "/verify":
            self.send_json(404, {"ok": False})
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            if length > 10000:
                self.send_json(413, {"ok": False})
                return

            body = json.loads(self.rfile.read(length))
            init_data = body.get("initData", "")
            user_id = verify_init_data(init_data)

            if not user_id:
                self.send_json(401, {
                    "ok": False,
                    "message": "Invalid Telegram session"
                })
                return

            joined = check_membership(user_id)

            self.send_json(200, {
                "ok": True,
                "joined": joined
            })

        except Exception:
            self.send_json(500, {"ok": False})

    def log_message(self, format, *args):
        pass


def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), HealthCheck).serve_forever()


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

    await update.message.reply_text(
        "Welcome to Shajid Money Hub! 🎉\n\n"
        "আমাদের Online Earning Community-তে স্বাগতম!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


threading.Thread(target=run_server, daemon=True).start()

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
