from aiosofascore.api.soccer.services.base import BaseRepository
from aiosofascore.api.soccer.services.live.models import LiveEventsResponse


class LiveRepository(BaseRepository):
    async def get_live_events(self, sport: str = "football") -> LiveEventsResponse:
        url = f"/api/v1/sport/{sport}/events/live"
        return await self._get(url, LiveEventsResponse)
