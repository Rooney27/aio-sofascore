from aiosofascore.api.soccer.services.live.models import LiveEventsResponse
from aiosofascore.api.soccer.services.live.repo import LiveRepository


class LiveService:
    def __init__(self, repository: LiveRepository):
        self.repository = repository

    async def get_live_events(self, sport: str = "football") -> LiveEventsResponse:
        return await self.repository.get_live_events(sport=sport)
