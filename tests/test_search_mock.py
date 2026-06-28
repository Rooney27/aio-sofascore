import pytest

from aiosofascore.client import SofaScoreClient


@pytest.mark.asyncio
async def test_search_all_entities(mock_client):
    results = []
    async for item in mock_client.search.search.search_entities("Manchester"):
        results.append(item)
    assert len(results) == 2
    assert results[0].type == "team"
    assert results[1].type == "player"


@pytest.mark.asyncio
async def test_search_teams_only(mock_client):
    results = []
    async for item in mock_client.search.search.search_entities(
        "Manchester", type="team"
    ):
        results.append(item)
    assert len(results) == 1
    assert results[0].entity.name == "Manchester United"


@pytest.mark.asyncio
async def test_search_players_only(mock_client):
    results = []
    async for item in mock_client.search.search.search_entities(
        "Manchester", type="player"
    ):
        results.append(item)
    assert len(results) == 1
    assert results[0].entity.name == "Bruno Fernandes"
