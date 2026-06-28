from pydantic import BaseModel
from typing import Optional, List, Dict


class TeamShortInfo(BaseModel):
    id: int
    name: str
    slug: str
    shortName: Optional[str] = None
    gender: Optional[str] = None
    sport: Optional[dict] = None
    userCount: Optional[int] = None
    nameCode: Optional[str] = None
    disabled: Optional[bool] = None
    national: Optional[bool] = None
    type: Optional[int] = None
    subTeams: Optional[list] = None
    teamColors: Optional[dict] = None
    fieldTranslations: Optional[dict] = None
    country: Optional[dict] = None


class TournamentCategory(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    sport: Optional[dict] = None
    flag: Optional[str] = None
    alpha2: Optional[str] = None
    country: Optional[dict] = None


class UniqueTournament(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    primaryColorHex: Optional[str] = None
    secondaryColorHex: Optional[str] = None
    category: Optional[TournamentCategory] = None
    userCount: Optional[int] = None
    hasPerformanceGraphFeature: Optional[bool] = None
    hasEventPlayerStatistics: Optional[bool] = None
    displayInverseHomeAwayTeams: Optional[bool] = None
    fieldTranslations: Optional[dict] = None
    country: Optional[dict] = None


class Tournament(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    category: Optional[TournamentCategory] = None
    uniqueTournament: Optional[UniqueTournament] = None
    priority: Optional[int] = None
    isGroup: Optional[bool] = None
    isLive: Optional[bool] = None
    fieldTranslations: Optional[dict] = None
    groupName: Optional[str] = None


class Season(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    year: Optional[str] = None
    editor: Optional[bool] = None


class RoundInfo(BaseModel):
    round: Optional[int] = None
    name: Optional[str] = None


class Status(BaseModel):
    code: Optional[int] = None
    description: Optional[str] = None
    type: Optional[str] = None


class Score(BaseModel):
    current: Optional[int] = None
    display: Optional[int] = None
    period1: Optional[int] = None
    period2: Optional[int] = None
    normaltime: Optional[int] = None


class TimeInfo(BaseModel):
    injuryTime1: Optional[int] = None
    injuryTime2: Optional[int] = None
    currentPeriodStartTimestamp: Optional[int] = None
    periodLength: Optional[int] = None
    overtimeLength: Optional[int] = None
    totalPeriodCount: Optional[int] = None


class Country(BaseModel):
    alpha2: Optional[str]
    alpha3: Optional[str]
    name: str
    slug: str


class Manager(BaseModel):
    name: str
    slug: str
    shortName: Optional[str]
    id: Optional[int]
    country: Optional[Country]


class VenueCoordinates(BaseModel):
    latitude: float
    longitude: float


class City(BaseModel):
    name: str


class Venue(BaseModel):
    city: Optional[City]
    venueCoordinates: Optional[VenueCoordinates]
    hidden: Optional[bool]
    slug: Optional[str]
    name: str
    capacity: Optional[int]
    id: Optional[int]
    country: Optional[Country]
    fieldTranslations: Optional[dict]
    stadium: Optional[dict]


class TeamColors(BaseModel):
    primary: str
    secondary: str
    text: str


class TeamInfo(BaseModel):
    name: str
    slug: str
    shortName: Optional[str]
    gender: Optional[str]
    sport: dict
    category: dict
    tournament: dict
    primaryUniqueTournament: dict
    userCount: Optional[int]
    manager: Optional[Manager]
    venue: Optional[Venue]
    nameCode: Optional[str]
    disabled: Optional[bool]
    national: Optional[bool]
    type: Optional[int]
    id: int
    country: Optional[Country]
    fullName: Optional[str]
    teamColors: Optional[TeamColors]
    foundationDateTimestamp: Optional[int]
    fieldTranslations: Optional[dict]
    timeActive: Optional[list]


class PregameForm(BaseModel):
    avgRating: Optional[str]
    position: Optional[int]
    value: Optional[str]
    form: Optional[List[str]]


class Player(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    slug: Optional[str] = None
    shortName: Optional[str] = None
    position: Optional[str] = None
    userCount: Optional[int] = None
    dateOfBirthTimestamp: Optional[int] = None
    dateOfDeathTimestamp: Optional[int] = None
    country: Optional[dict] = None
    team: Optional[dict] = None
    jerseyNumber: Optional[str] = None
    height: Optional[int] = None
    preferredFoot: Optional[str] = None
    retired: Optional[bool] = None
    deceased: Optional[bool] = None
    cricketPlayerInfo: Optional[dict] = None
    managerId: Optional[int] = None
    marketValueRaw: Optional[dict] = None
    proposedMarketValueRaw: Optional[dict] = None
    contractUntilTimestamp: Optional[int] = None
    injury: Optional[dict] = None
    fieldTranslations: Optional[dict] = None


class PlayerItem(BaseModel):
    player: Player


class CricketSupportStaff(BaseModel):
    pass


class TransferTeamShort(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None


class TransferPlayerShort(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None


class TransferFeeRaw(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None


class Referee(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
