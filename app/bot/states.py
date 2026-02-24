from aiogram.fsm.state import State, StatesGroup


class AddMuscleState(StatesGroup):
    muscle_name = State()