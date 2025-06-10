from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_form_keyboard(
        *buttons,
        one_row_buttons: list[InlineKeyboardButton] = None,
        back_button: list[InlineKeyboardButton] = None):
    builder = InlineKeyboardBuilder()
    for button in buttons:
        builder.add(button)
    builder.adjust(1)
    if one_row_buttons:
        builder.row(*one_row_buttons)
    if back_button:
        builder.row(back_button)

    return builder.as_markup()


back_to_main_button = InlineKeyboardButton(
    text='🏠 На главную',
    callback_data='back'
)

back_to_main_keyboard = get_form_keyboard(back_to_main_button)
