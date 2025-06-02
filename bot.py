import os
import json
import datetime
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Загрузка календаря из JSON-файла
with open("gp_calendar.json", "r") as f:
    CALENDAR = json.load(f)

def get_next_gp():
    today = datetime.date.today()
    for gp in CALENDAR:
        gp_date = datetime.date.fromisoformat(gp["date"])
        if gp_date >= today:
            return gp
    return None

@dp.message(Command("start"))
async def start(message: Message):
    logging.info(f"/start by {message.from_user.full_name} ({message.from_user.id})")
    await message.answer(
        "🏁 Привет! Я RaceHub Bot. Вот что я умею:\n\n"
        "/next — следующий Гран-при\n"
        "/calendar — весь календарь сезона"
    )

@dp.message(Command("next"))
async def next_gp(message: Message):
    logging.info(f"/next by {message.from_user.full_name} ({message.from_user.id})")
    gp = get_next_gp()
    if gp:
        await message.answer(
            f"🚥 Следующий Гран-при:\n<b>{gp['name']}</b>\n📍 {gp['location']}\n📅 {gp['date']}"
        )
    else:
        await message.answer("Все гонки сезона уже завершены! 🎉")

@dp.message(Command("calendar"))
async def calendar(message: Message):
    logging.info(f"/calendar by {message.from_user.full_name} ({message.from_user.id})")
    text = "📆 <b>Календарь Гран-при 2025:</b>\n\n"
    for gp in CALENDAR:
        text += f"• <b>{gp['name']}</b> — {gp['date']}\n"
    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
