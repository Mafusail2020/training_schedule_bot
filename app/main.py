from app.bot.bot import bot, dp
import asyncio
import logging
from app.database.db import db

async def main():
    await db.connect()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[#] PROG EXIT")
