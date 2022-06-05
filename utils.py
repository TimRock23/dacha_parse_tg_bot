from typing import List

from aiogram import types
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from db import get_all_categories, get_user_categories

URI = 'https://plus.yandex.ru/dacha'


def get_category_keyboard(user_id: int) -> types.ReplyKeyboardMarkup:
    user_categories = get_user_categories(user_id=user_id)
    all_categories = get_all_categories()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for i, cat in enumerate(all_categories):
        if cat in user_categories:
            buttons.append(cat + ' +')
        else:
            buttons.append(cat + ' -')
        if i % 2 == 1 or i == len(all_categories) - 1:
            keyboard.add(*buttons)
            buttons = []
    return keyboard


def get_all_events() -> List[dict]:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URI)
    try:
        data = driver.find_elements(by=By.CLASS_NAME,
                                    value='dacha-events__item')
    except Exception as e:
        print(e)
        data = []

    all_events = []
    for event in data:
        text_event = [i for i in event.text.split('\n') if i not in ('', ' ')]
        category = text_event[3].split(' ')[-3]
        if category == 'Дети':
            continue
        tickets = (0 if text_event[5].startswith('Билетов нет')
                   else int(text_event[5].split(' ')[1]))
        all_events.append(
            {
                'date': text_event[0],
                'name': text_event[1],
                'description': text_event[2],
                'category': category,
                'tickets': tickets
            }
        )
    return all_events
