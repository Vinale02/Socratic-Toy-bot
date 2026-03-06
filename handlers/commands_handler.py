from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
import aiohttp
from utils.get_web_data import get_info_price_btc, get_weather
from config import city
from states.states import RegistrationProfile
from utils.file_handler import write_to_file, get_user_from_file

router = Router()

@router.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Действие отменено')

@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    kb = [[KeyboardButton(text='/help')]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    user = get_user_from_file('data/users.json',message.from_user.id)
    if user:
        await message.answer(f'Привет, {user['name']}\nИспользуй команду "/help", чтобы увидеть список доступных команд.')
    else:
        await message.answer('Привет! Давай зарегистрируемся. \n\nШаг 1 из 3: Как тебя зовут? Отменить /cancel', reply_markup=keyboard)
        await state.set_state(RegistrationProfile.waiting_name)


@router.message(RegistrationProfile.waiting_name)
async def cmd_waiting_name(message: Message, state: FSMContext):
    await message.answer(f'Приятно познакомиться {message.text}')
    await state.update_data(id=message.from_user.id)
    await state.update_data(name=message.text)
    await message.answer('Шаг 2 из 3: Сколько тебе лет? Отменить /cancel')
    await state.set_state(RegistrationProfile.waiting_age)


@router.message(RegistrationProfile.waiting_age)
async def cmd_waiting_age(message: Message, state: FSMContext):
    await message.answer(f'Ого тебе {message.text} лет!')
    await state.update_data(age=message.text)
    await message.answer('Шаг 3 из 3: Откуда ты? Отменить /cancel')
    await state.set_state(RegistrationProfile.waiting_city)


@router.message(RegistrationProfile.waiting_city)
async def cmd_waiting_name(message: Message, state: FSMContext):
    await message.answer(f'{message.text} - отличное место!')
    await state.update_data(city=message.text)
    data = await state.get_data()
    await message.answer(f'Регистрация успешно пройдена! Вот твои данные:\nИмя: {data['name']}\nВозраст: {data['age']}\nГород: {data['city']}\nИспользуй команду "/help", чтобы увидеть список доступных команд.')
    write_to_file('data/users.json', data)
    await state.clear()


@router.message(Command('help'))
async def cmd_help(message: Message):
    help_text = '''
    Список доступных команд:
    *    /start - Начать работу
    *    /help - Показать это сообщение
    *    /about - О нас 
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
        ],
        [
            KeyboardButton(text='/about')
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer(help_text, reply_markup=keyboard)


@router.message(Command('about'))
async def cmd_about(message: Message):
    start_text = '''
    Я бот-учебный проект, созданный непонятно зачем. Используй команду "/help", чтобы увидеть список доступных команд.'''
    await message.answer(start_text)


@router.message(Command('whoami'))
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

@router.message(Command('price_btc'))
async def cmd_price_btc(message: Message, session: aiohttp.ClientSession):
    price_data = await get_info_price_btc(message, session)
    if price_data:
        await message.answer(f'1 BTC: {price_data['bitcoin']['usd']}$')

@router.message(Command('weather'))
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
