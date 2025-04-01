import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

TOKEN_BOT = "TOKEN"
USER_ID = 123 # ID USER/GROUP TELEGRAM

bot = Bot(bot=TOKEN)
dp = Dispatcher()

@dp.message(Command("send"))
async def send_msg(message: Message):
    msg = "Automatic Mensage"
    await bot.send_msg(USER_ID, msg)

    await message.answer("send confirmed")

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
