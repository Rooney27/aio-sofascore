import pytest


@pytest.mark.asyncio
async def test_get_live_events(mock_client):
    live = await mock_client.live.get_live_events()
    assert live.events is not None
    assert len(live.events) == 1
    assert live.events[0].status.type == "inprogress"
