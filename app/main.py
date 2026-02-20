from app.bot.bot import bot, dp
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
