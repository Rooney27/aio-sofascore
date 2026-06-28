from typing import List, Optional

from pydantic import BaseModel

from aiosofascore.api.soccer.services.team.common import (
    RoundInfo,
    Score,
    Status,
    TeamShortInfo,
    Tournament,
)


class LiveEvent(BaseModel):
    id: Optional[int] = None
    slug: Optional[str] = None
    tournament: Optional[Tournament] = None
    status: Optional[Status] = None
    homeTeam: Optional[TeamShortInfo] = None
    awayTeam: Optional[TeamShortInfo] = None
    homeScore: Optional[Score] = None
    awayScore: Optional[Score] = None
    startTimestamp: Optional[int] = None
    roundInfo: Optional[RoundInfo] = None
    finalResultOnly: Optional[bool] = None


class LiveEventsResponse(BaseModel):
    events: Optional[List[LiveEvent]] = None
