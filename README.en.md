[🇷🇺 Russian](README.md) | [🇬🇧 English](README.en.md)

![PyPI Version](https://img.shields.io/pypi/v/aiosofascore)
[![PyPI Downloads](https://static.pepy.tech/badge/aiosofascore)](https://pepy.tech/projects/aiosofascore)
![LICENSE](https://img.shields.io/badge/License-MIT-blue.svg)

# Aiosofascore

**Aiosofascore** is an asynchronous Python client for the SofaScore API (football), providing easy access to team, match, search, and statistics data.

## Features

- Get team info, last matches, and statistics
- Search for players, teams, events, managers
- Asynchronous HTTP client based on aiohttp
- Convenient SofaScoreClient facade for all services

## Installation

```bash
pip install aiosofascore
```

## Quick Start

### Team example (all main features)
```python
import asyncio
from aiosofascore.client import SofaScoreClient

TEAM_ID = 2819  # You can change to any team ID
PAGE = 0

async def main():
    async with SofaScoreClient() as client:
        # Players
        players = await client.team.players.get_team_players(TEAM_ID)
        print(f"\n=== Team players ===")
        if players.players:
            for i, player_item in enumerate(players.players, 1):
                player = player_item.player
                print(f"{i:2d}. {player.name} | {player.position or '-'} | #{player.jerseyNumber or '-'}")
        # Last events
        last_events = await client.team.last_events.get_last_events(TEAM_ID, PAGE)
        print(f"\n=== Last events ===")
        for event in last_events.events:
            tournament_name = event.tournament.name if event.tournament and event.tournament.name else "-"
            print(f"Event id: {event.id}, tournament: {tournament_name}, date: {event.startTimestamp}")
        # Performance
        perf = await client.team.performance.get_team_performance(TEAM_ID)
        print(f"\n=== Performance ===")
        if perf.events:
            for i, event in enumerate(perf.events[:5], 1):
                home = event.homeTeam.name if event.homeTeam else '-'
                away = event.awayTeam.name if event.awayTeam else '-'
                print(f"{i:2d}. {home} vs {away}")
                if event.homeScore and event.awayScore:
                    print(f"     Score: {event.homeScore.current or 0} - {event.awayScore.current or 0}")
        # Rankings
        rankings = await client.team.rankings.get_team_rankings(TEAM_ID)
        print(f"\n=== Rankings ===")
        if rankings.rankings:
            for r in rankings.rankings:
                print(f"{r.rowName or '-'}: {r.ranking} place, {r.points} pts, tournament: {r.currentTournamentName}")
        # Transfers
        transfers = await client.team.transfers.get_team_transfers(TEAM_ID)
        print(f"\n=== Transfers in ===")
        if transfers.transfersIn:
            for t in transfers.transfersIn:
                print(f"{t.player.name if t.player else '-'} from {t.fromTeamName or '-'} for {t.transferFeeDescription or '-'}")
        print(f"\n=== Transfers out ===")
        if transfers.transfersOut:
            for t in transfers.transfersOut:
                print(f"{t.player.name if t.player else '-'} to {t.toTeamName or '-'} for {t.transferFeeDescription or '-'}")

if __name__ == "__main__":
    asyncio.run(main())
```

### HTTP session configuration

If you encounter 403 (anti-bot challenge) errors, pass browser cookies:

```python
async with SofaScoreClient(cookies={"your_cookie": "value"}) as client:
    ...
```

Or set the `SOFASCORE_COOKIES` environment variable (JSON). Optionally use `SOFASCORE_PROXY` for a proxy.

## License
This project is licensed under the MIT License — see the LICENSE file for details.

## Contact
If you have any questions or suggestions, feel free to open an issue or contact me via vasilewskij.fil@gmail.com 