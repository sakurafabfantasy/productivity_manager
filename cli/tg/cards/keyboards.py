from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.flashcards.service import cards_list


async def languages():
    all_cards = await cards_list()
    keyboard = InlineKeyboardBuilder()
    seen_langs = set()
    for card in all_cards:
        if card.language not in seen_langs:
            keyboard.add(
                InlineKeyboardButton(
                    text=card.language, callback_data=f"lang_{card.language}"
                )
            )
            seen_langs.add(card.language)
    keyboard.add(InlineKeyboardButton(text="Добавить карточку", callback_data="add"))
    keyboard.add(InlineKeyboardButton(text="На главную", callback_data="to_main_lang"))
    return keyboard.adjust(1,2).as_markup()


async def kb_marks(word_index: int):
    builder = InlineKeyboardBuilder()
    for mark in range(1, 6):
        builder.button(text=str(mark), callback_data=f"mark_{mark}")
    builder.adjust(5)
    return builder.as_markup()


async def kb_show_translation(word_index: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="Показать перевод", callback_data=f"translate_{word_index}")
    return builder.adjust(2).as_markup()

async def kb_show_start():
    builder = InlineKeyboardBuilder()
    builder.button(text="На главную", callback_data="to_main")
    return builder.as_markup()

async def welcome_msg():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Изучение слов", callback_data="study"))
    builder.add(InlineKeyboardButton(text="Добавить карточку", callback_data="add"))
    return builder.adjust(1).as_markup()


async def cancel_button():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    return builder.as_markup()