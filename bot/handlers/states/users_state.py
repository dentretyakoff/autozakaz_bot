from aiogram.fsm.state import StatesGroup, State


class UserForm(StatesGroup):
    phone = State()
    phone_message_id = State()
