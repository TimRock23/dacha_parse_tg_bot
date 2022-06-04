import logging
from dotenv import load_dotenv
import os
import time

from aiogram import Bot, Dispatcher, executor, types

load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Бот парсит Яндекс Дачу https://plus.yandex.ru/dacha'
                         'на предмет появления новых ивентов и билетов на старые'
                         'по выбранным категориям.\n'
                         'Для выбора/изменения категорий введите "/category"')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)