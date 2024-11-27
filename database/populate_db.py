import asyncio
import logging

from sqlalchemy import insert

from db import Base, engine, async_session_maker
from models.models import BasketModel, MushroomModel
from population_data import basket_data, mushroom_data


async def populate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        for item in basket_data:
            stmt = insert(BasketModel).values(item)
            await session.execute(stmt)
            await session.commit()
        for item in mushroom_data:
            stmt = insert(MushroomModel).values(item)
            await session.execute(stmt)
            await session.commit()
        logging.info("Database was populated")


async def main():
    await populate()


if __name__ == "__main__":
    asyncio.run(main())