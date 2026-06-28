from aiosofascore.api.soccer.services.base import BaseRepository
from aiosofascore.api.soccer.services.player.models import (
    PlayerDetail,
    PlayerStatisticsResponse,
    PlayerStatisticsSeasonsResponse,
    PlayerTransfersResponse,
)


class PlayerRepository(BaseRepository):
    async def get_player(self, player_id: int) -> PlayerDetail:
        url = f"/api/v1/player/{player_id}"
        return await self._get_wrapped(url, PlayerDetail, "player")

    async def get_statistics_seasons(
        self, player_id: int
    ) -> PlayerStatisticsSeasonsResponse:
        url = f"/api/v1/player/{player_id}/statistics/seasons"
        return await self._get(url, PlayerStatisticsSeasonsResponse)

    async def get_statistics(
        self,
        player_id: int,
        tournament_id: int,
        season_id: int,
        filter: str = "overall",
    ) -> PlayerStatisticsResponse:
        url = (
            f"/api/v1/player/{player_id}/unique-tournament/{tournament_id}"
            f"/season/{season_id}/statistics/{filter}"
        )
        return await self._get(url, PlayerStatisticsResponse)

    async def get_transfers(self, player_id: int) -> PlayerTransfersResponse:
        url = f"/api/v1/player/{player_id}/transfer-history"
        return await self._get(url, PlayerTransfersResponse)
