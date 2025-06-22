from aiogram.types import InlineKeyboardButton

from handlers.keyboards.base import get_form_keyboard


def generate_phone_buttons(phone: str):
    """Генерирует кнопки выбора номера телефона."""
    buttons = [
        InlineKeyboardButton(text=phone, callback_data='exist_phone')
    ]
    buttons.append(new_phone_button)
    return get_form_keyboard(*buttons)


new_phone_button = InlineKeyboardButton(
    text='Новый',
    callback_data='new_phone'
)
