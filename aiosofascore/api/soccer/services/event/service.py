from aiosofascore.api.soccer.services.event.models import (
    EventDetail,
    EventIncidentsResponse,
    EventLineupsResponse,
    EventManagersResponse,
    EventStatisticsResponse,
    H2HResponse,
    PregameFormResponse,
)
from aiosofascore.api.soccer.services.event.repo import EventRepository


class EventService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def get_event(self, event_id: int) -> EventDetail:
        return await self.repository.get_event(event_id)

    async def get_lineups(self, event_id: int) -> EventLineupsResponse:
        return await self.repository.get_lineups(event_id)

    async def get_statistics(self, event_id: int) -> EventStatisticsResponse:
        return await self.repository.get_statistics(event_id)

    async def get_incidents(self, event_id: int) -> EventIncidentsResponse:
        return await self.repository.get_incidents(event_id)

    async def get_h2h(self, event_id: int) -> H2HResponse:
        return await self.repository.get_h2h(event_id)

    async def get_pregame_form(self, event_id: int) -> PregameFormResponse:
        return await self.repository.get_pregame_form(event_id)

    async def get_managers(self, event_id: int) -> EventManagersResponse:
        return await self.repository.get_managers(event_id)
