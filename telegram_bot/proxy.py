"""Telegram proxy configuration helpers."""

from urllib.parse import urlparse

SUPPORTED_PROXY_SCHEMES = {"http", "https", "socks5", "socks5h"}


def normalize_proxy_url(proxy_url: str | None) -> str | None:
    """Return a valid proxy URL or None when proxying is disabled."""
    if proxy_url is None:
        return None

    proxy_url = proxy_url.strip()
    if not proxy_url:
        return None

    parsed = urlparse(proxy_url)
    if parsed.scheme not in SUPPORTED_PROXY_SCHEMES:
        supported = ", ".join(sorted(SUPPORTED_PROXY_SCHEMES))
        raise ValueError(
            "Unsupported TELEGRAM_PROXY scheme "
            f"'{parsed.scheme}'. Supported schemes: {supported}."
        )
    if not parsed.hostname:
        raise ValueError("TELEGRAM_PROXY must include a host.")

    return proxy_url
