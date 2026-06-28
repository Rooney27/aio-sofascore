from typing import List, Optional

from pydantic import BaseModel

from aiosofascore.api.soccer.services.team.common import (
    Manager,
    RoundInfo,
    Score,
    Season,
    Status,
    TeamShortInfo,
    Tournament,
)


class EventDetail(BaseModel):
    id: Optional[int] = None
    slug: Optional[str] = None
    customId: Optional[str] = None
    tournament: Optional[Tournament] = None
    season: Optional[Season] = None
    roundInfo: Optional[RoundInfo] = None
    status: Optional[Status] = None
    winnerCode: Optional[int] = None
    homeTeam: Optional[TeamShortInfo] = None
    awayTeam: Optional[TeamShortInfo] = None
    homeScore: Optional[Score] = None
    awayScore: Optional[Score] = None
    startTimestamp: Optional[int] = None
    venue: Optional[dict] = None
    referee: Optional[dict] = None


class EventLineupsResponse(BaseModel):
    confirmed: Optional[bool] = None
    home: Optional[dict] = None
    away: Optional[dict] = None


class EventStatisticsItem(BaseModel):
    name: Optional[str] = None
    home: Optional[str | int | float] = None
    away: Optional[str | int | float] = None
    homeValue: Optional[float] = None
    awayValue: Optional[float] = None
    compareCode: Optional[int] = None


class EventStatisticsGroup(BaseModel):
    groupName: Optional[str] = None
    statisticsItems: Optional[List[EventStatisticsItem]] = None


class EventStatisticsPeriod(BaseModel):
    period: Optional[str] = None
    groups: Optional[List[EventStatisticsGroup]] = None


class EventStatisticsResponse(BaseModel):
    statistics: Optional[List[EventStatisticsPeriod]] = None


class EventIncident(BaseModel):
    id: Optional[int] = None
    time: Optional[int] = None
    addedTime: Optional[int] = None
    incidentType: Optional[str] = None
    player: Optional[dict] = None
    playerIn: Optional[dict] = None
    playerOut: Optional[dict] = None
    isHome: Optional[bool] = None
    text: Optional[str] = None
    homeScore: Optional[int] = None
    awayScore: Optional[int] = None


class EventIncidentsResponse(BaseModel):
    incidents: Optional[List[EventIncident]] = None
    home: Optional[dict] = None
    away: Optional[dict] = None


class TeamForm(BaseModel):
    avgRating: Optional[str] = None
    form: Optional[List[str]] = None
    position: Optional[int] = None
    value: Optional[str] = None


class PregameFormResponse(BaseModel):
    homeTeam: Optional[TeamForm] = None
    awayTeam: Optional[TeamForm] = None


class Duel(BaseModel):
    homeWins: Optional[int] = None
    awayWins: Optional[int] = None
    draws: Optional[int] = None


class H2HResponse(BaseModel):
    teamDuel: Optional[Duel] = None
    managerDuel: Optional[Duel] = None


class EventManagersResponse(BaseModel):
    homeManager: Optional[Manager] = None
    awayManager: Optional[Manager] = None
