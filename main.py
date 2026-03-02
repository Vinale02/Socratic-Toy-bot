from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
import aiohttp
from config import BOT_TOKEN, COINGECKO_API, WEATHER_API
import asyncio
import logging

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

city = 'Минск'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s %(message)s')

@dp.startup()
async def on_startup():
    session = aiohttp.ClientSession()
    dp['session'] = session
    print('Сессия создана')

@dp.shutdown()
async def on_shutdown():
    session = dp.get('session')
    if session:
        await session.close()
        print('Сессия закрыта')

@dp.message(Command('start'))
async def cmd_start(message: Message):
    kb = [[KeyboardButton(text='/help')]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    await message.answer('Привет, я бот-учебный проект, созданный непонятно зачем. Используй команду "/help", чтобы увидеть список доступных команд.', reply_markup=keyboard)

@dp.message(Command('help'))
async def cmd_help(message: Message):
    help_text = '''
    Список доступных команд:
    *    /start - Начать работу
    *    /help - Показать это сообщение
    *    /whoami - Информация о пользователе
    *    /price_btc - Курс биткоина
    *    /weather - Погода 
Иные возможности:
    *    Напишите "Хочу котика", чтобы получить случайное фото котика
    '''
    kb = [
        [
            KeyboardButton(text='/start'),
            KeyboardButton(text='/help')
        ],
        [
            KeyboardButton(text='/whoami'),
            KeyboardButton(text='/price_btc')
        ],
        [
            KeyboardButton(text='/weather'),
            KeyboardButton(text='Хочу котика')
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer(help_text, reply_markup=keyboard)

@dp.message(Command('whoami'))
async def cmd_whoami(message: Message):
    user = message.from_user

    info = (
        f'Твой ID: {user.id}',
        f'Имя: {user.first_name or 'Не указано'}',
        f'Фамилия: {user.last_name or 'Не указано'}',
        f'Username: {user.username}',
        f'ID чата: {message.chat.id}',
        f'Тип чата: {message.chat.type}'
    )
    await message.answer('\n'.join(info))

@dp.message(Command('price_btc'))
async def cmd_price_btc(message: Message, session: aiohttp.ClientSession):
    price_data = await get_info_price_btc(message, session)
    if price_data:
        await message.answer(f'1 BTC: {price_data['bitcoin']['usd']}$')

async def get_info_price_btc(message: Message, session: aiohttp.ClientSession):
    try:
        async with session.get(
            f'https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin&names=Bitcoin&symbols=btc?x_cg_demo_api_key={COINGECKO_API}') as response:
            return await response.json()

    except Exception as e:
        logging.error(f'Ошибка: {e}')
        await message.answer('Извините, сервис временно недоступен')

@dp.message(Command('weather'))
async def cmd_weather(message: Message, session: aiohttp.ClientSession):
    weather_data = await get_weather(message, session, city)
    if weather_data:
        weather_info = (
            f'Текущая погода в {city}: {weather_data['weather'][0]['description']}',
            f'Температура: {weather_data['main']['temp']}°C',
            f'Ощущается как: {weather_data['main']['feels_like']}°C',
            f'Влажность: {weather_data['main']['humidity']}%',
            f'Скорость ветра: {int(weather_data['wind']['speed'] * 3.6):.1f} км/ч'
        )
        await message.answer('\n'.join(weather_info))

async def get_weather(message: Message, session: aiohttp.ClientSession, city_name):
    try:
        async with session.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API}&lang=ru&units=metric') as response:
            return await response.json()

    except Exception as e:
        logging.error(f'Ошибка: {e}')
        await message.answer('Извините, сервис временно недоступен')

@dp.message(F.text.lower() == 'хочу котика')
async def print_cat(message: Message, session: aiohttp.ClientSession):
    cat_image = await get_cat(message, session)
    if cat_image:
        photo = cat_image[0]['url']
        await message.answer_photo(photo)

async def get_cat(message: Message, session: aiohttp.ClientSession):
    try:
        async with session.get(
            'https://api.thecatapi.com/v1/images/search') as response:
            return await response.json()

    except Exception as e:
        logging.error(f'Ошибка: {e}')
        await message.answer('Извините, сервис временно недоступен')

@dp.message(F.text.lower() == 'привет')
async def send_greeting(message: Message):
        await message.answer('О, здарова! Это я, Женя Пригожин!')

@dp.message(F.text.contains('помощь'))
async def handle_help_word(message: Message):
    user = message.from_user
    await bot.send_message(chat_id=673364458, text=f'У @{user.username} возникла проблема')

@dp.message(F.text)
async def eho_text(message: Message):
        await message.answer(f'Ты сказал {message.text}')



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())