from aiogram.types import InlineKeyboardButton

from handlers.keyboards import get_form_keyboard, back_to_main_button


def generate_cart_buttons(cart: dict):
    """Генерирует кнопки в корзине."""
    buttons = []
    items = cart.get('items')
    if len(items) > 0:
        buttons.append(making_order_button)
    buttons.append(back_to_main_button)
    return get_form_keyboard(*buttons)


making_order_button = InlineKeyboardButton(
    text='✍️ К оформлению заказа',
    callback_data='phone'
)
