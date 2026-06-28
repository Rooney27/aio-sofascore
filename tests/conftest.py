import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from aiosofascore.client import SofaScoreClient

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict:
    with open(FIXTURES_DIR / name, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def team_info_response():
    return load_fixture("team_info.json")


@pytest.fixture
def team_players_response():
    return load_fixture("team_players.json")


@pytest.fixture
def search_response():
    return load_fixture("search_results.json")


@pytest_asyncio.fixture
async def mock_client(team_info_response, team_players_response, search_response):
    """Client with mocked HTTP responses for unit tests."""
    client = SofaScoreClient(base_url="https://api.sofascore.com")

    async def mock_get(path: str, params: dict | None = None):
        if path.startswith("/api/v1/team/") and path.endswith("/players"):
            return team_players_response
        if path.startswith("/api/v1/team/"):
            return team_info_response
        if path == "/v1/search/all":
            if params and params.get("page", 0) > 0:
                return {"results": []}
            return search_response
        raise AssertionError(f"Unexpected API path: {path}")

    client.http.get = AsyncMock(side_effect=mock_get)
    await client.http.open()
    yield client
    await client.close()
