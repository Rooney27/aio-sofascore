import asyncio
from aiosofascore.client import SofaScoreClient


async def main():
    async with SofaScoreClient() as client:
        # Поиск менеджеров по имени Alexander
        print("=== Менеджеры с именем Alexander ===")
        async for result in client.search.search_managers("Alexander"):
            name = (
                result.entity.name
                if result.entity and hasattr(result.entity, "name")
                else "-"
            )
            team = (
                result.entity.team.name
                if result.entity
                and hasattr(result.entity, "team")
                and result.entity.team
                and hasattr(result.entity.team, "name")
                else "-"
            )
            print(f"Имя: {name}, Тип: {result.type}, Команда: {team}")
            print("===================")
        # Поиск матчей Arsenal vs Manchester united
        print("=== Матчи Arsenal vs Manchester united ===")
        async for result in client.search.search_events("Arsenal vs Manchester united"):
            if result.entity and hasattr(result.entity, "name"):
                name = result.entity.name
            else:
                name = "-"
            if result.entity and hasattr(result.entity, "startTimestamp"):
                start = result.entity.startTimestamp
            else:
                start = "-"
            status = (
                result.entity.status.type
                if result.entity
                and hasattr(result.entity, "status")
                and result.entity.status
                and hasattr(result.entity.status, "type")
                else "-"
            )
            home_score = (
                result.entity.homeScore.display
                if result.entity
                and hasattr(result.entity, "homeScore")
                and result.entity.homeScore
                and hasattr(result.entity.homeScore, "display")
                else "-"
            )
            away_score = (
                result.entity.awayScore.display
                if result.entity
                and hasattr(result.entity, "awayScore")
                and result.entity.awayScore
                and hasattr(result.entity.awayScore, "display")
                else "-"
            )
            print(f"Матч: {name}, Дата: {start}")
            if status == "finished":
                print(f"Счёт: {home_score} - {away_score}")
            print("===================")


if __name__ == "__main__":
    asyncio.run(main())
