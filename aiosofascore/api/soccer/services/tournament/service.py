from aiosofascore.api.soccer.services.tournament.models import (
    CategoriesResponse,
    SeasonsResponse,
    StandingsResponse,
    UniqueTournamentsResponse,
)
from aiosofascore.api.soccer.services.tournament.repo import TournamentRepository


class TournamentService:
    def __init__(self, repository: TournamentRepository):
        self.repository = repository

    async def get_categories(self, sport: str = "football") -> CategoriesResponse:
        return await self.repository.get_categories(sport=sport)

    async def get_unique_tournaments(
        self, category_id: int
    ) -> UniqueTournamentsResponse:
        return await self.repository.get_unique_tournaments(category_id)

    async def get_seasons(self, tournament_id: int) -> SeasonsResponse:
        return await self.repository.get_seasons(tournament_id)

    async def get_standings(
        self,
        tournament_id: int,
        season_id: int,
        standing_type: str = "total",
    ) -> StandingsResponse:
        return await self.repository.get_standings(
            tournament_id, season_id, standing_type=standing_type
        )

    async def get_standings_by_year(
        self,
        tournament_id: int,
        season_year: str | None = None,
        standing_type: str = "total",
    ) -> StandingsResponse:
        seasons = await self.get_seasons(tournament_id)
        if season_year:
            season = seasons.get_season_by_year(season_year)
        else:
            season = seasons.get_current_season()
        if not season or not season.id:
            return StandingsResponse()
        return await self.get_standings(tournament_id, season.id, standing_type)
