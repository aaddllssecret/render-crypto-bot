
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")
CRYPTOBOT_URL = os.getenv("CRYPTOBOT_URL")
CHANNEL_INVITE_LINK = os.getenv("CHANNEL_INVITE_LINK")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User {update.effective_user.id} started bot")
    keyboard = [
        [InlineKeyboardButton("Оплатить через CryptoBot", url=CRYPTOBOT_URL)],
        [InlineKeyboardButton("Я оплатил", callback_data="confirm_payment")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать! Выберите способ оплаты:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    logger.info(f"Button pressed: {query.data} by user {query.from_user.id}")
    if query.data == "confirm_payment":
        await query.message.reply_text(f"Спасибо за оплату! Вот ваша ссылка в канал:
{CHANNEL_INVITE_LINK}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
