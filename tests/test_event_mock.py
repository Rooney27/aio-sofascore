import pytest

EVENT_ID = 11352523


@pytest.mark.asyncio
async def test_get_event(mock_client):
    event = await mock_client.event.get_event(EVENT_ID)
    assert event.id == EVENT_ID
    assert event.homeTeam.name == "Arsenal"
    assert event.awayTeam.name == "Chelsea"


@pytest.mark.asyncio
async def test_get_event_statistics(mock_client):
    stats = await mock_client.event.get_statistics(EVENT_ID)
    assert stats.statistics is not None
    assert stats.statistics[0].groups[0].statisticsItems[0].name == "Ball possession"


@pytest.mark.asyncio
async def test_get_event_lineups(mock_client):
    lineups = await mock_client.event.get_lineups(EVENT_ID)
    assert lineups.confirmed is True
    assert lineups.home["formation"] == "4-3-3"


@pytest.mark.asyncio
async def test_get_event_incidents(mock_client):
    incidents = await mock_client.event.get_incidents(EVENT_ID)
    assert len(incidents.incidents) == 1
    assert incidents.incidents[0].incidentType == "goal"
