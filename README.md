[🇷🇺 Русский](README.md) | [🇬🇧 English](README.en.md)

![PyPI Version](https://img.shields.io/pypi/v/aiosofascore)
[![PyPI Downloads](https://static.pepy.tech/badge/aiosofascore)](https://pepy.tech/projects/aiosofascore)
![LICENSE](https://img.shields.io/badge/License-MIT-blue.svg)

# Aiosofascore

**Aiosofascore** — асинхронный Python-клиент для SofaScore API (футбол), предоставляющий удобный доступ к данным о командах, матчах, турнирах, игроках и поиску.

## Возможности

- **Team** — информация, игроки, матчи, рейтинги, трансферы, статистика
- **Event** — детали матча, составы, статистика, инциденты, H2H
- **Live** — текущие live-матчи
- **Tournament** — категории, турниры, сезоны, таблицы
- **Player** — профиль, статистика, трансферы
- **Search** — поиск команд, игроков, матчей, менеджеров

## Установка

```bash
pip install aiosofascore
```

## Быстрый старт

```python
import asyncio
from aiosofascore.client import SofaScoreClient

async def main():
    async with SofaScoreClient() as client:
        # Команда
        info = await client.team.info.get_team_info(2819)
        print(info.name)

        # Live-матчи
        live = await client.live.get_live_events()
        for e in live.events or []:
            print(e.homeTeam.name, "vs", e.awayTeam.name)

        # Матч
        event = await client.event.get_event(11352523)
        stats = await client.event.get_statistics(11352523)

        # Турнирная таблица
        standings = await client.tournament.get_standings(17, 52186)

        # Игрок
        player = await client.player.get_player(12345)

        # Поиск
        async for result in client.search.search_teams("Arsenal"):
            print(result.entity.name)

asyncio.run(main())
```

## API

| Сервис | Метод | Описание |
|--------|-------|----------|
| `client.team.info` | `get_team_info(id)` | Информация о команде |
| `client.team.players` | `get_team_players(id)` | Состав |
| `client.team.last_events` | `get_last_events(id, page)` / `iter_last_events(id)` | Последние матчи |
| `client.team.statistics` | `get_statistics(id, tournament_id, season_id)` | Статистика сезона |
| `client.event` | `get_event`, `get_lineups`, `get_statistics`, `get_incidents`, `get_h2h` | Матч |
| `client.live` | `get_live_events()` | Live-матчи |
| `client.tournament` | `get_categories`, `get_standings`, `get_seasons` | Турниры |
| `client.player` | `get_player`, `get_statistics`, `get_transfers` | Игрок |
| `client.search` | `search_teams`, `search_players`, `search_events`, `search_all` | Поиск |

Полный список изменений — в [CHANGELOG.md](CHANGELOG.md).

## Настройка HTTP-сессии

При ошибках 403 (anti-bot challenge) передайте cookies из браузера:

```python
async with SofaScoreClient(cookies={"your_cookie": "value"}) as client:
    ...
```

Или через переменную окружения `SOFASCORE_COOKIES` (JSON). Опционально: `SOFASCORE_PROXY` для прокси.

## Тесты

```bash
pytest tests/ -m "not integration" -v          # unit-тесты (без сети)
SOFASCORE_LIVE=1 pytest tests/ -m integration  # live API
```

## License

MIT — см. [LICENSE](LICENSE).

## Contact

Вопросы и предложения: issue на GitHub или vasilewskij.fil@gmail.com
