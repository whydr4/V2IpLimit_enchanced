import unittest

from telegram_bot.proxy import normalize_proxy_url


class NormalizeProxyUrlTest(unittest.TestCase):
    def test_returns_none_for_missing_or_empty_proxy(self):
        self.assertIsNone(normalize_proxy_url(None))
        self.assertIsNone(normalize_proxy_url(""))
        self.assertIsNone(normalize_proxy_url("   "))

    def test_accepts_supported_proxy_schemes(self):
        self.assertEqual(
            normalize_proxy_url(" socks5://user:pass@127.0.0.1:1080 "),
            "socks5://user:pass@127.0.0.1:1080",
        )
        self.assertEqual(
            normalize_proxy_url("http://127.0.0.1:8080"),
            "http://127.0.0.1:8080",
        )
        self.assertEqual(
            normalize_proxy_url("https://proxy.example.com:443"),
            "https://proxy.example.com:443",
        )
        self.assertEqual(
            normalize_proxy_url("socks5h://proxy.example.com:1080"),
            "socks5h://proxy.example.com:1080",
        )

    def test_rejects_unsupported_proxy_schemes(self):
        with self.assertRaisesRegex(ValueError, "Unsupported TELEGRAM_PROXY scheme"):
            normalize_proxy_url("ftp://proxy.example.com:21")

    def test_rejects_proxy_without_host(self):
        with self.assertRaisesRegex(ValueError, "must include a host"):
            normalize_proxy_url("socks5://")


if __name__ == "__main__":
    unittest.main()
