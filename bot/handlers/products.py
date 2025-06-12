import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.methods import SendMessage

from api import api_backend
from core.constants import MessagesConstants
from core.validators import validate_search_query
from handlers.keyboards import (
    back_to_main_keyboard,
    generate_products_buttons,
    generate_product_buttons,
    main_menu_keyboard
)
from handlers.states import Search
from .utils import (
    delete_previous_message,
    safe_delete_message,
    make_product_text
)


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
    """Обработчик для показа результатов поиска."""
    query = validate_search_query(message.text)
    data = await state.get_data()
    await state.update_data(query=query)
    await delete_previous_message(data.get('message_id'), message)
    sent_message = await message.answer(MessagesConstants.WAITING_SEARCH)
    products = api_backend.products.search_products(query)
    await delete_previous_message(sent_message.message_id, message)

    if not products:
        sent_message = await message.answer(
            text=MessagesConstants.NOT_FOUND,
            reply_markup=back_to_main_keyboard
        )
        await state.update_data(message_id=sent_message.message_id)
        await state.set_state(Search.query)
    else:
        await message.answer(
            text=MessagesConstants.CHOOSE_PRODUCT,
            reply_markup=generate_products_buttons(products)
        )


@router.callback_query(F.data.startswith('product_id_'))
async def product(callback_query: CallbackQuery) -> SendMessage:
    """Детальная информация о товаре."""
    product_id = int(callback_query.data.split('_')[-1])
    await answer_with_detail_product(
        product_id=product_id,
        message=callback_query.message
    )


@router.callback_query(F.data == 'back_to_results')
async def back_to_results(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    query = data.get('query')
    if not query:
        await callback_query.message.edit_text(
            text=MessagesConstants.HELLO,
            reply_markup=main_menu_keyboard)
        return

    products = api_backend.products.search_products(query, meilisearch=True)
    await callback_query.message.edit_text(
            text=MessagesConstants.CHOOSE_PRODUCT,
            reply_markup=generate_products_buttons(products))


async def answer_with_detail_product(
        product_id: int,
        message: Message | CallbackQuery,
) -> None:
    """Ответ с деталями о товаре."""
    product = api_backend.products.get_product(product_id)
    text = make_product_text(product)
    await safe_delete_message(message)
    await message.answer(
        text=text,
        reply_markup=generate_product_buttons()
    )
