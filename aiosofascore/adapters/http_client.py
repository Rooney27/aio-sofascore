import asyncio
import json
import os
from typing import Any

from aiohttp import ClientSession

from aiosofascore.exception import ResponseParseContentError

__all__ = ["HttpSessionManager", "DEFAULT_BASE_URL", "DEFAULT_HEADERS"]

DEFAULT_BASE_URL = "https://api.sofascore.com"
DEFAULT_HEADERS = {
    "accept": "application/json",
    "accept-language": "ru,en;q=0.9",
    "cache-control": "no-cache",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    ),
    "referer": "https://www.sofascore.com/",
    "origin": "https://www.sofascore.com",
    "accept-encoding": "gzip, deflate, br",
    "connection": "keep-alive",
}
RETRYABLE_STATUS_CODES = {403, 429, 500, 502, 503, 504}


def _cookies_from_env() -> dict[str, str]:
    raw = os.getenv("SOFASCORE_COOKIES")
    if not raw:
        return {}
    return json.loads(raw)


class HttpSessionManager:
    """Manages a reusable aiohttp session for SofaScore API requests."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        cookies: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        proxy: str | None = None,
        max_retries: int = 3,
        retry_base_delay: float = 1.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.cookies = {**_cookies_from_env(), **(cookies or {})}
        self.headers = {**DEFAULT_HEADERS, **(headers or {})}
        self.proxy = proxy or os.getenv("SOFASCORE_PROXY")
        self.max_retries = max_retries
        self.retry_base_delay = retry_base_delay
        self._session: ClientSession | None = None

    @property
    def is_open(self) -> bool:
        return self._session is not None and not self._session.closed

    async def open(self) -> None:
        if self.is_open:
            return
        self._session = ClientSession(headers=self.headers, cookies=self.cookies)

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None

    async def __aenter__(self) -> "HttpSessionManager":
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    def set_cookies(self, cookies: dict[str, str]) -> None:
        """Update cookies for subsequent requests."""
        self.cookies.update(cookies)
        if self._session:
            self._session.cookie_jar.update_cookies(cookies)

    async def get(self, path: str, params: dict | None = None) -> Any:
        """
        Execute an HTTP GET request and return parsed JSON.

        Opens the session lazily on first use. Retries transient errors
        (403 challenge, 429 rate limit, 5xx) with exponential backoff.
        """
        if not self.is_open:
            await self.open()

        params = params or {}
        url = f"{self.base_url}{path}"

        for attempt in range(self.max_retries + 1):
            assert self._session is not None
            async with self._session.get(
                url, params=params, allow_redirects=False, proxy=self.proxy
            ) as response:
                if response.ok:
                    return await response.json()

                if (
                    response.status in RETRYABLE_STATUS_CODES
                    and attempt < self.max_retries
                ):
                    delay = self.retry_base_delay * (2**attempt)
                    await asyncio.sleep(delay)
                    continue

                raise ResponseParseContentError(response, path)

        raise RuntimeError("Unexpected retry loop exit")
