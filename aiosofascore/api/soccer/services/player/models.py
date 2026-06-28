from typing import List, Optional

from pydantic import BaseModel


class PlayerCountry(BaseModel):
    name: Optional[str] = None
    alpha2: Optional[str] = None
    slug: Optional[str] = None


class PlayerTeamShort(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    teamColors: Optional[dict] = None


class PlayerDetail(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    shortName: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    position: Optional[str] = None
    jerseyNumber: Optional[str] = None
    height: Optional[int] = None
    preferredFoot: Optional[str] = None
    dateOfBirthTimestamp: Optional[int] = None
    country: Optional[PlayerCountry] = None
    team: Optional[PlayerTeamShort] = None
    userCount: Optional[int] = None


class PlayerStatisticsSeason(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    year: Optional[str] = None


class PlayerStatisticsUniqueTournament(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None


class PlayerStatisticsSeasonItem(BaseModel):
    uniqueTournament: Optional[PlayerStatisticsUniqueTournament] = None
    seasons: Optional[List[PlayerStatisticsSeason]] = None


class PlayerStatisticsSeasonsResponse(BaseModel):
    uniqueTournamentSeasons: Optional[List[PlayerStatisticsSeasonItem]] = None


class PlayerStatisticsResponse(BaseModel):
    statistics: Optional[dict] = None


class PlayerTransfer(BaseModel):
    id: Optional[int] = None
    transferDateTimestamp: Optional[int] = None
    type: Optional[int] = None
    fromTeamName: Optional[str] = None
    toTeamName: Optional[str] = None
    transferFeeDescription: Optional[str] = None
    player: Optional[dict] = None
    transferFrom: Optional[dict] = None
    transferTo: Optional[dict] = None


class PlayerTransfersResponse(BaseModel):
    transferHistory: Optional[List[PlayerTransfer]] = None
