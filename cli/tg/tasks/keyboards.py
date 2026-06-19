from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.tasks.service import get_all_tasks, info_abt_task


async def all_tasks(tg_id: int):
    list_tasks = await get_all_tasks(tg_id=tg_id)
    builder = InlineKeyboardBuilder()
    for task in list_tasks:
        if task.is_completed is False:
            builder.add(
                InlineKeyboardButton(
                    text=f"🟢{task.title}", callback_data=f"task_{task.id}"
                )
            )
    builder.add(InlineKeyboardButton(text="На главную", callback_data="tasks_main"))
    builder.add(InlineKeyboardButton(text="Архив", callback_data="archive"))
    builder.add(InlineKeyboardButton(text="Завершить задачу", callback_data="complete"))

    return builder.adjust(1).as_markup()

async def show_start():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="На главную", callback_data="tasks_main"))
    return builder.adjust(1).as_markup()



async def archive_tasks(tg_id: int):
    list_tasks = await get_all_tasks(tg_id=tg_id)
    builder = InlineKeyboardBuilder()
    for task in list_tasks:
        if task.is_completed is True:
            builder.add(
                InlineKeyboardButton(
                    text=f"🔴{task.title}", callback_data=f"archive_{task.id}"
                )
            )
    builder.add(InlineKeyboardButton(text="На главную", callback_data="tasks_main"))
    builder.add(
        InlineKeyboardButton(text="Акутальные задачи", callback_data="listtasks")
    )
    return builder.adjust(1).as_markup()


async def cancel():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    return builder.as_markup()


async def info_task(title: str, tg_id: int):
    builder = InlineKeyboardBuilder()
    task = await info_abt_task(title=title, tg_id=tg_id)
    if task is not None:
        if task.tag is not None:
            builder.add(
                InlineKeyboardButton(text=f"Тег: {task.tag}", callback_data="listtasks")
            )
        else:
            builder.add(
                InlineKeyboardButton(text="Тег отсутствует", callback_data="listtasks")
            )

        if task.is_completed is False:
            form = task.created_at.strftime("%d/%m/%Y")
            builder.add(
                InlineKeyboardButton(
                    text=f"Дата создания: {form}", callback_data="listtasks"
                )
            )
            builder.add(
                InlineKeyboardButton(
                    text="Завершить задачу", callback_data=f"complete_{task.id}"
                )
            )
            builder.add(InlineKeyboardButton(text="Список всех задач", callback_data="listtasks"))
            builder.add(
                InlineKeyboardButton(text="На главную", callback_data="tasks_main")
            )
            
            return builder.adjust(1, 1, 2, 1).as_markup()

        else:
            form = task.expiring_date.strftime("%d/%m/%Y")
            builder.add(
                InlineKeyboardButton(
                    text=f"Дата удаления: {form}", callback_data="listtasks"
                )
            )
            builder.add(
                InlineKeyboardButton(
                    text="Удалить задачу", callback_data=f"delete_{task.id}"
                )
            )
            builder.add(InlineKeyboardButton(text="Список всех задач", callback_data="listtasks"))
            builder.add(
                InlineKeyboardButton(text="На главную", callback_data="tasks_main")
            )
            return builder.adjust(1, 1, 2).as_markup()


async def welcome_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Список задач", callback_data="listtasks"))
    builder.add(InlineKeyboardButton(text="Добавить задачу", callback_data="addtask"))
    return builder.adjust(1).as_markup()
