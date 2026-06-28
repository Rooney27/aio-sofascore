import os

import pytest
import pytest_asyncio

from aiosofascore.client import SofaScoreClient

pytestmark = pytest.mark.integration(
    skipif=not os.getenv("SOFASCORE_LIVE"),
    reason="Set SOFASCORE_LIVE=1 to run live API tests",
)


@pytest_asyncio.fixture(scope="module")
async def client():
    async with SofaScoreClient() as client:
        yield client


@pytest.mark.asyncio
async def test_get_live_events(client):
    live = await client.live.get_live_events()
    assert hasattr(live, "events")


@pytest.mark.asyncio
async def test_get_categories(client):
    categories = await client.tournament.get_categories()
    assert hasattr(categories, "categories")


@pytest.mark.asyncio
async def test_get_event(client):
    # Use a known finished event id if available; skip if empty search
    results = []
    async for item in client.search.search_events("Arsenal Chelsea"):
        if item.type == "event":
            results.append(item)
            break
    if not results:
        pytest.skip("No event found via search")
    event_id = results[0].entity.id
    event = await client.event.get_event(event_id)
    assert event.id == event_id
