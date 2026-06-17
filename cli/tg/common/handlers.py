from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import cli.tg.common.keyboards as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from cli.tg.common.service import set_setting, find_mode

router = Router()

class CommonFSM(StatesGroup):
    adding = State()

@router.message(CommandStart())
async def welcome_msg(message: Message):
    usr_id = message.from_user.id
    find = await find_mode(tg_id=usr_id)
    if find:
        usr_func = getattr(kb, find.setting)
        reply_kb = await usr_func()
    else:
        reply_kb = await kb.main_msg()

    await message.answer(f"Привет {message.from_user.first_name}!", reply_markup=reply_kb)
    
@router.message(Command("Default"))
@router.callback_query((F.data == "defaultstart") | (F.data == "change"))
async def set_default_msg(event: Message | CallbackQuery, state: FSMContext):
    await state.set_state(CommonFSM.adding)
    if isinstance(event, Message):
        await event.answer("Выберите дефолтный режим команды /start", reply_markup= await kb.default_choice())
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer("Выберите дефолтный режим команды /start", reply_markup = await kb.default_choice())

@router.callback_query(CommonFSM.adding, (F.data == "notes") | (F.data == "tasks") | (F.data == "cards") | (F.data == "main_msg"))
async def set_default(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    usr_choice = callback.data
    usr_id = callback.from_user.id
    await set_setting(tg_id=usr_id, choice=str(usr_choice))
    find = await find_mode(tg_id=usr_id)
    if find and hasattr(kb, find.setting):
        usr_func = getattr(kb, find.setting)
        reply_kb = await usr_func()
    else:
        reply_kb = await kb.main_msg()
    await callback.message.edit_text("Главное меню")
    await callback.message.edit_reply_markup(reply_markup=reply_kb)


