from aiosofascore.adapters.http_client import DEFAULT_BASE_URL, HttpSessionManager
from aiosofascore.api.soccer.services.team import (
    TeamInfoRepository,
    TeamInfoService,
    TeamLastEventsRepository,
    TeamLastEventsService,
    TeamPerformanceRepository,
    TeamPerformanceService,
    TeamPlayersRepository,
    TeamPlayersService,
    TeamRankingsRepository,
    TeamRankingsService,
    TeamStatisticsRepository,
    TeamStatisticsSeasonsRepository,
    TeamStatisticsSeasonsService,
    TeamStatisticsService,
    TeamTransfersRepository,
    TeamTransfersService,
)
from aiosofascore.api.soccer.services.search import SearchRepository, SearchService


class SofaScoreTeamServices:
    """Groups all team-related services."""

    def __init__(self, http: HttpSessionManager):
        self.performance = TeamPerformanceService(TeamPerformanceRepository(http))
        self.info = TeamInfoService(TeamInfoRepository(http))
        self.last_events = TeamLastEventsService(TeamLastEventsRepository(http))
        self.players = TeamPlayersService(TeamPlayersRepository(http))
        self.rankings = TeamRankingsService(TeamRankingsRepository(http))
        self.transfers = TeamTransfersService(TeamTransfersRepository(http))
        self.statistics_seasons = TeamStatisticsSeasonsService(
            TeamStatisticsSeasonsRepository(http)
        )
        self.statistics = TeamStatisticsService(TeamStatisticsRepository(http))


class SofaScoreClient:
    """
    Main facade for working with the SofaScore API.

    Example:
        async with SofaScoreClient() as client:
            players = await client.team.players.get_team_players(team_id)
            async for team in client.search.search_teams("Arsenal"):
                print(team.entity.name)
    """

    def __init__(
        self,
        base_url: str | None = None,
        cookies: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        proxy: str | None = None,
        max_retries: int = 3,
    ):
        self.http = HttpSessionManager(
            base_url=base_url or DEFAULT_BASE_URL,
            cookies=cookies,
            headers=headers,
            proxy=proxy,
            max_retries=max_retries,
        )
        self.team = SofaScoreTeamServices(self.http)
        self.search = SearchService(SearchRepository(self.http))

    async def __aenter__(self) -> "SofaScoreClient":
        await self.http.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.http.close()

    async def close(self) -> None:
        """Close the underlying HTTP session."""
        await self.http.close()
