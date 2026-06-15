from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def main_msg():
    builder = InlineKeyboardBuilder()
    builder.button(text="Заметки", callback_data="notescmd")
    builder.button(text="Задачи", callback_data="taskscmd")
    builder.button(text="Изучение слов", callback_data="studycmd")
    return builder.adjust(2, 1).as_markup()
