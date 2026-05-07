import sys
import types
import unittest
from unittest.mock import AsyncMock, patch

httpx_stub = types.ModuleType("httpx")
httpx_stub.AsyncClient = object
sys.modules.setdefault("httpx", httpx_stub)

send_message_stub = types.ModuleType("telegram_bot.send_message")
send_message_stub.send_logs = AsyncMock()
sys.modules.setdefault("telegram_bot.send_message", send_message_stub)

panel_api_stub = types.ModuleType("utils.panel_api")
panel_api_stub.disable_user = AsyncMock()
sys.modules.setdefault("utils.panel_api", panel_api_stub)

from utils.check_usage import ACTIVE_USERS
from utils.parse_logs import parse_logs


class ParseLogsTest(unittest.IsolatedAsyncioTestCase):
    def tearDown(self):
        ACTIVE_USERS.clear()

    async def test_parses_client_ip_from_new_xray_from_accepted_format(self):
        log = (
            "2026/05/07 13:37:29.050560 from 109.10.20.30:3320 "
            "accepted udp:1.1.1.1:53 [VLESS TCP REALITY -> silkroad] "
            "email: 76.us_88"
        )

        with patch(
            "utils.parse_logs.read_config",
            new=AsyncMock(return_value={"IP_LOCATION": "None"}),
        ):
            active_users = await parse_logs(log)

        self.assertEqual(active_users["us_88"].ip, ["109.10.20.30"])

    async def test_parses_masked_client_ip_from_new_xray_from_accepted_format(self):
        log = (
            "2026/05/07 13:37:29.050560 from 109.*.*.*:3320 "
            "accepted udp:1.*.*.*:53 [VLESS TCP REALITY -> silkroad] "
            "email: 76.us_88"
        )

        with patch(
            "utils.parse_logs.read_config",
            new=AsyncMock(return_value={"IP_LOCATION": "RU"}),
        ):
            active_users = await parse_logs(log)

        self.assertEqual(active_users["us_88"].ip, ["109.*.*.*"])


if __name__ == "__main__":
    unittest.main()
