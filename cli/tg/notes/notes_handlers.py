from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import cli.tg.notes.keyboard as kb
from src.notes.service import info_note, delete_note, set_note, get_all_notes

router = Router()


class NotesFSM(StatesGroup):
    adding = State()
    deleting = State()


@router.callback_query(
    (F.data == "notescmd") | (F.data == "cancel") | (F.data == "tomain")
)
async def welcome_msg(callback: CallbackQuery):
    if callback.data == "cancel":
        await callback.answer("Действие отменено")
    await callback.message.edit_text(
        "Список доступных команд:\n/list_notes - список заметок\n/list_tag - список заметок по тегу\n/add_note - добавить заметку\n/del_note - удалить заметку"
    )


@router.message(Command("list_notes"))
@router.callback_query(F.data == "list")
async def show_list(event: Message | CallbackQuery):
    if isinstance(event, Message):
        await event.answer("Список всех заметок", reply_markup=await kb.list_notes())
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer("Список всех заметок", reply_markup=await kb.list_notes())

@router.callback_query(F.data.startswith("note_"))
async def show_note_info(callback: CallbackQuery):
    note = callback.data.strip().split("_")[-1]
    information = await info_note(id=int(note))
    if information is not None:
        title = information.title
        content = information.content
    await callback.message.edit_text(
        f"Заголовок: {title}\nСодержание: {content}",
        reply_markup=await kb.note_info(id=int(note)),
    )


@router.callback_query(F.data.startswith("del_"))
async def del_current_note(callback: CallbackQuery):
    await callback.answer()
    note_id = callback.data.strip().split("_")[-1]
    await delete_note(int(note_id))
    await callback.message.answer(f"Удалена заметка с ID: {note_id}✅")


@router.callback_query(F.data == "addnote")
@router.message(Command("add_note"))
async def add_note_msg(event: CallbackQuery | Message, state: FSMContext):
    await state.set_state(NotesFSM.adding)
    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer(
            "Введите заметку в формате Заголовок;Описание;Тег(по желанию)"
        )
    elif isinstance(event, Message):
        await event.answer(
            "Введите заметку в формате Заголовок;Описание;Тег(по желанию)"
        )


@router.message(NotesFSM.adding)
async def add_note(message: Message, state: FSMContext):
    usr_input = [item.strip().capitalize() for item in message.text.split(";")]
    if len(usr_input) == 2:  # без тега
        title, content, tag = usr_input[0], usr_input[1], None
    elif len(usr_input) == 3:  # с тегом
        title, content, tag = usr_input[0], usr_input[1], usr_input[2]
    else:
        await message.reply(
            "Неверный формат ввода!\nНажмите /add_note для повторного ввода"
        )
        return
    await set_note(title=title, text=content, tag=tag)
    await message.answer(f"Добавлена заметка с заголовком {title}")
    await state.clear()

@router.callback_query(F.data == "delete")
@router.message(Command("del"))
async def delete_note_msg(event: Message | CallbackQuery, state: FSMContext):
    await state.set_state(NotesFSM.deleting)
    notes = await get_all_notes()
    notes_text = []
    if not notes:
        await event.answer("Список пуст")
        return
    for note in notes:
        notes_text.append(f"ID: {note.id} Заголовок: {note.title}")
    text = "\n".join(notes_text)
    if isinstance(event, Message):
        await event.answer(text)
        await event.answer("Введите заметку или заметки(через запятую) которые вы хотите удалить. Пример: 13, 67, 54")
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer(text)
        await event.message.answer("Введите заметку или заметки(через запятую) которые вы хотите удалить. Пример: 13, 67, 54")


@router.message(NotesFSM.deleting)
async def delete_notes(message: Message, state: FSMContext):
    notes_to_delete = [item.strip() for item in message.text.split(",")] 
    for note in notes_to_delete:
        await delete_note(id=int(note))
        await message.reply(f"Удалена заметка с ID {note}")
    
    await state.clear()



