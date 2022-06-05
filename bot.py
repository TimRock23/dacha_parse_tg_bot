import logging
from dotenv import load_dotenv
import os
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from db import (add_user, is_user_exists, get_user_categories,
                get_all_users_ids, get_all_categories, add_user_category,
                delete_user_category)
from utils import get_category_keyboard, get_all_events

load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help', 'info'])
async def start(message: types.Message):
    """Add user to DB if not exists, send info message"""
    if not is_user_exists(tg_id=message.from_user['id']):
        add_user(tg_id=message.from_user['id'],
                 username=message.from_user['username'])

    await message.answer('Бот парсит [Яндекс Дачу]('
                         'https://plus.yandex.ru/dacha) '
                         'на предмет появления новых ивентов и билетов на '
                         'старые по выбранным категориям\n'
                         'Для выбора/изменения категорий введите "/category"',
                         parse_mode="MarkdownV2")


@dp.message_handler(commands=['category'])
async def choose_category(message: types.Message):
    keyboard = get_category_keyboard(user_id=message.from_user['id'])
    await message.answer('Выберите интересующие категории:',
                         reply_markup=keyboard)


@dp.message_handler(Text(endswith=' -'))
async def add_user_ctg(message: types.Message):
    category = message.text.split(' ')[0]
    user_id = message.from_user['id']
    if category not in get_all_categories():
        await message.answer('Введена несуществующая категория.')
        return
    if category in get_user_categories(user_id=user_id):
        await message.answer('Вы уже подписаны на эту категорию')
        return
    add_user_category(user_id=user_id, category=category)
    keyboard = get_category_keyboard(user_id)
    await message.answer(f'Вы подписались на категорию - {category}',
                         reply_markup=keyboard)


@dp.message_handler(Text(endswith=' +'))
async def delete_user_ctg(message: types.Message):
    category = message.text.split(' ')[0]
    user_id = message.from_user['id']
    if category not in get_all_categories():
        await message.answer('Введена несуществующая категория.')
        return
    if category not in get_user_categories(user_id=user_id):
        await message.answer('Вы не подписаны на эту категорию')
        return
    delete_user_category(user_id=user_id, category=category)
    keyboard = get_category_keyboard(user_id)
    await message.answer(f'Вы отписались от категории - {category}',
                         reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
