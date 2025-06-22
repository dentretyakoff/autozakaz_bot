import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.methods import SendMessage

from api import api_backend
from core.constants import MessagesConstants
from handlers.keyboards import (
    create_order_keyboard,
    generate_phone_buttons
)
from handlers.states import UserForm, CartForm
from core.validators import validate_phone_number, validate_message_is_text
from handlers.utils import delete_previous_message, get_cart_detail

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == 'phone')
async def phone(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Предлагает оставить телефон."""
    response = api_backend.users.get_user(callback_query.from_user.id)
    phone = response.json().get('phone')
    if phone:
        return await callback_query.message.edit_text(
            text='Номер телефона для связи',
            reply_markup=generate_phone_buttons(phone))
    sent_message = await callback_query.message.edit_text(
        'Введи номер телефона:')
    await state.update_data(phone_message_id=sent_message.message_id)
    await state.set_state(UserForm.phone)


@router.callback_query(F.data == 'new_phone')
async def new_phone(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Ожидает ввода номера телефона."""
    sent_message = await callback_query.message.edit_text(
        'Введи номер телефона:')
    await state.update_data(phone_message_id=sent_message.message_id)
    await state.set_state(UserForm.phone)


@router.callback_query(F.data == 'exist_phone')
async def exist_phone(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """При воборе текущего номер телефона переводит на ввод комментария."""
    await state.clear()
    sent_message = await callback_query.message.edit_text(
        MessagesConstants.REQUEST_COMMENT)
    await state.update_data(comment_message_id=sent_message.message_id)
    await state.set_state(CartForm.comment)


@router.message(UserForm.phone)
async def input_phone(
        message: Message,
        state: FSMContext) -> SendMessage:
    """Запоминает номер телефона клиента."""
    phone = validate_phone_number(message.text.strip())
    api_backend.users.update_phone(message.from_user.id, phone)
    data = await state.get_data()
    await delete_previous_message(data.pop('phone_message_id'), message)
    await state.clear()
    sent_message = await message.answer(text=MessagesConstants.REQUEST_COMMENT)
    await state.update_data(comment_message_id=sent_message.message_id)
    await state.set_state(CartForm.comment)


@router.message(CartForm.comment)
async def input_comment(
        message: Message,
        state: FSMContext) -> SendMessage:
    """Запоминает комментарий к заказу."""
    comment = validate_message_is_text(message)
    api_backend.users.update_comment(message.from_user.id, comment)
    data = await state.get_data()
    await delete_previous_message(data.pop('comment_message_id'), message)
    await state.clear()
    cart = api_backend.users.get_cart(message.from_user.id)
    text = get_cart_detail(cart, pre_order=True)
    await message.answer(
        text=text,
        reply_markup=create_order_keyboard
    )
