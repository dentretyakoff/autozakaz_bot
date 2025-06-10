from aiogram.fsm.state import StatesGroup, State


class Search(StatesGroup):
    query = State()
    message_id = State()
