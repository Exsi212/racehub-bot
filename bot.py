from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
import asyncio
import datetime
import json
import os  # добавлено

BOT_TOKEN = os.getenv("BOT_TOKEN")  # изменено

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Календарь в json-формате
with open("gp_calendar.json", "r") as f:
    CALENDAR = json.load(f)

def get_next_gp():
    today = datetime.date.today()
    for gp in CALENDAR:
        gp_date = datetime.date.fromisoformat(gp["date"])
        if gp_date >= today:
            return gp
    return None

@dp.message(commands=["start"])
async def start(message: types.Message):
    await message.answer("🏁 Привет! Я RaceHub Bot. Вот что я умею:\n\n/next — следующий Гран-при\n/calendar — весь календарь сезона")

@dp.message(commands=["next"])
async def next_gp(message: types.Message):
    gp = get_next_gp()
    if gp:
        await message.answer(f"🚥 Следующий Гран-при:\n<b>{gp['name']}</b>\n📍 {gp['location']}\n📅 {gp['date']}")
    else:
        await message.answer("Все гонки сезона уже завершены! 🎉")

@dp.message(commands=["calendar"])
async def calendar(message: types.Message):
    text = "📆 <b>Календарь Гран-при 2025:</b>\n\n"
    for gp in CALENDAR:
        text += f"• <b>{gp['name']}</b> — {gp['date']}\n"
    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
