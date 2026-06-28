from datetime import datetime
from typing import Union, Optional, List

from pydantic import BaseModel, root_validator, model_validator


class Country(BaseModel):
    name: str


class TeamColors(BaseModel):
    primary: str
    secondary: str
    text: str


class Sport(BaseModel):
    id: int
    name: str


class Team(BaseModel):
    id: int
    name: str
    nameCode: Optional[str] = None
    national: Optional[bool] = False
    sport: Optional[Sport] = None
    teamColors: TeamColors
    country: Optional[Country] = None
    type: Optional[str | int] = None
    gender: Optional[str] = None


class Player(BaseModel):
    id: int
    name: str
    shortName: str
    position: Optional[str] = None
    jerseyNumber: Optional[str] = None
    team: Team
    country: Optional[Country] = None
    sofascoreId: Optional[str] = None


class Manager(BaseModel):
    id: int
    name: str
    sport: Optional[Sport] = None
    team: Optional[Team] = None
    country: Optional[Country] = None


class TournamentCategory(BaseModel):
    id: int
    name: str
    flag: str
    sport: Optional[Sport] = None
    country: Optional[Country] = None


class Tournament(BaseModel):
    id: int
    name: str
    category: TournamentCategory


class EventStatus(BaseModel):
    type: str
    description: str


class EventTeamScore(BaseModel):
    display: Optional[int] = None


class Event(BaseModel):
    id: int
    name: str
    tournament: Tournament
    status: EventStatus
    homeTeam: Team
    awayTeam: Team
    homeScore: Optional[EventTeamScore]
    awayScore: Optional[EventTeamScore]
    startTimestamp: datetime


class SearchEntityResult(BaseModel):
    entity: Union[Team, Player, Event, Manager]
    type: str
    model_config = {
        "repr": True,
    }

    @model_validator(mode="before")
    @classmethod
    def validate_entity(cls, values: dict) -> dict:
        entity_data = values.get("entity")
        entity_type = values.get("type")

        if not entity_data or not entity_type:
            return values
        if entity_type == "team":
            values["entity"] = Team.model_validate(entity_data)
        elif entity_type == "player":
            values["entity"] = Player.model_validate(entity_data)
        elif entity_type == "event":
            values["entity"] = Event.model_validate(entity_data)
        elif entity_type == "manager":
            values["entity"] = Manager.model_validate(entity_data)

        return values
