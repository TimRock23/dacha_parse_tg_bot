import asyncio
import logging
import os
import random
import sys

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

from db import (add_user, add_user_category, delete_user_category,
                get_all_categories, get_user_categories,
                get_users_by_category_name, is_user_exists)
from utils import get_all_events, get_category_keyboard, is_event_old
import settings

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help', 'info'])
async def start(message: types.Message):
    """Add user to DB if not exists, send info message."""
    if not is_user_exists(tg_id=message.from_user['id']):
        add_user(tg_id=message.from_user['id'],
                 username=message.from_user['username'])
    await message.answer(settings.START_MESSAGE)


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


@dp.message_handler(commands=['events'])
async def send_followed_events(message: types.Message):
    all_events = get_all_events()
    user_categories = get_user_categories(user_id=message.from_user['id'])
    for event in all_events:
        if event.category in user_categories:
            await message.answer(event.get_event_message())


@dp.message_handler(commands=['link'])
async def send_followed_events(message: types.Message):
    await message.answer(settings.URI)


async def parse_new_event_tickets():
    old_events = []
    while True:
        all_events = get_all_events()
        for event in all_events:
            is_new = True
            for old_event in old_events:
                if is_event_old(old_event, event):
                    is_new = False
                    if old_event.tickets < event.tickets:
                        users = get_users_by_category_name(
                            category=event.category
                        )
                        for user in users:
                            await bot.send_message(
                                user, text=event.get_new_tickets_message()
                            )
            if is_new:
                users = get_users_by_category_name(category=event.category)
                for user in users:
                    await bot.send_message(user,
                                           text=event.get_new_event_message())
        old_events = all_events
        await asyncio.sleep(random.randint(*settings.REQUEST_TIME_RANGE))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=(
            '%(asctime)s [%(levelname)s] - '
            '(%(filename)s).%(funcName)s:%(lineno)d - %(message)s'
        ),
        handlers=[
            logging.FileHandler(f'output.log', mode='a'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    loop = asyncio.get_event_loop()
    loop.create_task(parse_new_event_tickets())
    executor.start_polling(dp, skip_updates=True)
