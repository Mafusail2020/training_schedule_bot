from aiogram import Bot, Dispatcher
from app.bot.handlers import router
from app.config import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher()
dp.include_router(router)
