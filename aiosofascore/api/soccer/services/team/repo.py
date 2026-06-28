from aiosofascore.api.soccer.services.team.models import (
    TeamPerformanceResponse,
    TeamLastEventsResponse,
    TeamPlayersResponse,
    TeamRankingsResponse,
    TeamTransfersResponse,
    TeamStatisticsSeasonsResponse,
    TeamStatisticsResponse,
)
from aiosofascore.api.soccer.services.team.common import TeamInfo
from aiosofascore.api.soccer.services.team.base import BaseRepository


class TeamPerformanceRepository(BaseRepository):
    async def get_performance(self, team_id: int) -> TeamPerformanceResponse:
        url = f"/api/v1/team/{team_id}/performance"
        return await self._get(url, TeamPerformanceResponse)


class TeamInfoRepository(BaseRepository):
    async def get_team_info(self, team_id: int) -> TeamInfo:
        url = f"/api/v1/team/{team_id}"
        data = await self._get_json(url)
        if "team" in data:
            data = data["team"]
        return TeamInfo(**data)


class TeamLastEventsRepository(BaseRepository):
    async def get_last_events(
        self, team_id: int, page: int = 0
    ) -> TeamLastEventsResponse:
        url = f"/api/v1/team/{team_id}/events/last/{page}"
        return await self._get(url, TeamLastEventsResponse)


class TeamPlayersRepository(BaseRepository):
    async def get_team_players(self, team_id: int) -> TeamPlayersResponse:
        url = f"/api/v1/team/{team_id}/players"
        return await self._get(url, TeamPlayersResponse)


class TeamRankingsRepository(BaseRepository):
    async def get_team_rankings(self, team_id: int) -> TeamRankingsResponse:
        url = f"/api/v1/team/{team_id}/rankings"
        return await self._get(url, TeamRankingsResponse)


class TeamTransfersRepository(BaseRepository):
    async def get_team_transfers(self, team_id: int) -> TeamTransfersResponse:
        url = f"/api/v1/team/{team_id}/transfers"
        return await self._get(url, TeamTransfersResponse)


class TeamStatisticsSeasonsRepository(BaseRepository):
    async def get_statistics_seasons(
        self, team_id: int
    ) -> TeamStatisticsSeasonsResponse:
        url = f"/api/v1/team/{team_id}/statistics/seasons"
        return await self._get(url, TeamStatisticsSeasonsResponse)


class TeamStatisticsRepository(BaseRepository):
    async def get_statistics(
        self,
        team_id: int,
        tournament_id: int,
        season_id: int,
        filter: str = "overall",
    ) -> TeamStatisticsResponse:
        url = (
            f"/api/v1/team/{team_id}/unique-tournament/{tournament_id}"
            f"/season/{season_id}/statistics/{filter}"
        )
        return await self._get(url, TeamStatisticsResponse)
