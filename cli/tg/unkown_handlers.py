from aiogram.types import Message, CallbackQuery
from aiogram import F, Router

router = Router()


@router.callback_query()
async def unknown_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Неизвестная команда")


@router.message()
async def unknown_command(message: Message):
    await message.reply("Неизвестная комнда")
