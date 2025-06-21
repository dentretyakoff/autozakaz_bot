import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.methods import SendMessage

from api import api_backend
from handlers.keyboards import generate_cart_buttons
from .utils import get_cart_detail

router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == 'cart')
async def cart(callback_query: CallbackQuery) -> SendMessage:
    """Корзина пользователя."""
    cart = api_backend.users.get_cart(callback_query.from_user.id)
    text = get_cart_detail(cart)
    await callback_query.message.edit_text(
        text=text, reply_markup=generate_cart_buttons(cart))


@router.callback_query(F.data == 'clear_cart')
async def clear_cart(callback_query: CallbackQuery) -> SendMessage:
    """Очищает корзину."""
    api_backend.users.clear_cart(callback_query.from_user.id)
    cart = api_backend.users.get_cart(callback_query.from_user.id)
    text = get_cart_detail(cart)
    await callback_query.message.edit_text(
        text=text, reply_markup=generate_cart_buttons(cart))
