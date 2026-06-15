from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import cli.tg.common.keyboards as kb

router = Router()

@router.message(CommandStart())
async def welcome_msg(message: Message):
    await message.answer(f"Привет {message.from_user.first_name}!", reply_markup=await kb.main_msg())