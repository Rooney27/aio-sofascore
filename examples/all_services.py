"""
Example usage of event, live, tournament, and player services.
"""

import asyncio

from aiosofascore.client import SofaScoreClient

EVENT_ID = 11352523
PLAYER_ID = 12345
TOURNAMENT_ID = 17
SEASON_ID = 52186


async def main():
    async with SofaScoreClient() as client:
        print("=== Live events ===")
        live = await client.live.get_live_events()
        for event in (live.events or [])[:3]:
            home = event.homeTeam.name if event.homeTeam else "-"
            away = event.awayTeam.name if event.awayTeam else "-"
            status = event.status.type if event.status else "-"
            print(f"{home} vs {away} [{status}]")

        print("\n=== Event detail ===")
        event = await client.event.get_event(EVENT_ID)
        print(f"{event.homeTeam.name} vs {event.awayTeam.name}")

        print("\n=== Event statistics ===")
        stats = await client.event.get_statistics(EVENT_ID)
        if stats.statistics and stats.statistics[0].groups:
            for item in stats.statistics[0].groups[0].statisticsItems[:3]:
                print(f"{item.name}: {item.home} - {item.away}")

        print("\n=== Standings ===")
        standings = await client.tournament.get_standings(TOURNAMENT_ID, SEASON_ID)
        for row in (standings.rows or [])[:3]:
            print(f"{row.position}. {row.team.name} — {row.points} pts")

        print("\n=== Player ===")
        player = await client.player.get_player(PLAYER_ID)
        team_name = player.team.name if player.team else "-"
        print(f"{player.name} ({player.position}) — {team_name}")


if __name__ == "__main__":
    asyncio.run(main())
