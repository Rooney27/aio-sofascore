from aiosofascore.api.soccer.services.player.models import (
    PlayerDetail,
    PlayerStatisticsResponse,
    PlayerStatisticsSeasonsResponse,
    PlayerTransfersResponse,
)
from aiosofascore.api.soccer.services.player.repo import PlayerRepository


class PlayerService:
    def __init__(self, repository: PlayerRepository):
        self.repository = repository

    async def get_player(self, player_id: int) -> PlayerDetail:
        return await self.repository.get_player(player_id)

    async def get_statistics_seasons(
        self, player_id: int
    ) -> PlayerStatisticsSeasonsResponse:
        return await self.repository.get_statistics_seasons(player_id)

    async def get_statistics(
        self,
        player_id: int,
        tournament_id: int,
        season_id: int,
        filter: str = "overall",
    ) -> PlayerStatisticsResponse:
        return await self.repository.get_statistics(
            player_id, tournament_id, season_id, filter=filter
        )

    async def get_transfers(self, player_id: int) -> PlayerTransfersResponse:
        return await self.repository.get_transfers(player_id)
