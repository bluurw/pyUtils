import asyncio
from aiogram import Bot, Dispatcher

TOKEN_BOT = "TOKEN"
USER_ID = 123 # ID USER/GROUP TELEGRAM

bot = Bot(bot=TOKEN)
dp = Dispatcher()

async def send_msg():
    while True:
        msg = "Personalized msg"
        await bot.send_msg(USER_ID, msg)
        await asyncio.sleep(60)

async def main():
    asyncio.create_task(send_msg())
    await dp.start_polling(bot)

asyncio.run(main())