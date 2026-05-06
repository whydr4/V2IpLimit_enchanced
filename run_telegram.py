"""Run the telegram bot."""

import asyncio

from telegram_bot.main import application
from utils.logs import logger


async def run_telegram_bot():
    """Run the telegram bot."""
    while True:
        initialized = False
        started = False
        polling = False
        try:
            await application.initialize()
            initialized = True
            await application.start()
            started = True
            await application.updater.start_polling()
            polling = True
            while True:
                await asyncio.sleep(40)
        except Exception as error:  # pylint: disable=broad-except
            logger.exception(
                "Telegram bot polling failed: %s. "
                "Check BOT_TOKEN and TELEGRAM_PROXY. "
                "If TELEGRAM_PROXY is set, make sure its scheme matches the proxy "
                "server (http://, https://, socks5://, or socks5h://).",
                error,
            )
        finally:
            if polling:
                try:
                    await application.updater.stop()
                except Exception as error:  # pylint: disable=broad-except
                    logger.exception("Failed to stop Telegram polling: %s", error)
            if started:
                try:
                    await application.stop()
                except Exception as error:  # pylint: disable=broad-except
                    logger.exception("Failed to stop Telegram application: %s", error)
            if initialized:
                try:
                    await application.shutdown()
                except Exception as error:  # pylint: disable=broad-except
                    logger.exception(
                        "Failed to shutdown Telegram application: %s", error
                    )
            await asyncio.sleep(10)
