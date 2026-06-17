from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import cli.tg.cards.keyboards as kb
from src.flashcards.service import (
    choosen_words,
    choosen_words_tr,
    change_card_status,
    add_word,
    delete_card,
    cards_list
)
from src.flashcards.get_tr import translate

router = Router()


class CardsFSM(StatesGroup):
    learning = State()
    adding = State()
    deleting = State()


@router.callback_query((F.data == "to_main_lang") | (F.data == "to_main") | (F.data == "studycmd") | (F.data == "cancel"))
async def tomain(callback: CallbackQuery):
    text = f"Список доступных команд:\n/study - изучение слов\n/add_card - добавление карточки\n/del_card - удаление карточки"
    await callback.message.edit_text(text, reply_markup=await kb.welcome_msg())




@router.message(Command("study"))
@router.callback_query(F.data == "study")
async def get_all(event: Message | CallbackQuery):
    if isinstance(event, Message):
        await event.answer(
            "Выберите язык. Нажмите /add_card для добавления новой карточки",
            reply_markup=await kb.languages(),
        )
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer(
            "Выберите язык. Нажмите /add_card для добавления новой карточки",
            reply_markup=await kb.languages(),
        )


@router.callback_query(F.data.startswith("lang_"))
async def start_learning(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(CardsFSM.learning)
    lang = callback.data.split("_")[-1]
    words = await choosen_words(lang=lang)
    if not words:
        await callback.message.edit_text(
            text="На сегодня все слова по этому уроку повторены!",
            reply_markup=await kb.kb_show_start()

        )
        await state.clear()
        return
    
    await state.update_data(words=words, lang=lang, current_index=0)

    current_word = words[0]
    await callback.message.edit_text(
        text=str(current_word), reply_markup=await kb.kb_show_translation(0)
    )


@router.callback_query(F.data.startswith("translate_"), CardsFSM.learning)
async def translate_word(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    words = data.get("words", [])
    current_language = data.get("lang", "русский")
    current_index = callback.data.split("_")[-1]
    current_word = words[int(current_index)]
    tr_word = await choosen_words_tr(word=current_word, lang=current_language)
    await callback.message.edit_text(
        text=str(tr_word), reply_markup=await kb.kb_marks(int(current_index))
    )


@router.callback_query(F.data.startswith("mark_"), CardsFSM.learning)
async def continue_learning(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    words = data.get("words", [])
    current_index = data.get("current_index", 0)
    current_word = words[current_index]
    next_index = current_index + 1
    await change_card_status(word=current_word, num=int(callback.data.split("_")[-1]))

    if next_index < len(words):
        await state.update_data(current_index=next_index)
        next_word = words[next_index]
        await callback.message.edit_text(
            text=str(next_word), reply_markup=await kb.kb_show_translation(next_index)
        )

    else:
        await callback.message.edit_text(
            text="Поздравляю! Вы повторили все слова!",
            reply_markup=await kb.kb_show_start()
        )
        await state.clear()


@router.message(Command("add_card"))
@router.callback_query(F.data == "add_card")
async def add_msg(event: Message | CallbackQuery, state: FSMContext):
    await state.set_state(CardsFSM.adding)
    if isinstance(event, Message):
        await event.answer(
            "Введи карточку в формате: слово, язык на который нужно перевести слово, пример: персик,испанский",
            reply_markup=await kb.cancel_button()
        )
    elif isinstance(event, CallbackQuery):
        await event.message.edit_text(
            "Введи карточку в формате: слово, язык на который нужно перевести слово, пример: персик,испанский",
            reply_markup=await kb.cancel_button()
        )


@router.message(CardsFSM.adding)
async def new_word(message: Message, state: FSMContext):
    usr_input = message.text.strip()
    try:
        word, usr_lang = [x.strip().capitalize() for x in usr_input.split(",")]
    except ValueError:
        await message.answer(
            "Неверный формат ввода! Нажмите /add_card для повторного добавления"
        )
        await state.clear()
        return

    status_msg = await message.answer("Идёт перевод слова через Gemini, подождите")
    output = await translate(word=word, lang=usr_lang)

    if output.startswith("Ошибка"):
        print(output)
        await status_msg.edit_text(
            "Ошибка подключения к нейросети! Поробуйте ещё раз через пару минут!"
        )
        await state.clear()
        return
    trword, lang2, lang = [x.strip().capitalize() for x in output.split(",")]

    await add_word(trword=trword, lang=lang, word=word)
    await status_msg.edit_text(
        f"Слово {word} на {lang2} -> {trword}. Слово успешно добавлено в БД. Нажмите /study для изучения карточек"
    )
    await state.clear()

@router.message(Command("del_card"))
@router.callback_query(F.data == "del_card")
async def del_card_msg(event: Message | CallbackQuery, state: FSMContext):
    await state.set_state(CardsFSM.deleting)
    if isinstance(event, Message):
        
        text = []
        words = await cards_list()
        for word in words:
            text.append(f"ID: {word.id}, Слово: {word.word}")
        response_text = "\n".join(text)
        await event.answer(response_text)
        await event.answer("Введите ID карточки или карточек через запятую которые вы хотите удалить\nПример №1: 43,45. Пример №2: 56")
    elif isinstance(event, CallbackQuery):
        await event.answer()
        text = []
        words = await cards_list()
        for word in words:
            text.append(f"ID: {word.id}, Слово: {word.word}")
        response_text = "\n".join(text)
        await event.message.edit_text(response_text)
        await event.message.answer("Введите ID карточки или карточек через запятую которые вы хотите удалить\nПример №1: 43,45. Пример №2: 56")
@router.message(CardsFSM.deleting)
async def del_card(message: Message, state: FSMContext):
    nums = [item.strip() for item in message.text.split(",")]
    for id in nums:
        try:
            await delete_card(int(id))
        except ValueError:
            await message.reply("Неверный формат ввода!")
    await message.answer(f"Удалены карточки: {','.join(nums)} ")
    await state.clear()

    