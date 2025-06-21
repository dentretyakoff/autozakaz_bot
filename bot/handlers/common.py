from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.methods import SendMessage
from aiogram.fsm.context import FSMContext

from api import api_backend
from core.constants import MessagesConstants
from handlers.keyboards import (
    main_menu_keyboard,
    back_to_main_keyboard,
    gdpr_confirm_keyboard
)


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> SendMessage:
    """Приветствие пользователя."""
    user = api_backend.users.create_or_update(
        message.from_user.id, message.from_user.username)
    if not user.get('gdpr_accepted'):
        gdpr = api_backend.about.get_gdpr() or MessagesConstants.DEFAULT_GDPR
        await message.answer(
            text=gdpr,
            reply_markup=gdpr_confirm_keyboard
        )
        return
    api_backend.users.create_cart(message.from_user.id)
    await message.answer(
        text=MessagesConstants.HELLO, reply_markup=main_menu_keyboard)


@router.callback_query(F.data == 'gdpr_confirm')
async def gdpr_confirm(callback_query: CallbackQuery) -> SendMessage:
    """Сохраняет согласие на обработку персональных данных."""
    api_backend.users.gdpr_confirm(callback_query.from_user.id)
    await callback_query.message.edit_text(
        text=MessagesConstants.HELLO,
        reply_markup=main_menu_keyboard)


@router.callback_query(F.data == 'back')
async def back_to_main(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Вернуться в главное меню."""
    await state.clear()
    await callback_query.message.edit_text(
        text=MessagesConstants.HELLO,
        reply_markup=main_menu_keyboard)


@router.message(F.text.startswith('/'))
async def unknown_command_handler(message: Message) -> SendMessage:
    """Обработка неизвестной команды."""
    await message.answer(
        text=MessagesConstants.UNKNOWN_COMMAND,
        reply_markup=back_to_main_keyboard)
