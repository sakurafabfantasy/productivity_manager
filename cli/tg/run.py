import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.settings import TOKEN
from database.connection import async_main
from cli.tg.cards.cards_handlers import router as cards_router
from cli.tg.tasks.tasks_handlers import router as tasks_router
from cli.tg.common.handlers import router as base_router


async def main():
    await async_main()
    bot = Bot(token=str(TOKEN))
    dp = Dispatcher()
    dp.include_routers(cards_router, tasks_router, base_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")
