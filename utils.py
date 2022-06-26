from dataclasses import dataclass
import re
from time import time
from typing import List

from aiogram import types
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from db import get_all_categories, get_user_categories

URI = 'https://plus.yandex.ru/dacha'
CACHE_TIME_SEC = 180
PARSE_ITEM = 'dacha-events__item'
REGISTRATION_URI = ('https://widget.afisha.yandex.ru/w/sessions/ticketsteam'
                    '-1550%40{id}')
ID_REGEX = r'\[data-style-id="dacha-event-card-(.*?)\"\]'


@dataclass
class Event:
    """Class to store event data."""
    index: str
    date: str
    name: str
    description: str
    category: str
    tickets: int
    NEW_EVENT_MESSAGE = ('Новое событие: {name}\n'
                         'Категория: {category}\n'
                         'Дата: {date}\n'
                         'Билетов: {tickets}\n'
                         'Регистрация: {uri}')
    NEW_TICKETS_MESSAGE = ('Новые билеты у события {name}\n'
                           'Дата: {date}\n'
                           'Билетов: {tickets}'
                           'Регистрация: {uri}')
    EVENT_MESSAGE = ('Cобытие: {name}\n'
                     'Категория: {category}\n'
                     'Дата: {date}\n'
                     'Билетов: {tickets}'
                     'Регистрация: {uri}')

    def get_new_event_message(self) -> str:
        return self.NEW_EVENT_MESSAGE.format(name=self.name,
                                             category=self.category,
                                             date=self.date,
                                             tickets=self.tickets,
                                             uri=REGISTRATION_URI.format(
                                                 id=self.index))

    def get_new_tickets_message(self) -> str:
        return self.NEW_TICKETS_MESSAGE.format(name=self.name,
                                               date=self.date,
                                               tickets=self.tickets,
                                               uri=REGISTRATION_URI.format(
                                                   id=self.index))

    def get_event_message(self) -> str:
        return self.EVENT_MESSAGE.format(name=self.name,
                                         category=self.category,
                                         date=self.date,
                                         tickets=self.tickets,
                                         uri=REGISTRATION_URI.format(
                                             id=self.index))


def cache(func):
    res = None
    cache_time = time()

    def wrapper(*args, **kwargs):
        nonlocal res
        if not res or time() - cache_time > CACHE_TIME_SEC:
            res = func(*args, **kwargs)
        return res

    return wrapper


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


@cache
def get_all_events() -> List[Event]:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URI)
    try:
        data = driver.find_elements(by=By.CLASS_NAME,
                                    value=PARSE_ITEM)
    except Exception as e:
        print(e)
        data = []

    all_events = []
    for event in data:
        text_event = [i for i in event.text.split('\n') if i not in ('', ' ')]
        category = None
        style = event.find_elements(by=By.TAG_NAME, value='style')
        inner = style[0].get_attribute('innerHTML')
        index = str(re.search(ID_REGEX, inner).group(1))

        for event_info in text_event:
            if event_info.strip(' ').startswith('Бесплатно с Плюсом'):
                category = event_info.split(' ')[-3]
        tickets = (0 if text_event[-1].startswith('Билетов нет')
                   else int(text_event[-1].split(' ')[1]))
        all_events.append(
            Event(index=index,
                  date=text_event[0],
                  name=text_event[1],
                  description=text_event[2],
                  category=category,
                  tickets=tickets)
        )
    return all_events


def is_event_old(old_event: Event, event: Event) -> bool:
    return old_event.name == event.name and old_event.date == event.date


get_all_events()
