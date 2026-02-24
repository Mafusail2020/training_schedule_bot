from app.bot.bot import dp
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from app.database.db import db
from typing import List
from datetime import datetime, timedelta

commands = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="/show_my_muscles")],
    [KeyboardButton(text="/history"), KeyboardButton(text="/help")],
    [KeyboardButton(text="/settings")]
], resize_keyboard=True, one_time_keyboard=None, input_field_placeholder="Choose a command")


async def create_muscles_inline(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    user_muscles: dict = db.get_user_muscles()
    for muscle in user_muscles.keys():
        state = __get_muscle_state(last_trained=user_muscles[muscle])

        # Create inline text
        button_text = muscle
        match state:
            case "UNTRAINED":
                button_text = "🔴 " + button_text
                break

            case "READY":
                button_text = "🟢 " + button_text
                break

            case "UNREADY":
                button_text = "🟡 " + button_text
                break
        
        # Create and add button
        btn = InlineKeyboardButton(text=button_text, callback_data=f"update_muscle_{muscle}")
        kb.add(btn)

    return kb.adjust(2).as_markup()
    
async def __get_muscle_state(last_trained):
    """
    Checks if 72 hours have passed since the provided start_time.
    """
    now = datetime.now()
    
    # Calculate the difference
    elapsed_time = now - last_trained
    
    # timedelta(hours=72) is the same as timedelta(days=3)
    if elapsed_time > timedelta(days=10):
        return "UNTRAINED"
    elif elapsed_time > timedelta(hours=60):
        return "READY"
    else:
        return "UNREADY"
