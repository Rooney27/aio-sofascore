import pytest


@pytest.mark.asyncio
async def test_get_categories(mock_client):
    categories = await mock_client.tournament.get_categories()
    assert categories.categories is not None
    assert categories.categories[0].name == "England"


@pytest.mark.asyncio
async def test_get_unique_tournaments(mock_client):
    tournaments = await mock_client.tournament.get_unique_tournaments(1)
    items = tournaments.unique_tournaments
    assert len(items) == 1
    assert items[0].name == "Premier League"


@pytest.mark.asyncio
async def test_get_seasons(mock_client):
    seasons = await mock_client.tournament.get_seasons(17)
    assert seasons.seasons[0].year == "23/24"


@pytest.mark.asyncio
async def test_get_standings(mock_client):
    standings = await mock_client.tournament.get_standings(17, 52186)
    assert standings.rows[0].team.name == "Arsenal"
    assert standings.rows[0].position == 1


@pytest.mark.asyncio
async def test_get_standings_by_year(mock_client):
    standings = await mock_client.tournament.get_standings_by_year(17, "23/24")
    assert standings.rows[0].points == 80
