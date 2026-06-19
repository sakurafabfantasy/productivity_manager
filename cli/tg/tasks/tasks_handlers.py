from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import cli.tg.tasks.keyboards as kb
from src.tasks.service import (
    set_task,
    complete,
    get_all_tasks,
    delete_task,
    archive_date,
    add_sample,
    search_id,
)
import cli.tg.common.keyboards as src_kb

router = Router()


class TasksFSM(StatesGroup):
    adding = State()
    completing = State()
    deleting = State()


@router.callback_query(
    (F.data == "taskscmd") | (F.data == "cancel") | (F.data == "tasks_main")
)
async def welcome_msg(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    if callback.data == "cancel":
        await callback.answer("Действие отменено")
    await callback.answer()
    await callback.message.answer(
        "Главное меню", reply_markup=await src_kb.tasks()
    )


@router.message(Command("list_tasks"))
@router.callback_query(F.data == "listtasks")
async def show_list(event: Message | CallbackQuery):
    usr_id = event.from_user.id
    if isinstance(event, Message):
        await event.answer("Список всех задач", reply_markup=await kb.all_tasks(tg_id=usr_id))
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer(
            "Список всех задач", reply_markup=await kb.all_tasks(tg_id=usr_id)
        )


@router.message(Command("add_task"))
@router.callback_query(F.data == "addtask")
async def add_task_msg(event: Message | CallbackQuery, state: FSMContext):
    if isinstance(event, Message):
        await event.answer(
            f"Введите задачу в формате: Заголовок; тег(по желанию)",
            reply_markup=await kb.cancel(),
        )
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer(
            f"Введите задачу в формате: Заголовок; тег(по желанию)",
            reply_markup=await kb.cancel(),
        )
    await state.set_state(TasksFSM.adding)


@router.message(TasksFSM.adding)
async def add_task(message: Message, state: FSMContext):
    usr_id = message.from_user.id
    words = [item.strip() for item in message.text.split(";")]
    if len(words) == 2:
        await set_task(title=words[0], tag=words[1], tg_id=usr_id)
        await message.reply(f"Добавлена задача {words[0]} с тегом {words[1]}", reply_markup=await kb.show_start())
        await state.clear()

    elif len(words) == 1:
        await set_task(title=words[0], tg_id=usr_id)
        await message.reply(f"Добавлена задача {words[0]}", reply_markup=await kb.show_start())
        await state.clear()
    else:
        await message.reply(
            "Неверный формат ввода!Нажмите /add_task для повторного ввода данных."
        )
        await state.clear()


@router.callback_query(F.data == "archive")
async def show_archive_list(callback: CallbackQuery):
    usr_id = callback.from_user.id
    await callback.answer()
    await callback.message.answer(
        "Список архивных задач", reply_markup=await kb.archive_tasks(tg_id=usr_id)
    )


@router.message(Command("complete"))
@router.callback_query(F.data == "complete")
async def complete_task_msg(event: Message | CallbackQuery, state: FSMContext):
    usr_id = event.from_user.id
    await state.set_state(TasksFSM.completing)
    tasks = await get_all_tasks(tg_id=usr_id)
    tasks_list = []
    if not tasks:
        await event.answer("Список пуст")
        return

    for task in tasks:
        if task.is_completed is False:
            tasks_list.append(f"ID: {task.id}. Заголовок: {task.title}")
    text = "\n".join(tasks_list)
    if isinstance(event, Message):
        await event.answer(text)
        await event.answer(
            "Выберите задачу или задачи(через запятую) для заверешения, напишите ID. Пример: 45,67"
        )
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer(text)
        await event.message.answer(
            "Выберите задачу или задачи(через запятую) для заверешения, напишите ID. Пример: 45,67"
        )


@router.message(TasksFSM.completing)
async def complete_task(message: Message, state: FSMContext):
    nums = [item.strip() for item in message.text.split(",")]
    for num in nums:
        try:
            await complete(int(num))
        except ValueError:
            return
        await archive_date(int(num))
        await message.answer(
            f"Завершена задача с ID {int(num)}. Срок хранения в архиве истекает через 30 дней",
            reply_markup=await kb.show_start()
        )

    await state.clear()


@router.message(Command("del_task"))
@router.callback_query(F.data == "deltask")
async def del_task_msg(event: Message | CallbackQuery, state: FSMContext):
    await state.set_state(TasksFSM.deleting)
    usr_id = event.from_user.id
    nums = await get_all_tasks(tg_id=usr_id)
    tasks_list = []
    if not nums:
        await event.answer("Список пуст")
        return
    for num in nums:
        if num.is_completed is False:
            tasks_list.append(f"ID: {num.id}. Заголовок: {num.title}")
    if isinstance(event, Message):
        await event.answer("\n".join(tasks_list))
        await event.answer(
            "Выберите задачу или задачи(через запятую) для удаления, напишите ID. Пример: 45,67"
        )
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer("\n".join(tasks_list))
        await event.message.answer(
            "Выберите задачу или задачи(через запятую) для удаления, напишите ID. Пример: 45,67"
        )


@router.message(TasksFSM.deleting)
async def del_task(message: Message, state: FSMContext):
    nums = [num.strip() for num in message.text.split(",")]
    for num in nums:
        await delete_task(int(num))
        await message.answer(f"Удалена задача с ID {num}", reply_markup=await kb.show_start())
    await state.clear() 


@router.callback_query(F.data.startswith("delete_"))
async def del_task_callback(callback: CallbackQuery):
    num = callback.data.strip().split("_")[-1]
    await callback.answer()
    await delete_task(int(num))
    await callback.message.answer(f"Удалена задача с ID {num}")


@router.callback_query(F.data.startswith("complete_"))
async def complete_task_callback(callback: CallbackQuery):
    num = callback.data.strip().split("_")[-1]
    await callback.answer()
    await complete(int(num))
    await callback.message.answer(f"Завершена задача с ID {num}")


@router.callback_query(F.data.startswith("archive_"))
async def show_archive_info(callback: CallbackQuery):
    task_id = callback.data.strip().split("_")[-1]
    usr_id = callback.from_user.id
    task = await search_id(int(task_id))
    await callback.answer()
    await callback.message.edit_text(
        text=f"Информация о задаче: {task}", reply_markup=await kb.info_task(title=task, tg_id=usr_id)
    )


@router.message(Command("cjcbcj4yfz"))
async def add_new_sample_cards(message: Message):
    usr_id = message.from_user.id
    await add_sample(tg_id=usr_id)
    await message.answer("✅")


@router.callback_query(F.data.startswith("task_"))
async def show_task_info(callback: CallbackQuery):
    task_id = callback.data.strip().split("_")[-1]
    usr_id = callback.from_user.id
    task = await search_id(int(task_id))
    await callback.answer()
    await callback.message.edit_text(
        text=f"Информация о задаче: {task}", reply_markup=await kb.info_task(title=task, tg_id=usr_id)
    )
