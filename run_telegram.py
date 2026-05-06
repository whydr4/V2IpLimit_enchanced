"""Run the telegram bot."""

import asyncio

from telegram_bot.main import application
from utils.logs import logger


async def run_telegram_bot():
    """Run the telegram bot."""
    while True:
        try:
            async with application:
                await application.start()
                await application.updater.start_polling()
                while True:
                    await asyncio.sleep(40)
        except Exception as error:  # pylint: disable=broad-except
            logger.exception("Telegram bot polling failed: %s", error)
            await asyncio.sleep(10)
