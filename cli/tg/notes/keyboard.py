from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from src.notes.service import get_all_notes, info_note
from datetime import datetime

async def list_notes():
    notes = await get_all_notes()
    builder = InlineKeyboardBuilder()
    if notes != []:
        for note in notes:
            builder.add(InlineKeyboardButton(text=f"{note.title}", callback_data=f"note_{note.id}"))
    else:
        builder.add(InlineKeyboardButton(text="Список пуст", callback_data="addnote"))
    builder.add(InlineKeyboardButton(text="На главную", callback_data="tomain"))

        
    builder.add(InlineKeyboardButton(text="Добавить заметку", callback_data="addnote"))
    builder.add(InlineKeyboardButton(text="Удалить заметку", callback_data="delnote"))
    return builder.adjust(1).as_markup()

async def note_info(id: int):
    info = await info_note(id=id)
    builder = InlineKeyboardBuilder()
    if info is not None:
        if info.tag is not None:
            builder.add(InlineKeyboardButton(text=f"Тег: {info.tag}", callback_data="tomain"))
        else:
            builder.add(InlineKeyboardButton(text="Тег отсутсвует", callback_data="tomain"))
        cool_date = info.created_at.strftime("%d/%m/%Y")
        builder.add(InlineKeyboardButton(text=f"Дата создания: {cool_date}", callback_data="tomain"))
        builder.add(InlineKeyboardButton(text="Удалить заметку", callback_data=f"del_{info.id}"))
        builder.add(InlineKeyboardButton(text="На главную", callback_data="tomain"))
        return builder.adjust(1,1,2).as_markup()
