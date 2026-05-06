"""Helpers for validating runtime configuration."""

REQUIRED_PANEL_ELEMENTS = [
    "PANEL_DOMAIN",
    "PANEL_USERNAME",
    "PANEL_PASSWORD",
    "CHECK_INTERVAL",
    "TIME_TO_ACTIVE_USERS",
    "IP_LOCATION",
    "GENERAL_LIMIT",
]


def get_missing_required_elements(config_data: dict) -> list[str]:
    """Return required panel settings that are missing or empty."""
    return [
        element
        for element in REQUIRED_PANEL_ELEMENTS
        if config_data.get(element) in (None, "")
    ]
