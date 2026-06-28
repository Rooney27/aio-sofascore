# Changelog

## 0.2.1

### Changed
- **Breaking fix:** default API base URL changed from `https://api.sofascore.com` to `https://www.sofascore.com`
- Search endpoint fixed: `/api/v1/search/all` (was `/v1/search/all`)

## 0.2.0

### Added
- **Event service**: `get_event`, `get_lineups`, `get_statistics`, `get_incidents`, `get_h2h`, `get_pregame_form`, `get_managers`
- **Live service**: `get_live_events(sport="football")`
- **Tournament service**: `get_categories`, `get_unique_tournaments`, `get_seasons`, `get_standings`, `get_standings_by_year`
- **Player service**: `get_player`, `get_statistics_seasons`, `get_statistics`, `get_transfers`
- Shared `BaseRepository` with `_get_wrapped` helper
- 31 unit tests with JSON fixtures
- Example `examples/all_services.py`

### Changed
- `SofaScoreClient` exposes `event`, `live`, `tournament`, `player` services
- CI publish workflow triggers on version tags (`v*`) instead of every push to main

## 0.1.3.0

- Search UX: `client.search` is `SearchService` directly with sugar methods
- Team statistics: `statistics_seasons`, `statistics`
- `iter_last_events` async generator

## 0.1.2.0

- HTTP session reuse, retry, configurable cookies/proxy
- `async with SofaScoreClient()` context manager
- Mock-based unit tests and CI test workflow

## 0.1.1.0

- Team and search services refactor
