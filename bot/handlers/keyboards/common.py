from aiogram.types import InlineKeyboardButton

from handlers.keyboards.base import get_form_keyboard


start_search_products_button = InlineKeyboardButton(
    text='🔍 Поиск деталей',
    callback_data='start_search_products'
)
contacts_button = InlineKeyboardButton(
    text='📝 Контакты',
    callback_data='contacts'
)


main_menu_keyboard = get_form_keyboard(
    start_search_products_button,
    contacts_button,
)
