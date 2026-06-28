from pydantic import BaseModel, Field
from typing import Any, Optional, List, Dict
from .common import (
    TeamShortInfo,
    TournamentCategory,
    UniqueTournament,
    Tournament,
    Season,
    RoundInfo,
    Status,
    Score,
    TimeInfo,
    Country,
    Manager,
    VenueCoordinates,
    City,
    Venue,
    TeamColors,
    TeamInfo,
    PregameForm,
    Player,
    PlayerItem,
    CricketSupportStaff,
    TransferTeamShort,
    TransferPlayerShort,
    TransferFeeRaw,
    Referee,
)


class ManOfMatch(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    slug: Optional[str] = None
    shortName: Optional[str] = None
    position: Optional[str] = None
    userCount: Optional[int] = None
    dateOfBirthTimestamp: Optional[int] = None
    country: Optional[dict] = None
    team: Optional[dict] = None
    jerseyNumber: Optional[str] = None
    height: Optional[int] = None
    preferredFoot: Optional[str] = None
    retired: Optional[bool] = None
    deceased: Optional[bool] = None


class Periods(BaseModel):
    # Dynamic fields for periods
    pass


class TeamSeasonHistoricalForm(BaseModel):
    form: Optional[str] = None
    lastFiveEvents: Optional[List[dict]] = None


class PerformanceEvent(BaseModel):
    id: Optional[int] = None
    slug: Optional[str] = None
    tournament: Optional[Tournament] = None
    season: Optional[Season] = None
    roundInfo: Optional[RoundInfo] = None
    status: Optional[Status] = None
    winnerCode: Optional[int] = None
    aggregatedWinnerCode: Optional[int] = None
    attendance: Optional[int] = None
    venue: Optional[dict] = None
    referee: Optional[Referee] = None
    homeTeam: Optional[TeamShortInfo] = None
    awayTeam: Optional[TeamShortInfo] = None
    homeScore: Optional[Score] = None
    awayScore: Optional[Score] = None
    hasGlobalHighlights: Optional[bool] = None
    hasEventPlayerStatistics: Optional[bool] = None
    hasEventPlayerHeatMap: Optional[bool] = None
    hasXg: Optional[bool] = None
    customId: Optional[str] = None
    detailId: Optional[int] = None
    startTimestamp: Optional[int] = None
    endTimestamp: Optional[int] = None
    time: Optional[TimeInfo] = None
    changes: Optional[dict] = None
    coverage: Optional[int] = None
    previousLegEventId: Optional[int] = None
    parentEventId: Optional[int] = None
    lastPeriod: Optional[str] = None
    finalResultOnly: Optional[bool] = None
    crowdsourcingEnabled: Optional[bool] = None
    isEditor: Optional[bool] = None
    isAwarded: Optional[bool] = None
    deletedAtTimestamp: Optional[int] = None
    manOfMatch: Optional[ManOfMatch] = None
    currentPeriodStartTimestamp: Optional[int] = None
    periods: Optional[dict] = None
    defaultPeriodCount: Optional[int] = None
    defaultPeriodLength: Optional[int] = None
    hasBet365LiveStream: Optional[bool] = None
    bet365ExcludedCountryCodes: Optional[List[str]] = None
    cupMatchesInRound: Optional[int] = None
    fanRatingEvent: Optional[bool] = None
    statusReason: Optional[str] = None
    eventEditorName: Optional[str] = None
    eventEditor: Optional[dict] = None
    eventType: Optional[str] = None
    seasonStatisticsType: Optional[str] = None
    homeRedCards: Optional[int] = None
    awayRedCards: Optional[int] = None
    currentBattingTeamId: Optional[int] = None
    currentBatsmanId: Optional[int] = None
    currentBowlerId: Optional[int] = None
    refereeName: Optional[str] = None
    umpire1Name: Optional[str] = None
    umpire2Name: Optional[str] = None
    tvUmpireName: Optional[str] = None
    note: Optional[str] = None
    tossWin: Optional[str] = None
    tossDecision: Optional[str] = None
    cricketBallProperties: Optional[List[dict]] = None
    firstToServe: Optional[str] = None
    groundType: Optional[str] = None
    homeTeamSeed: Optional[int] = None
    awayTeamSeed: Optional[int] = None
    bestOf: Optional[int] = None
    gameAdvantageTeamId: Optional[int] = None
    showTotoPromo: Optional[bool] = None
    fightType: Optional[str] = None
    fightDiscipline: Optional[str] = None
    winType: Optional[str] = None
    weightClass: Optional[str] = None
    gender: Optional[str] = None
    finalRound: Optional[str] = None
    fightState: Optional[str] = None
    homeTeamRanking: Optional[int] = None
    awayTeamRanking: Optional[int] = None
    crowdsourcingDataDisplayEnabled: Optional[bool] = None
    yardDistance: Optional[int] = None
    homeTeamSeasonHistoricalForm: Optional[TeamSeasonHistoricalForm] = None
    awayTeamSeasonHistoricalForm: Optional[TeamSeasonHistoricalForm] = None


class TeamPerformanceResponse(BaseModel):
    events: List[PerformanceEvent]
    points: Dict[str, float]


class TeamPlayersResponse(BaseModel):
    players: Optional[List[PlayerItem]] = None
    foreignPlayers: Optional[List[PlayerItem]] = None
    nationalPlayers: Optional[List[PlayerItem]] = None
    supportStaff: Optional[List[CricketSupportStaff]] = None


class TeamRankingCountry(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    alpha2: Optional[str] = None
    alpha3: Optional[str] = None


class TeamRankingTeam(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    userCount: Optional[int] = None
    type: Optional[int] = None
    teamColors: Optional[dict] = None
    nameCode: Optional[str] = None


class TeamRankingUniqueTournament(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None


class TeamRankingItem(BaseModel):
    id: Optional[int] = None
    type: Optional[int] = None
    country: Optional[TeamRankingCountry] = None
    rankingClass: Optional[str] = None
    ranking: Optional[int] = None
    points: Optional[float] = None
    previousRanking: Optional[int] = None
    previousPoints: Optional[float] = None
    rowName: Optional[str] = None
    bestRanking: Optional[int] = None
    bestRankingDateTimestamp: Optional[int] = None
    currentRound: Optional[str] = None
    currentTournamentName: Optional[str] = None
    currentTournamentId: Optional[int] = None
    previousTournamentRound: Optional[str] = None
    previousTournamentName: Optional[str] = None
    previousTournamentId: Optional[int] = None
    nextWinPoints: Optional[float] = None
    maxPoints: Optional[float] = None
    team: Optional[TeamRankingTeam] = None
    tournamentsPlayed: Optional[int] = None
    uniqueTournament: Optional[TeamRankingUniqueTournament] = None
    totalTeams: Optional[int] = None
    playingTeams: Optional[int] = None


class TeamRankingsResponse(BaseModel):
    rankings: Optional[List[TeamRankingItem]] = None


# Transfers
class TransferItem(BaseModel):
    id: Optional[int] = None
    transferDateTimestamp: Optional[int] = None
    player: Optional[TransferPlayerShort] = None
    transferFrom: Optional[TransferTeamShort] = None
    transferTo: Optional[TransferTeamShort] = None
    fromTeamName: Optional[str] = None
    toTeamName: Optional[str] = None
    type: Optional[int] = None
    transferFeeRaw: Optional[TransferFeeRaw] = None
    transferFeeDescription: Optional[str] = None
    round: Optional[str] = None
    pick: Optional[str] = None


class TeamTransfersResponse(BaseModel):
    transfersIn: Optional[List[TransferItem]] = None
    transfersOut: Optional[List[TransferItem]] = None


class TeamLastEventsResponse(BaseModel):
    events: Optional[List[PerformanceEvent]] = None
    hasNextPage: Optional[bool] = None


class StatisticsSeason(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    year: Optional[str] = None


class StatisticsUniqueTournament(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None


class UniqueTournamentSeasonItem(BaseModel):
    uniqueTournament: Optional[StatisticsUniqueTournament] = None
    seasons: Optional[List[StatisticsSeason]] = None


class TeamStatisticsSeasonsResponse(BaseModel):
    uniqueTournamentSeasons: Optional[List[UniqueTournamentSeasonItem]] = None


class TeamStatisticsResponse(BaseModel):
    statistics: Optional[dict] = None
