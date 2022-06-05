import logging
from dotenv import load_dotenv
import os
import time

from aiogram import Bot, Dispatcher, executor, types

from db import (add_user, is_user_exists, get_user_categories,
                get_all_categories)

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
async def category(message: types.Message):
    user_categories = get_user_categories(user_id=message.from_user['id'])
    all_categories = get_all_categories()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for i, cat in enumerate(all_categories):
        if cat in user_categories:
            buttons.append(cat[0] + ' +')
        else:
            buttons.append(cat[0] + ' -')
        if i % 2 == 1 or i == len(all_categories) - 1:
            keyboard.add(*buttons)
            buttons = []
    await message.answer('Выберите интересующие категории:',
                         reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
