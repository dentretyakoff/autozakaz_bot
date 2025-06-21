from aiogram.fsm.state import StatesGroup, State


class CartForm(StatesGroup):
    comment = State()
    comment_message_id = State()
