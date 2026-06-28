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


@pytest.fixture
def team_statistics_seasons_response():
    return load_fixture("team_statistics_seasons.json")


@pytest.fixture
def team_statistics_response():
    return load_fixture("team_statistics.json")


@pytest.fixture
def team_last_events_responses():
    return {
        0: load_fixture("team_last_events_page0.json"),
        1: load_fixture("team_last_events_page1.json"),
    }


@pytest_asyncio.fixture
async def mock_client(
    team_info_response,
    team_players_response,
    search_response,
    team_statistics_seasons_response,
    team_statistics_response,
    team_last_events_responses,
):
    """Client with mocked HTTP responses for unit tests."""
    client = SofaScoreClient(base_url="https://api.sofascore.com")

    async def mock_get(path: str, params: dict | None = None):
        if path.startswith("/api/v1/team/") and path.endswith("/players"):
            return team_players_response
        if path.endswith("/statistics/seasons") and "/player/" not in path:
            return team_statistics_seasons_response
        if "/player/" in path and path.endswith("/statistics/seasons"):
            return load_fixture("player_statistics_seasons.json")
        if "/player/" in path and "/statistics/" in path:
            return load_fixture("player_statistics.json")
        if "/player/" in path and path.endswith("/transfer-history"):
            return load_fixture("player_transfers.json")
        if path.startswith("/api/v1/player/"):
            return load_fixture("player_detail.json")
        if "/team/" in path and "/statistics/" in path:
            return team_statistics_response
        if "/events/last/" in path:
            page = int(path.rsplit("/", 1)[-1])
            return team_last_events_responses.get(
                page, {"events": [], "hasNextPage": False}
            )
        if path.startswith("/api/v1/team/"):
            return team_info_response
        if path == "/v1/search/all":
            if params and params.get("page", 0) > 0:
                return {"results": []}
            return search_response
        if path.startswith("/api/v1/event/") and path.endswith("/statistics"):
            return load_fixture("event_statistics.json")
        if path.startswith("/api/v1/event/") and path.endswith("/lineups"):
            return load_fixture("event_lineups.json")
        if path.startswith("/api/v1/event/") and path.endswith("/incidents"):
            return load_fixture("event_incidents.json")
        if path.startswith("/api/v1/event/"):
            return load_fixture("event_detail.json")
        if path.endswith("/events/live"):
            return load_fixture("live_events.json")
        if path.endswith("/categories"):
            return load_fixture("categories.json")
        if path.endswith("/unique-tournaments"):
            return load_fixture("unique_tournaments.json")
        if "/unique-tournament/" in path and path.endswith("/seasons"):
            return load_fixture("tournament_seasons.json")
        if "/standings/" in path:
            return load_fixture("standings.json")
        raise AssertionError(f"Unexpected API path: {path}")

    client.http.get = AsyncMock(side_effect=mock_get)
    await client.http.open()
    yield client
    await client.close()
