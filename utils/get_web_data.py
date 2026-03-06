from aiogram.types import Message
import aiohttp
import logging
from config import COINGECKO_API, WEATHER_API


async def get_info_price_btc(message: Message, session: aiohttp.ClientSession):
    try:
        async with session.get(
            f'https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin&names=Bitcoin&symbols=btc?x_cg_demo_api_key={COINGECKO_API}') as response:
            return await response.json()
    except Exception as e:
        logging.error(f'Ошибка: {e}')
        await message.answer('Извините, сервис временно недоступен')


async def get_weather(message: Message, session: aiohttp.ClientSession, city_name):
    try:
        async with session.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API}&lang=ru&units=metric') as response:
            return await response.json()
    except Exception as e:
        logging.error(f'Ошибка: {e}')
        await message.answer('Извините, сервис временно недоступен')


async def get_cat(message: Message, session: aiohttp.ClientSession):
    try:
        async with session.get(
            'https://api.thecatapi.com/v1/images/search') as response:
            return await response.json()
    except Exception as e:
        logging.error(f'Ошибка: {e}')
        await message.answer('Извините, сервис временно недоступен')