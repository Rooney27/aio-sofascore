#!/usr/bin/env python3
"""
Скрипт для ручной проверки работоспособности aiosofascore.

Запуск:
    pip install -e ".[curl]"
    python examples/verify_library.py

Cookies (обязательно для обхода 403):
    1. DevTools → Network → запрос к www.sofascore.com/api/... → Request Headers → Cookie
    2. Сохраните в cookies.txt (вся строка Cookie как есть)
    3. export SOFASCORE_COOKIES_FILE=cookies.txt
    python examples/verify_library.py

Важно: одних cookies в Python-коде часто недостаточно.
SofaScore проверяет TLS-отпечаток браузера — нужен transport=curl (curl_cffi).
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import traceback
from dataclasses import dataclass
from typing import Awaitable, Callable

from aiosofascore.adapters.http_client import (
    _curl_available,
    load_cookies_from_file,
    parse_cookie_header,
)
from aiosofascore.client import SofaScoreClient
from aiosofascore.exception import ResponseParseContentError

TEAM_ID = 2819
TOURNAMENT_ID = 17
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
        print(f"    → HTTP {exc.status}")
        for line in detail.strip().splitlines()[2:5]:
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
        await run_check("team.info.get_team_info", lambda: _check_team_info(client))
    )
    results.append(
        await run_check(
            "team.players.get_team_players", lambda: _check_team_players(client)
        )
    )
    results.append(
        await run_check(
            "team.last_events.get_last_events", lambda: _check_last_events(client)
        )
    )
    results.append(
        await run_check(
            "team.rankings.get_team_rankings", lambda: _check_rankings(client)
        )
    )

    section("2. Search — поиск")
    results.append(
        await run_check("search.search_teams", lambda: _check_search_teams(client))
    )

    section("3. Live — live-матчи")
    results.append(await run_check("live.get_live_events", lambda: _check_live(client)))

    section("4. Tournament — турниры")
    results.append(
        await run_check("tournament.get_categories", lambda: _check_categories(client))
    )
    results.append(
        await run_check(
            "tournament.get_standings", lambda: _check_standings(client, TOURNAMENT_ID)
        )
    )

    section("5. Team statistics — статистика команды")
    results.append(
        await run_check("team.statistics", lambda: _check_team_statistics(client))
    )

    section("6. Event — матч (через поиск)")
    results.append(
        await run_check("event via search", lambda: _check_event_via_search(client))
    )

    section("7. Player — игрок (через поиск)")
    results.append(
        await run_check("player via search", lambda: _check_player_via_search(client))
    )

    return results


async def _check_team_info(client: SofaScoreClient) -> str:
    info = await client.team.info.get_team_info(TEAM_ID)
    return ok(f"{info.name} (id={info.id})")


async def _check_team_players(client: SofaScoreClient) -> str:
    data = await client.team.players.get_team_players(TEAM_ID)
    count = len(data.players or [])
    return ok(f"{count} игроков")


async def _check_last_events(client: SofaScoreClient) -> str:
    data = await client.team.last_events.get_last_events(TEAM_ID, page=0)
    return ok(f"{len(data.events or [])} матчей, hasNextPage={data.hasNextPage}")


async def _check_rankings(client: SofaScoreClient) -> str:
    data = await client.team.rankings.get_team_rankings(TEAM_ID)
    return ok(f"{len(data.rankings or [])} записей")


async def _check_search_teams(client: SofaScoreClient) -> str:
    names = []
    async for item in client.search.search_teams(SEARCH_QUERY):
        names.append(item.entity.name)
        if len(names) >= 3:
            break
    return ok(", ".join(names) or "ничего")


async def _check_live(client: SofaScoreClient) -> str:
    data = await client.live.get_live_events()
    return ok(f"{len(data.events or [])} live-матчей")


async def _check_categories(client: SofaScoreClient) -> str:
    data = await client.tournament.get_categories()
    return ok(f"{len(data.categories or [])} категорий")


async def _check_standings(client: SofaScoreClient, tournament_id: int) -> str:
    seasons = await client.tournament.get_seasons(tournament_id)
    if not seasons.seasons:
        return ok("сезоны не найдены")
    data = await client.tournament.get_standings(tournament_id, seasons.seasons[0].id)
    top = data.rows[0] if data.rows else None
    return ok(f"лидер: {top.team.name} ({top.points} pts)" if top else "таблица пуста")


async def _check_team_statistics(client: SofaScoreClient) -> str:
    seasons = await client.team.statistics_seasons.get_statistics_seasons(TEAM_ID)
    if not seasons.uniqueTournamentSeasons:
        return ok("нет сезонов")
    item = seasons.uniqueTournamentSeasons[0]
    season = item.seasons[0] if item.seasons else None
    if not item.uniqueTournament or not season:
        return ok("нет данных")
    stats = await client.team.statistics.get_statistics(
        TEAM_ID, item.uniqueTournament.id, season.id
    )
    return ok(f"полей статистики: {len(stats.statistics or {})}")


async def _check_event_via_search(client: SofaScoreClient) -> str:
    event_id = None
    async for item in client.search.search_events(f"{SEARCH_QUERY} vs"):
        event_id = item.entity.id
        break
    if not event_id:
        return ok("матч не найден через search")
    event = await client.event.get_event(event_id)
    return ok(f"{event.homeTeam.name} vs {event.awayTeam.name}")


async def _check_player_via_search(client: SofaScoreClient) -> str:
    player_id = None
    async for item in client.search.search_players("Bruno"):
        player_id = item.entity.id
        break
    if not player_id:
        return ok("игрок не найден через search")
    player = await client.player.get_player(player_id)
    return ok(f"{player.name}")


def load_cookies(args: argparse.Namespace) -> dict[str, str]:
    if args.cookies_file:
        return load_cookies_from_file(args.cookies_file)
    if args.cookie_header:
        return parse_cookie_header(args.cookie_header)
    if os.getenv("SOFASCORE_COOKIES_FILE"):
        return load_cookies_from_file(os.environ["SOFASCORE_COOKIES_FILE"])
    return {}


def print_startup_info(args: argparse.Namespace, cookies: dict[str, str]) -> None:
    transport = args.transport or os.getenv("SOFASCORE_TRANSPORT", "auto")
    curl_ok = _curl_available()
    print("Проверка aiosofascore")
    print(f"  TEAM_ID={TEAM_ID}, SEARCH={SEARCH_QUERY!r}")
    print(f"  transport={transport}, curl_cffi={'да' if curl_ok else 'нет'}")
    print(f"  cookies: {len(cookies)} шт.")
    if not cookies:
        print("  ⚠ cookies не заданы")
    if not curl_ok and transport in ("auto", "curl"):
        print("  ⚠ Установите curl_cffi: pip install 'aiosofascore[curl]'")


def print_summary(results: list[CheckResult], transport: str, has_cookies: bool) -> int:
    section("Итог")
    passed = sum(1 for r in results if r.ok)
    failed = len(results) - passed
    print(f"  Успешно: {passed}/{len(results)}")
    print(f"  Ошибок:  {failed}/{len(results)}")

    if failed and all("403" in r.detail for r in results if not r.ok):
        print(
            "\n  Все запросы вернули 403. Cookies сами по себе часто НЕ помогают.\n"
            "  SofaScore (Akamai) проверяет TLS-отпечаток клиента.\n"
            "\n  Что сделать:\n"
            "  1. pip install 'aiosofascore[curl]'\n"
            "  2. Скопируйте Cookie из DevTools для запроса к www.sofascore.com/api/...\n"
            "     (Network → www.sofascore.com → Headers → Cookie — целиком)\n"
            "  3. Сохраните в cookies.txt и запустите:\n"
            "     export SOFASCORE_COOKIES_FILE=cookies.txt\n"
            "     export SOFASCORE_TRANSPORT=curl\n"
            "     python examples/verify_library.py\n"
            "\n  Важно:\n"
            "  - Копируйте Cookie из запроса к API, не из document.cookie\n"
            "  - Нужны HttpOnly cookies (_abck, bm_sz и др.) — их нет в document.cookie\n"
            "  - Cookies быстро устаревают — копируйте прямо перед запуском\n"
            f"  - Сейчас: transport={transport}, cookies={'есть' if has_cookies else 'нет'}\n"
        )
    elif failed:
        print("\n  Неудачные проверки:")
        for r in results:
            if not r.ok:
                print(f"    - {r.name}")

    return 0 if failed == 0 else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Проверка aiosofascore")
    parser.add_argument(
        "--cookies-file", help="Файл cookies (JSON или строка Cookie из DevTools)"
    )
    parser.add_argument("--cookie-header", help="Строка Cookie из DevTools")
    parser.add_argument(
        "--transport",
        choices=["auto", "aiohttp", "curl"],
        default=None,
        help="HTTP transport (по умолчанию auto → curl если установлен curl_cffi)",
    )
    return parser.parse_args()


async def main() -> int:
    args = parse_args()
    cookies = load_cookies(args)
    print_startup_info(args, cookies)

    try:
        async with SofaScoreClient(
            cookies=cookies or None,
            transport=args.transport,
        ) as client:
            print(f"  фактический transport: {client.http.transport}")
            results = await verify(client)
    except ImportError as exc:
        print(f"\n  Ошибка: {exc}")
        return 1
    except Exception:
        traceback.print_exc()
        return 1

    transport = args.transport or os.getenv("SOFASCORE_TRANSPORT", "auto")
    return print_summary(results, transport, bool(cookies))


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
