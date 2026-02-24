from aiogram.types import Message, CallbackQuery

from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from app.messages import START_WELCOME, SHOW_MUSCLES

from app.database.db import db
import app.bot.keyboards as kb
from app.bot.states import AddMuscleState


router = Router()

@router.message(CommandStart())
async def cmd_start(msg: Message):
    await msg.answer(text=START_WELCOME, reply_markup=kb.commands)

    # Check if user is in db if no, add
    user_id = msg.from_user.id
    if user_id not in await db.get_users():
        await db.add_user(user_id)


@router.message(Command("show_my_muscles"))
async def cmd_show_user_muscles(msg: Message):
    """Returns message with inline keyboard where already trained, untrained and recoveing muscles are displayed.
    Upon click muscle is couned as trained and updated"""
    user_id = msg.from_user.id
    await msg.answer(text=SHOW_MUSCLES, reply_markup=await kb.create_muscles_inline(user_id))


@router.callback_query(F.data.startswith("update_muscle"))
async def update_muscle(callback: CallbackQuery):
    user_id = callback.from_user.id
    muscle = callback.data.split("_")[-1]
    await callback.answer(f"You trained {muscle}")
    await callback.message.edit_text("Processing... 🔄")

    if not await db.update_user_muscle(user_id, muscle):
        await callback.message.edit_text("An error occured", reply_markup=await kb.create_muscles_inline(user_id))
        return

    await callback.message.edit_text("Updated ✅", reply_markup=await kb.create_muscles_inline(user_id))


@router.message(Command("add_muscle"))
async def cmd_add_user_muscle(msg: Message, state: FSMContext):
    await state.set_state(AddMuscleState.muscle_name)
    await msg.answer("Enter new muscle name:")


@router.message(AddMuscleState.muscle_name)
async def get_user_muscle_name(msg: Message, state: FSMContext):
    if "_$@#%^&" in msg.text:
        await msg.answer("Incorrect muscle name!\nPlease do not use special symbols(_$@#%^&)")
        await state.clear()
        return
    await state.update_data({"muscle_name": msg.text})
    data = await state.get_data()

    if await db.add_user_muscle(msg.from_user.id, data["muscle_name"]):
        await msg.answer("Added new muscle!")
    else:
        await msg.answer("Sorry, an error occured, try again later")

    await state.clear()


@router.message(Command("remove_muscle"))
async def cmd_remove_user_muscle(msg: Message):
    user_id = msg.from_user.id
    await msg.answer(text="Choose muscle to remove", reply_markup=await kb.create_muscle_remove_inline(user_id))


@router.callback_query(F.data.startswith("remove_muscle"))
async def remove_user_muscle(callback: CallbackQuery):
    user_id = callback.from_user.id
    muscle = callback.data.split("_")[-1]
    await callback.answer(f"You are removing {muscle} from tracking")
    await callback.message.edit_text("Processing... 🔄")
    if not await db.remove_user_muscle(user_id, muscle):
        await callback.message.edit_text("An error occured")
        return

    await callback.message.edit_text("Updated ✅")