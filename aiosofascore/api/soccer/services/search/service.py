from typing import AsyncGenerator, Literal

from aiosofascore.api.soccer.services.search.models import SearchEntityResult
from aiosofascore.api.soccer.services.search.repo import SearchRepository

EntityType = Literal["team", "player", "event", "manager"]


class SearchService:
    def __init__(self, repository: SearchRepository):
        self.repository = repository

    async def search(
        self,
        query: str,
        type: EntityType | None = None,
    ) -> AsyncGenerator[SearchEntityResult, None]:
        """Search entities by query, optionally filtered by type."""
        async for item in self.repository.search(query, type=type):
            yield item

    async def search_entities(
        self,
        query: str,
        type: EntityType | None = None,
    ) -> AsyncGenerator[SearchEntityResult, None]:
        """Alias for :meth:`search` (backward compatibility)."""
        async for item in self.search(query, type=type):
            yield item

    async def search_all(self, query: str) -> AsyncGenerator[SearchEntityResult, None]:
        async for item in self.search(query):
            yield item

    async def search_teams(
        self, query: str
    ) -> AsyncGenerator[SearchEntityResult, None]:
        async for item in self.search(query, type="team"):
            yield item

    async def search_players(
        self, query: str
    ) -> AsyncGenerator[SearchEntityResult, None]:
        async for item in self.search(query, type="player"):
            yield item

    async def search_events(
        self, query: str
    ) -> AsyncGenerator[SearchEntityResult, None]:
        async for item in self.search(query, type="event"):
            yield item

    async def search_managers(
        self, query: str
    ) -> AsyncGenerator[SearchEntityResult, None]:
        async for item in self.search(query, type="manager"):
            yield item
