import asyncio

from system.settings.dependencies import get_settings


async def main():
    settings = await get_settings()
    print(settings.model_dump())


if __name__ == "__main__":
    asyncio.run(main())
