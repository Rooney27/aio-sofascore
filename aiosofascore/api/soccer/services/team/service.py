from typing import AsyncGenerator

from aiosofascore.api.soccer.services.team.common import TeamInfo
from aiosofascore.api.soccer.services.team.models import (
    PerformanceEvent,
    TeamLastEventsResponse,
    TeamPerformanceResponse,
    TeamPlayersResponse,
    TeamRankingsResponse,
    TeamStatisticsResponse,
    TeamStatisticsSeasonsResponse,
    TeamTransfersResponse,
)
from aiosofascore.api.soccer.services.team.repo import (
    TeamInfoRepository,
    TeamLastEventsRepository,
    TeamPerformanceRepository,
    TeamPlayersRepository,
    TeamRankingsRepository,
    TeamStatisticsRepository,
    TeamStatisticsSeasonsRepository,
    TeamTransfersRepository,
)


class TeamPerformanceService:
    """Service for getting team performance."""

    def __init__(self, repository: TeamPerformanceRepository):
        self.repository = repository

    async def get_team_performance(self, team_id: int) -> TeamPerformanceResponse:
        return await self.repository.get_performance(team_id)


class TeamInfoService:
    """Service for getting team info."""

    def __init__(self, repository: TeamInfoRepository):
        self.repository = repository

    async def get_team_info(self, team_id: int) -> TeamInfo:
        return await self.repository.get_team_info(team_id)


class TeamLastEventsService:
    """Service for getting team last events."""

    def __init__(self, repository: TeamLastEventsRepository):
        self.repository = repository

    async def get_last_events(
        self, team_id: int, page: int = 0
    ) -> TeamLastEventsResponse:
        return await self.repository.get_last_events(team_id, page=page)

    async def iter_last_events(
        self, team_id: int
    ) -> AsyncGenerator[PerformanceEvent, None]:
        """Iterate over all last events, automatically paginating."""
        page = 0
        while True:
            result = await self.repository.get_last_events(team_id, page=page)
            if result.events:
                for event in result.events:
                    yield event
            if not result.hasNextPage:
                break
            page += 1


class TeamPlayersService:
    """Service for getting team players."""

    def __init__(self, repository: TeamPlayersRepository):
        self.repository = repository

    async def get_team_players(self, team_id: int) -> TeamPlayersResponse:
        return await self.repository.get_team_players(team_id)


class TeamRankingsService:
    """Service for getting team rankings."""

    def __init__(self, repository: TeamRankingsRepository):
        self.repository = repository

    async def get_team_rankings(self, team_id: int) -> TeamRankingsResponse:
        return await self.repository.get_team_rankings(team_id)


class TeamTransfersService:
    """Service for getting team transfers."""

    def __init__(self, repository: TeamTransfersRepository):
        self.repository = repository

    async def get_team_transfers(self, team_id: int) -> TeamTransfersResponse:
        return await self.repository.get_team_transfers(team_id)


class TeamStatisticsSeasonsService:
    """Service for listing available statistics seasons for a team."""

    def __init__(self, repository: TeamStatisticsSeasonsRepository):
        self.repository = repository

    async def get_statistics_seasons(
        self, team_id: int
    ) -> TeamStatisticsSeasonsResponse:
        return await self.repository.get_statistics_seasons(team_id)


class TeamStatisticsService:
    """Service for getting team statistics in a tournament season."""

    def __init__(self, repository: TeamStatisticsRepository):
        self.repository = repository

    async def get_statistics(
        self,
        team_id: int,
        tournament_id: int,
        season_id: int,
        filter: str = "overall",
    ) -> TeamStatisticsResponse:
        return await self.repository.get_statistics(
            team_id, tournament_id, season_id, filter=filter
        )
