from aiogram.types import InlineKeyboardButton

from handlers.keyboards import (
    back_to_main_button,
    get_form_keyboard
)


def generate_products_buttons(products: list):
    """Генерирует кнопки выбора товара."""
    buttons = []
    for product in products:
        title = f'{product.get("manufacturer")} - {product.get("price")} ₽'
        buttons.append(
            InlineKeyboardButton(
                text=title,
                callback_data=f'product_id_{product.get("id")}'))
    buttons.append(back_to_main_button)
    return get_form_keyboard(*buttons)


def generate_product_buttons():
    """Генерирует кнопки доавления товара в корзину."""
    buttons = []
    buttons.append(
        InlineKeyboardButton(
            text='⬅️ Назад к списку товаров',
            callback_data='back_to_results')
    )
    return get_form_keyboard(*buttons)
