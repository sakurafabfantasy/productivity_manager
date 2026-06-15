from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import cli.tg.tasks.keyboards as kb
from src.tasks.service import set_task, complete, get_all_tasks

router = Router()

class TasksFSM(StatesGroup):
    adding = State()
    completing = State()

@router.callback_query(F.data == "taskscmd")
async def welcome_msg(callback: CallbackQuery):
    await callback.message.edit_text("Список доступных команд:\n /list_tasks - список всех задач\n/add_task - добавить задачу\n/del_task - удалить задачу")

@router.message(Command("list_tasks"))
async def show_list(message: Message):
    await message.answer("Список всех задач", reply_markup=await kb.all_tasks())


@router.message(Command("add_task"))
async def add_task_msg(message: Message, state: FSMContext):
    await message.answer(f"Введите задачу в формате: Заголовок, тег(по желанию)")
    await state.set_state(TasksFSM.adding)

@router.message(TasksFSM.adding)
async def add_task(message: Message, state: FSMContext):
    words = [item.strip() for item in message.text.split(",")]
    if len(words) == 2:
        await set_task(title=words[0], tag=words[1])
        await message.reply(f"Добавлена задача {words[0]} с тегом {words[1]}")
        await state.clear()

    elif len(words) == 1:
        await set_task(title=words[0])
        await message.reply(f"Добавлена задача {words[0]}")
        await state.clear()
    else:
        await message.reply("Неверный формат ввода!Нажмите /add_task для повторного ввода данных.")
        await state.clear()

@router.callback_query(F.data == "archive")
async def show_archive_list(callback: CallbackQuery):
    await callback.message.edit_text("Список архивных задач", reply_markup=await kb.archive_tasks())
    
@router.message(Command("complete"))
async def complete_task_msg(message: Message, state: FSMContext):
    await state.set_state(TasksFSM.completing)
    tasks = await get_all_tasks()
    tasks_list = []
    for task in tasks:
        if task.is_completed is False:
            tasks_list.append(f"ID: {task.id}. Заголовок: {task.title}")
    text = '\n'.join(tasks_list)
    await message.answer(text)
    await message.answer("Выберите задачу или задачи(через запятую) для заверешения, напишите ID. Пример: 45,67")

@router.message(TasksFSM.completing)
async def complete_task(message: Message, state: FSMContext):
    nums = [item.strip() for item in message.text.split(",")]
    for num in nums:
        await complete(int(num))
        await message.answer(f"Завершена задача с ID {int(num)}")
    await state.clear()