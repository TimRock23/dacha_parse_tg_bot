from dataclasses import asdict, dataclass
import re
from time import time
from typing import List

from aiogram import types
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from db import get_all_categories, get_user_categories
import settings


@dataclass(frozen=True)
class Event:
    """Class to store and serialize event data."""
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
        return self.NEW_EVENT_MESSAGE.format(**asdict(self),
                                             uri=settings.REG_URI.format(
                                                 id=self.index))

    def get_new_tickets_message(self) -> str:
        return self.NEW_TICKETS_MESSAGE.format(**asdict(self),
                                               uri=settings.REG_URI.format(
                                                   id=self.index))

    def get_event_message(self) -> str:
        return self.EVENT_MESSAGE.format(**asdict(self),
                                         uri=settings.REG_URI.format(
                                             id=self.index))


def cache(func):
    res = None
    cache_time = time()

    def wrapper(*args, **kwargs):
        nonlocal res
        if not res or time() - cache_time > settings.CACHE_TIME_SEC:
            res = func(*args, **kwargs)
        return res

    return wrapper


def get_category_keyboard(user_id: int) -> types.ReplyKeyboardMarkup:
    user_categories = get_user_categories(user_id=user_id)
    all_categories = get_all_categories()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for idx, category in enumerate(all_categories):
        if category in user_categories:
            buttons.append(category + ' +')
        else:
            buttons.append(category + ' -')
        if idx % 2 == 1 or idx == len(all_categories) - 1:
            keyboard.add(*buttons)
            buttons = []
    return keyboard


def request_url_for_events() -> list:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    try:
        driver.get(settings.URI)
        data = driver.find_elements(by=By.CLASS_NAME,
                                    value=settings.PARSE_ITEM)
    except Exception as e:
        print(e)
        data = []
    return data


def parse_category(text_event) -> str:
    category = None
    for event_info in text_event:
        if event_info.strip(' ').startswith(settings.PLUS_ADVERTISING):
            category = event_info.split(' ')[-3]
    return category


def parse_tickets(text_event) -> int:
    if text_event[-1].startswith('Билетов нет'):
        return 0
    else:
        return int(text_event[-1].split(' ')[1])


def parse_index(event) -> str:
    style = event.find_elements(by=By.TAG_NAME, value='style')
    inner = style[0].get_attribute('innerHTML')
    index = str(re.search(settings.ID_REGEX, inner).group(1))
    return index


def parse_event(event) -> Event:
    text_event = [i for i in event.text.split('\n') if i not in ('', ' ')]

    return Event(index=parse_index(event),
                 date=text_event[0],
                 name=text_event[1],
                 description=text_event[2],
                 category=parse_category(text_event),
                 tickets=parse_tickets(text_event))


@cache
def get_all_events() -> List[Event]:
    raw_events = request_url_for_events()
    return [parse_event(event) for event in raw_events]


def is_event_old(old_event: Event, event: Event) -> bool:
    return old_event.name == event.name and old_event.date == event.date
