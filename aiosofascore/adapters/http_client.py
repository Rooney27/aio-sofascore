import asyncio
import json
import os
from typing import Any, Literal

from aiohttp import ClientSession

from aiosofascore.exception import ResponseParseContentError

__all__ = [
    "HttpSessionManager",
    "DEFAULT_BASE_URL",
    "DEFAULT_HEADERS",
    "parse_cookie_header",
    "load_cookies_from_file",
]

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
Transport = Literal["auto", "aiohttp", "curl"]


def _curl_available() -> bool:
    try:
        import curl_cffi  # noqa: F401

        return True
    except ImportError:
        return False


def parse_cookie_header(header: str) -> dict[str, str]:
    """Convert a DevTools Cookie header string to a dict."""
    cookies: dict[str, str] = {}
    for part in header.split(";"):
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            cookies[key.strip()] = value.strip()
    return cookies


def load_cookies_from_file(path: str) -> dict[str, str]:
    """Load cookies from JSON file or a raw Cookie header text file."""
    with open(path, encoding="utf-8") as file:
        raw = file.read().strip()
    if not raw:
        return {}
    if raw.startswith("{"):
        return json.loads(raw)
    return parse_cookie_header(raw)


def _cookies_from_env() -> dict[str, str]:
    raw = os.getenv("SOFASCORE_COOKIES")
    if raw:
        raw = raw.strip()
        if raw.startswith("{"):
            return json.loads(raw)
        return parse_cookie_header(raw)
    cookie_file = os.getenv("SOFASCORE_COOKIES_FILE")
    if cookie_file:
        return load_cookies_from_file(cookie_file)
    return {}


def _resolve_transport(transport: Transport | None) -> Literal["aiohttp", "curl"]:
    chosen = transport or os.getenv("SOFASCORE_TRANSPORT", "auto")
    if chosen == "auto":
        return "curl" if _curl_available() else "aiohttp"
    if chosen == "curl" and not _curl_available():
        raise ImportError(
            "curl_cffi is required for transport='curl'. "
            "Install with: pip install 'aiosofascore[curl]'"
        )
    return chosen


class HttpSessionManager:
    """Manages reusable HTTP sessions for SofaScore API requests."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        cookies: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        proxy: str | None = None,
        max_retries: int = 3,
        retry_base_delay: float = 1.0,
        transport: Transport | None = None,
        impersonate: str | None = None,
        warmup: bool | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.cookies = {**_cookies_from_env(), **(cookies or {})}
        self.headers = {**DEFAULT_HEADERS, **(headers or {})}
        self.proxy = proxy or os.getenv("SOFASCORE_PROXY")
        self.max_retries = max_retries
        self.retry_base_delay = retry_base_delay
        self.transport = _resolve_transport(transport)
        self.impersonate = impersonate or os.getenv("SOFASCORE_IMPERSONATE", "chrome")
        self.warmup = (
            warmup
            if warmup is not None
            else os.getenv("SOFASCORE_WARMUP", "1") != "0"
        )
        self._session: Any = None
        self._warmed_up = False

    @property
    def is_open(self) -> bool:
        if self._session is None:
            return False
        if self.transport == "aiohttp":
            return not self._session.closed
        return True

    async def open(self) -> None:
        if self.is_open:
            return
        if self.transport == "curl":
            from curl_cffi.requests import AsyncSession

            self._session = AsyncSession(
                impersonate=self.impersonate,
                headers=self.headers,
                cookies=self.cookies,
            )
        else:
            self._session = ClientSession(headers=self.headers, cookies=self.cookies)

    async def close(self) -> None:
        if self._session is None:
            return
        if self.transport == "aiohttp":
            if not self._session.closed:
                await self._session.close()
        else:
            await self._session.close()
        self._session = None
        self._warmed_up = False

    async def __aenter__(self) -> "HttpSessionManager":
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    def set_cookies(self, cookies: dict[str, str]) -> None:
        self.cookies.update(cookies)
        if self._session and self.transport == "aiohttp":
            self._session.cookie_jar.update_cookies(cookies)
        elif self._session and self.transport == "curl":
            self._session.cookies.update(cookies)

    async def _warmup_session(self) -> None:
        if not self.warmup or self._warmed_up:
            return
        if self.transport == "curl":
            await self._session.get("https://www.sofascore.com/", allow_redirects=True)
        self._warmed_up = True

    async def get(self, path: str, params: dict | None = None) -> Any:
        if not self.is_open:
            await self.open()
        await self._warmup_session()

        params = params or {}
        url = f"{self.base_url}{path}"

        for attempt in range(self.max_retries + 1):
            if self.transport == "curl":
                response = await self._curl_get(url, params)
                status = response.status_code
                if 200 <= status < 300:
                    return response.json()
                if status in RETRYABLE_STATUS_CODES and attempt < self.max_retries:
                    await asyncio.sleep(self.retry_base_delay * (2**attempt))
                    continue
                raise ResponseParseContentError(response, path)
            else:
                async with self._session.get(
                    url, params=params, allow_redirects=False, proxy=self.proxy
                ) as response:
                    status = response.status
                    if 200 <= status < 300:
                        return await response.json()
                    if status in RETRYABLE_STATUS_CODES and attempt < self.max_retries:
                        await asyncio.sleep(self.retry_base_delay * (2**attempt))
                        continue
                    raise ResponseParseContentError(response, path)

        raise RuntimeError("Unexpected retry loop exit")

    async def _curl_get(self, url: str, params: dict) -> Any:
        assert self._session is not None
        return await self._session.get(
            url,
            params=params,
            allow_redirects=False,
            proxy=self.proxy,
            headers=self.headers,
            cookies=self.cookies,
        )
