from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def main_msg():
    builder = InlineKeyboardBuilder()
    builder.button(text="Заметки", callback_data="notescmd")
    builder.button(text="Задачи", callback_data="taskscmd")
    builder.button(text="Изучение слов", callback_data="studycmd")
    builder.button(text="Выбрать дефолтный режим", callback_data="defaultstart")
    return builder.adjust(2, 1, 1).as_markup()

async def default_choice():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Заметки", callback_data="notes"))
    builder.add(InlineKeyboardButton(text="Задачи", callback_data="tasks"))
    builder.add(InlineKeyboardButton(text="Изучение слов", callback_data="cards"))
    builder.add(InlineKeyboardButton(text="Все 3 режима", callback_data="main"))
    return builder.adjust(1).as_markup()

async def notes():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Список заметок", callback_data="list"))
    builder.add(InlineKeyboardButton(text="Список заметок по тегу", callback_data="listbytag"))
    builder.add(InlineKeyboardButton(text="Добавить заметку", callback_data="addnote"))
    builder.add(InlineKeyboardButton(text="Удалить заметку", callback_data="delete"))
    builder.add(InlineKeyboardButton(text="Изменить дефолтный режим", callback_data="change"))
    return builder.adjust(1,1,2,1).as_markup()

async def tasks():
    builder = InlineKeyboardBuilder()
    builder.button(text="Список задач", callback_data="listtasks")
    builder.button(text="Добавить задачу", callback_data="addtask")
    builder.button(text="Удалить задачу", callback_data="deltask")
    builder.button(text="Завершить задачу", callback_data="complete")
    builder.button(text="Изменить дефолтный режим", callback_data="change")
    return builder.adjust(2,2,1).as_markup()

async def cards():
    builder = InlineKeyboardBuilder()
    builder.button(text="Изучение слов", callback_data="study")
    builder.button(text="Добавить карточку", callback_data="add_card")
    builder.button(text="Удалить карточку", callback_data="del_card")
    builder.button(text="Изменить дефолтный режим", callback_data="change")
    return builder.adjust(2,1,1).as_markup()