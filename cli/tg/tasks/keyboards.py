from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.tasks.service import get_all_tasks

async def all_tasks():
    list_tasks = await get_all_tasks()
    builder = InlineKeyboardBuilder()
    for task in list_tasks:
        if task.is_completed is False:
            builder.add(InlineKeyboardButton(text=f"🟢{task.title}", callback_data=f"task_{task.title}"))
    builder.add(InlineKeyboardButton(text="На главную", callback_data="tasks_main"))
    builder.add(InlineKeyboardButton(text="Архив", callback_data="archive"))
    return builder.adjust(1).as_markup()

async def archive_tasks():
    list_tasks = await get_all_tasks()
    builder = InlineKeyboardBuilder()
    for task in list_tasks:
        if task.is_completed is True:
            builder.add(InlineKeyboardButton(text=f"🔴{task.title}", callback_data=f"archive_{task.id}"))
    builder.add(InlineKeyboardButton(text="На главную", callback_data="tasks_main"))
    builder.add(InlineKeyboardButton(text="Акутальные задачи", callback_data="archive"))
    return builder.adjust(1).as_markup()

async def cancel():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    return builder.as_markup()

async def info_archive():
    builder = InlineKeyboardBuilder()
    tasks = await get_all_tasks()
    for task in tasks:
        if task.is_completed is True:
            form = task.expiring_date.strftime("%d/%m/%Y")
            builder.add(InlineKeyboardButton(text=f"Дата удаления: {form}", callback_data="archive"))
            builder.add(InlineKeyboardButton(text="Удалить задачу", callback_data=f"delete_{task.id}"))
            builder.add(InlineKeyboardButton(text="На главную", callback_data="tasks_main"))
    return builder.adjust(1).as_markup()