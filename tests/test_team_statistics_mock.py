import pytest

TEAM_ID = 2819
TOURNAMENT_ID = 17
SEASON_ID = 52186


@pytest.mark.asyncio
async def test_get_statistics_seasons(mock_client):
    result = await mock_client.team.statistics_seasons.get_statistics_seasons(TEAM_ID)
    assert result.uniqueTournamentSeasons is not None
    assert len(result.uniqueTournamentSeasons) == 1
    item = result.uniqueTournamentSeasons[0]
    assert item.uniqueTournament.name == "Premier League"
    assert len(item.seasons) == 2


@pytest.mark.asyncio
async def test_get_statistics(mock_client):
    result = await mock_client.team.statistics.get_statistics(
        TEAM_ID, TOURNAMENT_ID, SEASON_ID
    )
    assert result.statistics is not None
    assert result.statistics["goalsScored"] == 57
    assert result.statistics["matches"] == 38


@pytest.mark.asyncio
async def test_iter_last_events(mock_client):
    events = []
    async for event in mock_client.team.last_events.iter_last_events(TEAM_ID):
        events.append(event)
    assert len(events) == 2
    assert events[0].id == 1001
    assert events[1].id == 1002
