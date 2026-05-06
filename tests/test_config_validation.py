import unittest

from utils.config_validation import get_missing_required_elements


class GetMissingRequiredElementsTest(unittest.TestCase):
    def test_returns_missing_required_panel_elements(self):
        config = {
            "BOT_TOKEN": "token",
            "ADMINS": [123],
            "PANEL_USERNAME": "admin",
            "PANEL_PASSWORD": "",
        }

        self.assertEqual(
            get_missing_required_elements(config),
            [
                "PANEL_DOMAIN",
                "PANEL_PASSWORD",
                "CHECK_INTERVAL",
                "TIME_TO_ACTIVE_USERS",
                "IP_LOCATION",
                "GENERAL_LIMIT",
            ],
        )

    def test_returns_empty_list_when_required_elements_are_present(self):
        config = {
            "PANEL_DOMAIN": "example.com:8000",
            "PANEL_USERNAME": "admin",
            "PANEL_PASSWORD": "secret",
            "CHECK_INTERVAL": 240,
            "TIME_TO_ACTIVE_USERS": 600,
            "IP_LOCATION": "None",
            "GENERAL_LIMIT": 2,
        }

        self.assertEqual(get_missing_required_elements(config), [])


if __name__ == "__main__":
    unittest.main()
