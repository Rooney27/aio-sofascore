from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from aiosofascore.adapters.http_client import DEFAULT_BASE_URL, HttpSessionManager
from aiosofascore.exception import ResponseParseContentError


@pytest.mark.asyncio
async def test_default_base_url():
    http = HttpSessionManager(transport="aiohttp")
    assert http.base_url == DEFAULT_BASE_URL


@pytest.mark.asyncio
async def test_session_reuse():
    http = HttpSessionManager(transport="aiohttp")
    await http.open()
    session = http._session
    await http.open()
    assert http._session is session
    await http.close()
    assert not http.is_open


@pytest.mark.asyncio
async def test_context_manager_closes_session():
    async with HttpSessionManager(transport="aiohttp") as http:
        assert http.is_open
    assert not http.is_open


@pytest.mark.asyncio
async def test_lazy_session_open_on_get():
    http = HttpSessionManager(transport="aiohttp", warmup=False)
    assert not http.is_open

    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.ok = True
    mock_response.json = AsyncMock(return_value={"ok": True})
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    mock_session = MagicMock()
    mock_session.closed = False
    mock_session.get = MagicMock(return_value=mock_response)

    with patch.object(http, "open", wraps=http.open) as open_mock:
        with patch.object(HttpSessionManager, "_session", mock_session, create=True):
            http._session = mock_session
            http.transport = "aiohttp"
            result = await http.get("/api/v1/test")
            assert result == {"ok": True}


@pytest.mark.asyncio
async def test_retry_on_retryable_status():
    http = HttpSessionManager(max_retries=2, retry_base_delay=0.01, transport="aiohttp", warmup=False)

    call_count = 0

    def make_response(status: int, ok: bool):
        resp = MagicMock()
        resp.status = status
        resp.ok = ok
        resp.json = AsyncMock(return_value={})
        resp.__aenter__ = AsyncMock(return_value=resp)
        resp.__aexit__ = AsyncMock(return_value=None)
        return resp

    def mock_get(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count <= 2:
            return make_response(429, False)
        success = make_response(200, True)
        success.json = AsyncMock(return_value={"data": "ok"})
        return success

    mock_session = MagicMock()
    mock_session.closed = False
    mock_session.get = mock_get

    http._session = mock_session
    http.transport = "aiohttp"
    result = await http.get("/api/v1/test")
    assert result == {"data": "ok"}
    assert call_count == 3


@pytest.mark.asyncio
async def test_raises_after_max_retries():
    http = HttpSessionManager(max_retries=1, retry_base_delay=0.01, transport="aiohttp", warmup=False)

    resp = MagicMock()
    resp.status = 403
    resp.ok = False
    resp.__aenter__ = AsyncMock(return_value=resp)
    resp.__aexit__ = AsyncMock(return_value=None)

    mock_session = MagicMock()
    mock_session.closed = False
    mock_session.get = MagicMock(return_value=resp)

    http._session = mock_session
    http.transport = "aiohttp"
    with pytest.raises(ResponseParseContentError):
        await http.get("/api/v1/test")


@pytest.mark.asyncio
async def test_set_cookies():
    http = HttpSessionManager(cookies={"test": "value"}, transport="aiohttp")
    assert http.cookies["test"] == "value"
    http.set_cookies({"extra": "cookie"})
    assert http.cookies["extra"] == "cookie"
