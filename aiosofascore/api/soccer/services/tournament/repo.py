from aiosofascore.api.soccer.services.base import BaseRepository
from aiosofascore.api.soccer.services.tournament.models import (
    CategoriesResponse,
    SeasonsResponse,
    StandingsListResponse,
    StandingsResponse,
    UniqueTournamentsResponse,
)


class TournamentRepository(BaseRepository):
    async def get_categories(self, sport: str = "football") -> CategoriesResponse:
        url = f"/api/v1/sport/{sport}/categories"
        return await self._get(url, CategoriesResponse)

    async def get_unique_tournaments(
        self, category_id: int
    ) -> UniqueTournamentsResponse:
        url = f"/api/v1/category/{category_id}/unique-tournaments"
        return await self._get(url, UniqueTournamentsResponse)

    async def get_seasons(self, tournament_id: int) -> SeasonsResponse:
        url = f"/api/v1/unique-tournament/{tournament_id}/seasons"
        return await self._get(url, SeasonsResponse)

    async def get_standings(
        self,
        tournament_id: int,
        season_id: int,
        standing_type: str = "total",
    ) -> StandingsResponse:
        url = (
            f"/api/v1/unique-tournament/{tournament_id}"
            f"/season/{season_id}/standings/{standing_type}"
        )
        data = await self._get(url, StandingsListResponse)
        return data.first or StandingsResponse()
