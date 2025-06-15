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
gdpr_confirm_button = InlineKeyboardButton(
    text='✅ Cогласен',
    callback_data='gdpr_confirm'
)


main_menu_keyboard = get_form_keyboard(
    start_search_products_button,
    contacts_button,
)
gdpr_confirm_keyboard = get_form_keyboard(
    gdpr_confirm_button
)
