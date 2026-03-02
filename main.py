from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
import aiohttp
from config import BOT_TOKEN, COINGECKO_API
import asyncio
import logging

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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
    await message.answer('Привет, я бот-учебный проект, созданный непонятно зачем. Используй команду "/help", чтобы увидеть список доступных команд.')

@dp.message(Command('help'))
async def cmd_help(message: Message):
    help_text = '''
    Список доступных команд:
    *    /start - Начать работу
    *    /help - Показать это сообщение
    *    /whoami - Информация о пользователе
    *    /price_btc - Курс биткоина
Иные возможности:
    *    Напишите "Хочу котика", чтобы получить случайное фото котика
    '''
    await message.answer(help_text)

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
    await message.answer(f'1 биткоин стоит {price_data['bitcoin']['usd']}$')

async def get_info_price_btc(message: Message, session: aiohttp.ClientSession):
    try:
        async with session.get(
            f'https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin&names=Bitcoin&symbols=btc?x_cg_demo_api_key={COINGECKO_API}') as response:
                return await response.json()
    except Exception as e:
        print(f'Сервер недоступен. Ошибка: {e}')
        await message.answer('Извините, сервис временно недоступен')

@dp.message(F.text.lower() == 'хочу котика')
async def print_cat(message: Message, session: aiohttp.ClientSession):
    cat_image = await get_cat(message, session)
    photo = cat_image[0]['url']
    await message.answer_photo(photo)

async def get_cat(message: Message, session: aiohttp.ClientSession):
    try:
        async with session.get(
            'https://api.thecatapi.com/v1/images/search') as response:
                return await response.json()
    except Exception as e:
        print(f'Сервер недоступен. Ошибка: {e}')
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