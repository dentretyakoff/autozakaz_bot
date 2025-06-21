from datetime import datetime

from aiogram.types import InlineKeyboardButton

from core.settings import FRONTEND_URL
from core.constants import OrderStatus
from handlers.keyboards import (
    get_form_keyboard,
    back_to_main_button,
)


def generate_payment_link_buttons(payment_url: str):
    """Генерирует кнопку оплаты."""
    buttons = []
    if payment_url:
        url = FRONTEND_URL + payment_url
        buttons.append(
            InlineKeyboardButton(text='💳 Оплатить', url=url))
    buttons.append(back_to_main_button)
    return get_form_keyboard(*buttons)


def generate_orders_buttons(orders: dict):
    """Генерирует кнопки истории заказов."""
    buttons = []
    for order in orders:
        status = order.get('status')
        icon = OrderStatus.get_icon(status)
        dt = datetime.fromisoformat(
            order.get('created_at')).strftime("%d.%m.%Y %H:%M")
        buttons.append(
            InlineKeyboardButton(
                text=(f'{icon} {dt} - {order.get("total_price")} ₽'),
                callback_data=f'order_id_{order.get("id")}')
        )
    buttons.append(back_to_main_button)
    return get_form_keyboard(*buttons)


create_order_button = InlineKeyboardButton(
    text='Создать',
    callback_data='create_order'
)
back_to_orders_button = InlineKeyboardButton(
    text='⬅️ Назад к списку заказов',
    callback_data='orders'
)

create_order_keyboard = get_form_keyboard(
    create_order_button,
    back_to_main_button
)
back_to_orders_keyboard = get_form_keyboard(
    back_to_orders_button
)
