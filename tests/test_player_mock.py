import pytest

PLAYER_ID = 12345
TOURNAMENT_ID = 17
SEASON_ID = 52186


@pytest.mark.asyncio
async def test_get_player(mock_client):
    player = await mock_client.player.get_player(PLAYER_ID)
    assert player.id == PLAYER_ID
    assert player.name == "Bruno Fernandes"


@pytest.mark.asyncio
async def test_get_player_statistics_seasons(mock_client):
    seasons = await mock_client.player.get_statistics_seasons(PLAYER_ID)
    assert seasons.uniqueTournamentSeasons[0].uniqueTournament.name == "Premier League"


@pytest.mark.asyncio
async def test_get_player_statistics(mock_client):
    stats = await mock_client.player.get_statistics(PLAYER_ID, TOURNAMENT_ID, SEASON_ID)
    assert stats.statistics["goals"] == 15


@pytest.mark.asyncio
async def test_get_player_transfers(mock_client):
    transfers = await mock_client.player.get_transfers(PLAYER_ID)
    assert transfers.transferHistory[0].toTeamName == "Manchester United"
