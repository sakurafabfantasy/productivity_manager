from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import cli.tg.keyboards as kb
from src.flashcards.service import (
    choosen_words,
    choosen_words_tr,
    change_card_status,
    add_word,
)
from src.flashcards.get_tr import translate

router = Router()


class StudyState(StatesGroup):
    learning = State()


class StudyState2(StatesGroup):
    addding = State()


async def welcome(event: Message | CallbackQuery):
    text = f"Привет {event.from_user.first_name}! Нажмите /study для изучения слов"
    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text)
        await event.answer()

    else:
        await event.reply(text)


@router.callback_query((F.data == "to_main_lang") | (F.data == "to_main"))
async def tomain(callback: CallbackQuery):
    await welcome(callback)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await welcome(message)


@router.message(Command("study"))
async def get_all(message: Message):
    await message.answer(
        "Выберите язык. Нажмите /add для добавления новой карточки",
        reply_markup=await kb.languages(),
    )


@router.callback_query(F.data.startswith("lang_"))
async def start_learning(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(StudyState.learning)
    lang = callback.data.split("_")[-1]
    words = await choosen_words(lang=lang)
    if not words:
        await callback.message.edit_text(
            text="На сегодня все слова по этому уроку повторены!",
            reply_markup=await kb.kb_show_start()

        )
        return
    await state.update_data(words=words, lang=lang, current_index=0)

    current_word = words[0]
    await callback.message.edit_text(
        text=str(current_word), reply_markup=await kb.kb_show_translation(0)
    )


@router.callback_query(F.data.startswith("translate_"))
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


@router.callback_query(F.data.startswith("mark_"))
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


@router.message(Command("add"))
async def add_msg(message: Message, state: FSMContext):
    await state.set_state(StudyState2.addding)
    await message.answer(
        "Введи карточку в формате: слово, язык на который нужно перевести слово, пример: персик,испанский"
    )


@router.message(StudyState2.addding)
async def new_word(message: Message, state: FSMContext):
    usr_input = message.text.strip()
    try:
        word, usr_lang = [x.strip().capitalize() for x in usr_input.split(",")]
    except ValueError:
        await message.answer(
            "Неверный формат ввода! Нажмите /add для повторного добавления"
        )
        return

    status_msg = await message.answer("Идёт перевод слова через Gemini, подождите")
    output = translate(word=word, lang=usr_lang)

    if output.startswith("Ошибка"):
        print(output)
        await status_msg.edit_text(
            "Ошибка подключения к нейросети! Поробуйте ещё раз через пару минут!"
        )
        return
    trword, lang2, lang = [x.strip().capitalize() for x in output.split(",")]

    await add_word(trword=trword, lang=lang, word=word)
    await status_msg.edit_text(
        f"Слово {word} на {lang2} -> {trword}. Слово успешно добавлено в БД. Нажмите /study для изучения карточек"
    )
