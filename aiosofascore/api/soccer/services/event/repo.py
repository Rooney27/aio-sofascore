from aiosofascore.api.soccer.services.base import BaseRepository
from aiosofascore.api.soccer.services.event.models import (
    EventDetail,
    EventIncidentsResponse,
    EventLineupsResponse,
    EventManagersResponse,
    EventStatisticsResponse,
    H2HResponse,
    PregameFormResponse,
)


class EventRepository(BaseRepository):
    async def get_event(self, event_id: int) -> EventDetail:
        url = f"/api/v1/event/{event_id}"
        return await self._get_wrapped(url, EventDetail, "event")

    async def get_lineups(self, event_id: int) -> EventLineupsResponse:
        url = f"/api/v1/event/{event_id}/lineups"
        return await self._get(url, EventLineupsResponse)

    async def get_statistics(self, event_id: int) -> EventStatisticsResponse:
        url = f"/api/v1/event/{event_id}/statistics"
        return await self._get(url, EventStatisticsResponse)

    async def get_incidents(self, event_id: int) -> EventIncidentsResponse:
        url = f"/api/v1/event/{event_id}/incidents"
        return await self._get(url, EventIncidentsResponse)

    async def get_h2h(self, event_id: int) -> H2HResponse:
        url = f"/api/v1/event/{event_id}/h2h"
        return await self._get(url, H2HResponse)

    async def get_pregame_form(self, event_id: int) -> PregameFormResponse:
        url = f"/api/v1/event/{event_id}/pregame-form"
        return await self._get(url, PregameFormResponse)

    async def get_managers(self, event_id: int) -> EventManagersResponse:
        url = f"/api/v1/event/{event_id}/managers"
        return await self._get(url, EventManagersResponse)
