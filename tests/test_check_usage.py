import unittest
import sys
import types
from unittest.mock import AsyncMock, patch

send_message_stub = types.ModuleType("telegram_bot.send_message")
send_message_stub.send_logs = AsyncMock()
sys.modules.setdefault("telegram_bot.send_message", send_message_stub)
panel_api_stub = types.ModuleType("utils.panel_api")
panel_api_stub.disable_user = AsyncMock()
sys.modules.setdefault("utils.panel_api", panel_api_stub)

from utils.check_usage import ACTIVE_USERS, check_ip_used
from utils.types import UserType


class CheckIpUsedTest(unittest.IsolatedAsyncioTestCase):
    def tearDown(self):
        ACTIVE_USERS.clear()

    async def test_counts_unique_ips_seen_once_during_interval(self):
        ACTIVE_USERS["alice"] = UserType(
            name="alice",
            ip=["203.0.113.10", "198.51.100.20"],
        )

        with patch("utils.check_usage.send_logs", new_callable=AsyncMock):
            all_users_log = await check_ip_used()

        self.assertEqual(
            set(all_users_log["alice"]),
            {"203.0.113.10", "198.51.100.20"},
        )


if __name__ == "__main__":
    unittest.main()
