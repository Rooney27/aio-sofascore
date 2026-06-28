#!/usr/bin/env python3
"""
Скрипт для ручной проверки работоспособности aiosofascore.

Запуск из корня репозитория:
    pip install -e .
    python examples/verify_library.py

Если получаете 403 (anti-bot challenge), задайте cookies из браузера:
    export SOFASCORE_COOKIES='{"cookie_name": "value"}'
    python examples/verify_library.py
"""

from __future__ import annotations

import asyncio
import sys
import traceback
from dataclasses import dataclass
from typing import Awaitable, Callable

from aiosofascore.client import SofaScoreClient
from aiosofascore.exception import ResponseParseContentError

# Известные ID для проверки (можно поменять)
TEAM_ID = 2819          # Manchester United
TOURNAMENT_ID = 17      # Premier League
SEARCH_QUERY = "Arsenal"


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""


def ok(msg: str) -> str:
    return msg


def section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print("=" * 60)


async def run_check(name: str, fn: Callable[[], Awaitable[str]]) -> CheckResult:
    try:
        detail = await fn()
        print(f"  ✓ {name}")
        if detail:
            print(f"    → {detail}")
        return CheckResult(name, True, detail)
    except ResponseParseContentError as exc:
        detail = await exc.async_str()
        print(f"  ✗ {name}")
        print(f"    → HTTP-ошибка API (часто 403 — нужны cookies)")
        for line in detail.strip().splitlines()[:4]:
            print(f"    {line}")
        return CheckResult(name, False, detail)
    except Exception as exc:
        print(f"  ✗ {name}")
        print(f"    → {exc}")
        return CheckResult(name, False, str(exc))


async def verify(client: SofaScoreClient) -> list[CheckResult]:
    results: list[CheckResult] = []

    section("1. Team — команда")
    results.append(
        await run_check(
            "team.info.get_team_info",
            lambda: _check_team_info(client),
        )
    )
    results.append(
        await run_check(
            "team.players.get_team_players",
            lambda: _check_team_players(client),
        )
    )
    results.append(
        await run_check(
            "team.last_events.get_last_events",
            lambda: _check_last_events(client),
        )
    )
    results.append(
        await run_check(
            "team.rankings.get_team_rankings",
            lambda: _check_rankings(client),
        )
    )

    section("2. Search — поиск")
    search_result = await run_check(
        "search.search_teams",
        lambda: _check_search_teams(client),
    )
    results.append(search_result)

    section("3. Live — live-матчи")
    results.append(
        await run_check(
            "live.get_live_events",
            lambda: _check_live(client),
        )
    )

    section("4. Tournament — турниры")
    results.append(
        await run_check(
            "tournament.get_categories",
            lambda: _check_categories(client),
        )
    )
    results.append(
        await run_check(
            "tournament.get_standings",
            lambda: _check_standings(client, TOURNAMENT_ID),
        )
    )

    section("5. Team statistics — статистика команды")
    results.append(
        await run_check(
            "team.statistics_seasons + statistics",
            lambda: _check_team_statistics(client),
        )
    )

    section("6. Event — матч (через поиск)")
    event_result = await run_check(
        "search → event.get_event + statistics",
        lambda: _check_event_via_search(client),
    )
    results.append(event_result)

    section("7. Player — игрок (через поиск)")
    results.append(
        await run_check(
            "search → player.get_player",
            lambda: _check_player_via_search(client),
        )
    )

    return results


async def _check_team_info(client: SofaScoreClient) -> str:
    info = await client.team.info.get_team_info(TEAM_ID)
    return ok(f"{info.name} (id={info.id}, slug={info.slug})")


async def _check_team_players(client: SofaScoreClient) -> str:
    data = await client.team.players.get_team_players(TEAM_ID)
    count = len(data.players or [])
    first = data.players[0].player.name if data.players else "—"
    return ok(f"{count} игроков, первый: {first}")


async def _check_last_events(client: SofaScoreClient) -> str:
    data = await client.team.last_events.get_last_events(TEAM_ID, page=0)
    count = len(data.events or [])
    has_next = data.hasNextPage
    return ok(f"{count} матчей на странице, hasNextPage={has_next}")


async def _check_rankings(client: SofaScoreClient) -> str:
    data = await client.team.rankings.get_team_rankings(TEAM_ID)
    count = len(data.rankings or [])
    return ok(f"{count} записей рейтинга")


async def _check_search_teams(client: SofaScoreClient) -> str:
    names = []
    async for item in client.search.search_teams(SEARCH_QUERY):
        names.append(item.entity.name)
        if len(names) >= 3:
            break
    return ok(f"найдено: {', '.join(names) or 'ничего'}")


async def _check_live(client: SofaScoreClient) -> str:
    data = await client.live.get_live_events()
    events = data.events or []
    if not events:
        return ok("live-матчей сейчас нет (это нормально)")
    e = events[0]
    home = e.homeTeam.name if e.homeTeam else "?"
    away = e.awayTeam.name if e.awayTeam else "?"
    status = e.status.type if e.status else "?"
    return ok(f"{len(events)} live, пример: {home} vs {away} [{status}]")


async def _check_categories(client: SofaScoreClient) -> str:
    data = await client.tournament.get_categories()
    cats = data.categories or []
    sample = cats[0].name if cats else "—"
    return ok(f"{len(cats)} категорий, пример: {sample}")


async def _check_standings(client: SofaScoreClient, tournament_id: int) -> str:
    seasons = await client.tournament.get_seasons(tournament_id)
    if not seasons.seasons:
        return ok("сезоны не найдены — пропуск standings")
    season_id = seasons.seasons[0].id

    data = await client.tournament.get_standings(tournament_id, season_id)
    rows = data.rows or []
    if not rows:
        return ok("таблица пуста")
    top = rows[0]
    return ok(
        f"лидер: {top.team.name} — {top.points} очков ({len(rows)} команд)"
    )


async def _check_team_statistics(client: SofaScoreClient) -> str:
    seasons = await client.team.statistics_seasons.get_statistics_seasons(TEAM_ID)
    if not seasons.uniqueTournamentSeasons:
        return ok("сезоны статистики не найдены")
    item = seasons.uniqueTournamentSeasons[0]
    tournament = item.uniqueTournament
    season = item.seasons[0] if item.seasons else None
    if not tournament or not season or not season.id:
        return ok("нет данных турнира/сезона")
    stats = await client.team.statistics.get_statistics(
        TEAM_ID, tournament.id, season.id
    )
    keys = list((stats.statistics or {}).keys())[:4]
    return ok(f"{tournament.name} / {season.name}: поля {keys}")


async def _check_event_via_search(client: SofaScoreClient) -> str:
    event_id = None
    async for item in client.search.search_events(f"{SEARCH_QUERY} vs"):
        if item.type == "event" and hasattr(item.entity, "id"):
            event_id = item.entity.id
            break
    if not event_id:
        return ok("матч через поиск не найден — пропуск event API")

    event = await client.event.get_event(event_id)
    home = event.homeTeam.name if event.homeTeam else "?"
    away = event.awayTeam.name if event.awayTeam else "?"
    stats = await client.event.get_statistics(event_id)
    stat_count = sum(
        len(g.statisticsItems or [])
        for s in (stats.statistics or [])
        for g in (s.groups or [])
    )
    return ok(f"id={event_id}: {home} vs {away}, {stat_count} метрик")


async def _check_player_via_search(client: SofaScoreClient) -> str:
    player_id = None
    async for item in client.search.search_players("Bruno"):
        if item.type == "player" and hasattr(item.entity, "id"):
            player_id = item.entity.id
            break
    if not player_id:
        return ok("игрок через поиск не найден — пропуск player API")

    player = await client.player.get_player(player_id)
    team = player.team.name if player.team else "—"
    return ok(f"{player.name} (id={player_id}), команда: {team}")


def print_summary(results: list[CheckResult]) -> int:
    section("Итог")
    passed = sum(1 for r in results if r.ok)
    failed = len(results) - passed
    print(f"  Успешно: {passed}/{len(results)}")
    print(f"  Ошибок:  {failed}/{len(results)}")

    if failed and all("403" in r.detail for r in results if not r.ok):
        print(
            "\n  Подсказка: все запросы вернули 403. SofaScore блокирует бота.\n"
            "  Скопируйте cookies из браузера (DevTools → Network → api.sofascore.com)\n"
            "  и задайте переменную окружения SOFASCORE_COOKIES:\n"
            '\n    export SOFASCORE_COOKIES=\'{"имя_cookie": "значение"}\'\n'
        )
    elif failed:
        print("\n  Неудачные проверки:")
        for r in results:
            if not r.ok:
                print(f"    - {r.name}")

    return 0 if failed == 0 else 1


async def main() -> int:
    print("Проверка aiosofascore")
    print(f"  TEAM_ID={TEAM_ID}, TOURNAMENT_ID={TOURNAMENT_ID}, SEARCH={SEARCH_QUERY!r}")

    try:
        async with SofaScoreClient() as client:
            results = await verify(client)
    except Exception:
        traceback.print_exc()
        return 1

    return print_summary(results)


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
