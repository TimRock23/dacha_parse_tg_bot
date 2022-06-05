from aiogram import types

from db import get_all_categories, get_user_categories


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
