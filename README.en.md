[🇷🇺 Russian](README.md) | [🇬🇧 English](README.en.md)

![PyPI Version](https://img.shields.io/pypi/v/aiosofascore)
[![PyPI Downloads](https://static.pepy.tech/badge/aiosofascore)](https://pepy.tech/projects/aiosofascore)
![LICENSE](https://img.shields.io/badge/License-MIT-blue.svg)

# Aiosofascore

**Aiosofascore** is an asynchronous Python client for the SofaScore API (football), providing access to teams, matches, tournaments, players, and search.

## Features

- **Team** — info, players, events, rankings, transfers, statistics
- **Event** — match details, lineups, statistics, incidents, H2H
- **Live** — live matches
- **Tournament** — categories, tournaments, seasons, standings
- **Player** — profile, statistics, transfers
- **Search** — teams, players, events, managers

## Installation

```bash
pip install aiosofascore
```

## Quick Start

```python
import asyncio
from aiosofascore.client import SofaScoreClient

async def main():
    async with SofaScoreClient() as client:
        info = await client.team.info.get_team_info(2819)
        live = await client.live.get_live_events()
        event = await client.event.get_event(11352523)
        standings = await client.tournament.get_standings(17, 52186)
        player = await client.player.get_player(12345)
        async for result in client.search.search_teams("Arsenal"):
            print(result.entity.name)

asyncio.run(main())
```

## API Overview

| Service | Methods |
|---------|---------|
| `client.team` | info, players, last_events, performance, rankings, transfers, statistics |
| `client.event` | get_event, get_lineups, get_statistics, get_incidents, get_h2h, get_pregame_form, get_managers |
| `client.live` | get_live_events |
| `client.tournament` | get_categories, get_unique_tournaments, get_seasons, get_standings |
| `client.player` | get_player, get_statistics_seasons, get_statistics, get_transfers |
| `client.search` | search_teams, search_players, search_events, search_managers, search_all |

See [CHANGELOG.md](CHANGELOG.md) for version history.

## HTTP Session Configuration

If you encounter 403 (anti-bot challenge) errors, pass browser cookies:

```python
async with SofaScoreClient(cookies={"your_cookie": "value"}) as client:
    ...
```

Or set `SOFASCORE_COOKIES` (JSON). Optionally use `SOFASCORE_PROXY` for a proxy.

## Tests

```bash
pytest tests/ -m "not integration" -v
SOFASCORE_LIVE=1 pytest tests/ -m integration
```

## License

MIT — see [LICENSE](LICENSE).

## Contact

Questions and suggestions: GitHub issue or vasilewskij.fil@gmail.com
