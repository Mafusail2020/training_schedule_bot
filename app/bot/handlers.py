from aiogram.types import Message, CallbackQuery

from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from app.messages import START_WELCOME, SHOW_MUSCLES

from app.database.db import db
import app.bot.keyboards as kb


router = Router()

@router.message(CommandStart())
async def cmd_start(msg: Message):
    await msg.answer(text=START_WELCOME, reply_markup=kb.commands)

    # Check if user is in db if no, add
    user_id = msg.from_user.id
    if user_id not in db.get_users():
        await db.add_user(user_id)


@router.message(Command("show_my_muscles"))
async def cmd_show_user_muscles(msg: Message):
    """Returns message with inline keyboard where already trained, untrained and recoveing muscles are displayed.
    Upon click muscle is couned as trained and updated"""
    user_id = msg.from_user.id
    await msg.answer(text=SHOW_MUSCLES, reply_markup=await kb.create_muscles_inline(user_id))


@router.callback_query(F.data.startswith("update_muscle"))
async def update_muscle(callback: CallbackQuery):
    user_id = callback
    muscle = callback.data.split("_")[-1]
    await callback.answer("You trained this muscle")
    await callback.message.edit_text("Processing... 🔄")

    if not await db.update_user_muscle(user_id, muscle):
        await callback.message.edit_text("An error occured", reply_markup=await kb.create_muscles_inline(user_id))
        return

    await callback.message.edit_text("Updated ✅", reply_markup=await kb.create_muscles_inline(user_id))