from aiogram import Bot, Dispatcher
import aiohttp
import asyncio
import logging
from handlers import router
from config import BOT_TOKEN


async def main():
    async with aiohttp.ClientSession() as session:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s %(message)s')
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot, session=session)


if __name__ == '__main__':
    asyncio.run(main())