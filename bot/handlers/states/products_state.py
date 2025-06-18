from aiogram.fsm.state import StatesGroup, State


class ProductForm(StatesGroup):
    product = State()
    quantity = State()
    message_id = State()
