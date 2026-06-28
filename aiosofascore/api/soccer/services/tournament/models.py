from typing import List, Optional

from pydantic import BaseModel

from aiosofascore.api.soccer.services.team.common import UniqueTournament


class SportInfo(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None


class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    flag: Optional[str] = None
    sport: Optional[SportInfo] = None
    priority: Optional[int] = None


class CategoriesResponse(BaseModel):
    categories: Optional[List[Category]] = None


class UniqueTournamentsResponse(BaseModel):
    groups: Optional[List[dict]] = None

    @property
    def unique_tournaments(self) -> List[UniqueTournament]:
        if not self.groups:
            return []
        tournaments = []
        for group in self.groups:
            for item in group.get("uniqueTournaments", []):
                tournaments.append(UniqueTournament(**item))
        return tournaments


class Season(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    year: Optional[str] = None
    editor: Optional[bool] = None


class SeasonsResponse(BaseModel):
    seasons: Optional[List[Season]] = None

    def get_season_by_year(self, year: str) -> Season | None:
        if not self.seasons:
            return None
        return next((s for s in self.seasons if s.year == year), None)

    def get_current_season(self) -> Season | None:
        if not self.seasons:
            return None
        return self.seasons[0]


class StandingsTeam(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    shortName: Optional[str] = None
    nameCode: Optional[str] = None


class StandingsRow(BaseModel):
    id: Optional[int] = None
    position: Optional[int] = None
    points: Optional[int] = None
    matches: Optional[int] = None
    wins: Optional[int] = None
    draws: Optional[int] = None
    losses: Optional[int] = None
    scoresFor: Optional[int] = None
    scoresAgainst: Optional[int] = None
    team: Optional[StandingsTeam] = None


class StandingsResponse(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    rows: Optional[List[StandingsRow]] = None
    tournament: Optional[dict] = None


class StandingsListResponse(BaseModel):
    standings: Optional[List[StandingsResponse]] = None

    @property
    def first(self) -> StandingsResponse | None:
        if not self.standings:
            return None
        return self.standings[0]
