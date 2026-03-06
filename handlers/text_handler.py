from aiogram import Router, Bot, F
from aiogram.types import Message
import aiohttp
from utils.get_web_data import get_cat

router = Router()


@router.message(F.text.lower().contains('хочу котика'))
async def print_cat(message: Message, session: aiohttp.ClientSession):
    cat_image = await get_cat(message, session)
    if cat_image:
        photo = cat_image[0]['url']
        await message.answer_photo(photo)


@router.message(F.text.lower() == 'привет')
async def send_greeting(message: Message):
        await message.answer('О, здарова! Это я, Женя Пригожин!')


@router.message(F.text.contains('помощь'))
async def handle_help_word(message: Message, bot: Bot):
    user = message.from_user
    await bot.send_message(chat_id=673364458, text=f'У @{user.username} возникла проблема')


@router.message(F.text)
async def eho_text(message: Message):
        await message.answer(f'Ты сказал {message.text}')