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
    if parsed.path not in ("", "/") or parsed.query or parsed.fragment:
        raise ValueError(
            "TELEGRAM_PROXY must point to a forward proxy server and must not "
            "include a path, query, or fragment. Use TELEGRAM_API_BASE_URL for "
            "reverse proxy URLs."
        )

    return proxy_url


def normalize_base_url(base_url: str | None, config_name: str) -> str | None:
    """Return a valid Telegram Bot API base URL or None when disabled."""
    if base_url is None:
        return None

    base_url = base_url.strip()
    if not base_url:
        return None

    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"{config_name} must start with http:// or https://.")
    if not parsed.hostname:
        raise ValueError(f"{config_name} must include a host.")
    if parsed.query or parsed.fragment:
        raise ValueError(f"{config_name} must not include query or fragment.")

    return base_url.rstrip("/")
