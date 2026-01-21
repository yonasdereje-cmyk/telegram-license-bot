import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

# ===== SECURE CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("RESET_API_KEY")
RESET_API_URL = os.getenv("RESET_API_URL")

if not BOT_TOKEN or not API_KEY or not RESET_API_URL:
    raise RuntimeError("Missing environment variables")

# ===== ADMIN =====
ADMIN_ID = 6153240508

# ===== MASTER LICENSE =====
MASTER_LICENSE_KEY = "HG-ZNENJY"

# ===== ALLOWED USERS =====
ALLOWED_USERS = [
    6153240508,
    6739116372,
    7832566226,
]

async def reset_license(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    telegram_id = user.id
    username = user.username or "NoUsername"

    user_input = update.message.text.strip()

    if user_input != MASTER_LICENSE_KEY:
        await update.message.reply_text(
            "❌ License key is incorrect."
        )
        return

    is_allowed = telegram_id in ALLOWED_USERS

    admin_message = (
        "🔔 RESET ATTEMPT\n"
        f"User: @{username}\n"
        f"Telegram ID: {telegram_id}\n"
        f"Allowed: {'YES' if is_allowed else 'NO'}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_message
    )

    if not is_allowed:
        await update.message.reply_text(
            "❌ You are not authorized to use this reset."
        )
        return

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }

    payload = {"username": MASTER_LICENSE_KEY}

    try:
        r = requests.post(RESET_API_URL, json=payload, headers=headers)

        if r.status_code == 200:
            await update.message.reply_text(
                "✅ Device reset successful."
            )
        else:
            await update.message.reply_text(
                "❌ Reset failed. Contact support."
            )

    except Exception:
        await update.message.reply_text(
            "⚠️ Server error."
        )






# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔑 Send your license key to reset your device."
    )



def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reset_license))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
