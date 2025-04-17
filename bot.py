import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.utils.executor import start_webhook
import os

API_TOKEN = os.getenv("TOKEN")
CRYPTOBOT_URL = os.getenv("CRYPTOBOT_URL")
CHANNEL_INVITE_LINK = os.getenv("CHANNEL_INVITE_LINK")

WEBHOOK_HOST = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}"
WEBHOOK_PATH = f"/webhook/{API_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", default=8000))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    pay_btn = types.InlineKeyboardButton("Оплатить", url=CRYPTOBOT_URL)
    keyboard.add(pay_btn)
    await message.answer("Добро пожаловать! Чтобы получить доступ к каналу, оплатите подписку.", reply_markup=keyboard)

@dp.message_handler(lambda message: "Спасибо за оплату" in message.text)
async def send_invite(message: types.Message):
    await message.answer(f"Спасибо за оплату! Вот ваша ссылка в канал: {CHANNEL_INVITE_LINK}")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await bot.delete_webhook()

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
