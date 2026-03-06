from aiogram.fsm.state import State, StatesGroup


class RegistrationProfile(StatesGroup):
    waiting_name = State()
    waiting_age = State()
    waiting_city = State()