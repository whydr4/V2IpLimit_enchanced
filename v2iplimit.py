"""
v2iplimit.py is the
main file that run other files and functions to run the program.
"""

import argparse
import asyncio
import time

from run_telegram import run_telegram_bot
from telegram_bot.send_message import send_logs
from utils.check_usage import run_check_users_usage
from utils.get_logs import (
    TASKS,
    check_and_add_new_nodes,
    create_node_task,
    create_panel_task,
    handle_cancel,
    handle_cancel_all,
)
from utils.handel_dis_users import DisabledUsers
from utils.logs import logger
from utils.panel_api import (
    enable_dis_user,
    enable_selected_users,
    get_nodes,
)
from utils.read_config import read_config
from utils.types import PanelType

VERSION = "1.0.13"

parser = argparse.ArgumentParser(description="Help message")
parser.add_argument("--version", action="version", version=VERSION)
args = parser.parse_args()

dis_obj = DisabledUsers()


async def main():
    """Main function to run the code."""
    print("Telegram Bot running...")
    asyncio.create_task(run_telegram_bot())
    await asyncio.sleep(2)
    last_config_error = None
    while True:
        try:
            config_file = await read_config(check_required_elements=True)
            break
        except ValueError as error:
            error_message = str(error)
            logger.warning("Waiting for panel configuration: %s", error_message)
            if error_message != last_config_error:
                last_config_error = error_message
                await send_logs(
                    "<b>V2IpLimit is waiting for panel configuration.</b>\n"
                    + "<code>"
                    + error_message
                    + "</code>\n\n"
                    + "Please fill the required settings through Telegram:\n"
                    + "/create_config: <code>Config panel information (username, password,...)</code>\n"
                    + "/country_code: <code>Set your country code"
                    + " (to increase accuracy)</code>\n"
                    + "/set_general_limit_number: <code>Set the general limit number</code>\n"
                    + "/set_check_interval: <code>Set the check interval time</code>\n"
                    + "/set_time_to_active_users: <code>Set the time to active users</code>\n"
                    + "\nThe limiter will start automatically after the config is complete."
                )
            await asyncio.sleep(60)
    panel_data = PanelType(
        config_file["PANEL_USERNAME"],
        config_file["PANEL_PASSWORD"],
        config_file["PANEL_DOMAIN"],
    )
    dis_users = await dis_obj.read_and_clear_users()
    await enable_selected_users(panel_data, dis_users)
    await get_nodes(panel_data)
    async with asyncio.TaskGroup() as tg:
        print("Start Create Panel Task Test: ")
        await create_panel_task(panel_data, tg)
        await asyncio.sleep(5)
        nodes_list = await get_nodes(panel_data)
        if nodes_list and not isinstance(nodes_list, ValueError):
            print("Start Create Nodes Task Test: ")
            for node in nodes_list:
                if node.status == "connected":
                    await create_node_task(panel_data, tg, node)
                    await asyncio.sleep(4)
        print("Start 'check_and_add_new_nodes' Task Test: ")
        tg.create_task(
            check_and_add_new_nodes(panel_data, tg),
            name="add_new_nodes",
        )
        print("Start 'handle_cancel' Task Test: ")
        tg.create_task(
            handle_cancel(panel_data, TASKS),
            name="cancel_disable_nodes",
        )
        tg.create_task(
            handle_cancel_all(TASKS, panel_data),
            name="cancel_all",
        )
        tg.create_task(
            enable_dis_user(panel_data),
            name="enable_dis_user",
        )
        await run_check_users_usage(panel_data)


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as er:  # pylint: disable=broad-except
            logger.error(er)
            time.sleep(10)
