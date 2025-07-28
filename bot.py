import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import routers

load_dotenv()

bot = Bot(token=os.getenv("BOT_API_KEY"))
dp = Dispatcher()


async def main():
    for r in routers:
        dp.include_router(r)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
