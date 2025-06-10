import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.methods import SendMessage

from api import api_backend
from core.constants import MessagesConstants
from core.validators import validate_search_query
from handlers.keyboards import back_to_main_keyboard
from handlers.states import Search
from .utils import delete_previous_message


router = Router()

logger = logging.getLogger(__name__)


@router.callback_query(F.data == 'start_search_products')
async def start_search_products(
        callback_query: CallbackQuery,
        state: FSMContext) -> SendMessage:
    """Старт поиска товаров."""
    sent_message = await callback_query.message.edit_text(
        MessagesConstants.START_SEARCH,
        reply_markup=back_to_main_keyboard
    )
    await state.update_data(message_id=sent_message.message_id)
    await state.set_state(Search.query)


@router.message(Search.query)
async def handle_search_query(message: Message, state: FSMContext):
    """Поиск товаров."""
    query = validate_search_query(message.text)
    data = await state.get_data()
    await delete_previous_message(data.get('message_id'), message)
    sent_message = await message.answer(MessagesConstants.WAITING_SEARCH)
    response = api_backend.products.search_products(query)

    if not response:
        await delete_previous_message(sent_message.message_id, message)
        sent_message = await message.answer(
            text=MessagesConstants.NOT_FOUND,
            reply_markup=back_to_main_keyboard
        )
        await state.update_data(message_id=sent_message.message_id)
        await state.set_state(Search.query)
    else:
        await delete_previous_message(sent_message.message_id, message)
        for product in response:
            await message.answer(
                (f"🔧 {product['name']}\n"
                 f"Код: {product['code']}\n"
                 f"Цена: {product['price']} ₽")
            )
        await state.clear()
