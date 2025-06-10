from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.methods import SendMessage

from api import api_backend
from core.constants import MessagesConstants
from handlers.keyboards import main_menu_keyboard, back_to_main_keyboard


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> SendMessage:
    """Приветствие пользователя."""
    api_backend.users.create_or_update(
        message.from_user.id, message.from_user.username)
    await message.answer(
        text=MessagesConstants.HELLO, reply_markup=main_menu_keyboard)


@router.callback_query(F.data == 'back')
async def back_to_main(callback_query: CallbackQuery) -> SendMessage:
    """Вернуться в главное меню."""
    await callback_query.message.edit_text(
        text=MessagesConstants.HELLO,
        reply_markup=main_menu_keyboard)


@router.message(F.text.startswith('/'))
async def unknown_command_handler(message: Message) -> SendMessage:
    """Обработка неизвестной команды."""
    await message.answer(
        text=MessagesConstants.UNKNOWN_COMMAND,
        reply_markup=back_to_main_keyboard)
