import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.settings import TOKEN
from database.connection import async_main
from cli.tg.handlers import router


async def main():
    await async_main()
    bot = Bot(token=str(TOKEN))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")
