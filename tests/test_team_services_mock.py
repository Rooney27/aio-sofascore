import pytest

TEAM_ID = 2819


@pytest.mark.asyncio
async def test_get_team_info(mock_client):
    info = await mock_client.team.info.get_team_info(TEAM_ID)
    assert info.id == TEAM_ID
    assert info.name == "Manchester United"
    assert info.slug == "manchester-united"


@pytest.mark.asyncio
async def test_get_team_players(mock_client):
    players = await mock_client.team.players.get_team_players(TEAM_ID)
    assert players.players is not None
    assert len(players.players) == 2
    assert players.players[0].player.name == "Bruno Fernandes"


@pytest.mark.asyncio
async def test_client_context_manager():
    from aiosofascore.client import SofaScoreClient

    async with SofaScoreClient() as client:
        assert client.http.is_open
    assert not client.http.is_open
