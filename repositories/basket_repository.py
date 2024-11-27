from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.db import async_session_maker
from mixins.basket_mixins import BasketRepositoryMixin
from models.models import BasketModel
from repositories.mushroom_repository import MushroomRepository
from schemas.basket_schemas import BasketFilled
from utils.repository import SQLAlchemyRepository


class BasketRepository(SQLAlchemyRepository, BasketRepositoryMixin):
    model = BasketModel

    async def _get_basket_with_mushrooms(self, basket_id: int):
        async with async_session_maker() as session:
            # Запрос для получения корзины с грибами
            result = await session.execute(
                select(self.model).
                filter(self.model.id == basket_id).
                options(joinedload(self.model.mushrooms))
            )
            basket = result.scalars().first()

            if not basket:
                raise HTTPException(status_code=404, detail="Basket not found")

            return basket

    async def get_basket_with_mushrooms(self, id: int) -> model:
        basket = await self._get_basket_with_mushrooms(id)

        # Возвращаем корзину в нужном формате
        return basket.to_read_model_with_mushrooms()

    async def add_mushroom_to_basket(self, basket_id: int, mushroom_id: int):
        async with async_session_maker() as session:
            # Проверка существования корзины
            basket = await self._get_basket_with_mushrooms(basket_id)

            # Проверка существования гриба
            mushroom_repo = MushroomRepository()
            try:
                mushroom = await mushroom_repo.get_one(mushroom_id)
            except HTTPException as e:
                if "Object not found." in str(e.detail):
                    raise HTTPException(status_code=404, detail="Mushroom not found")
                raise
            # Проверка свободности гриба
            if mushroom.basket_id is not None:
                raise HTTPException(status_code=400, detail="Mushroom is already in a basket")

            # Валидация веса
            current_weight = sum(m.weight for m in basket.mushrooms)
            limit = basket.capacity
            mushroom_weight = mushroom.weight

            if limit < (mushroom_weight + current_weight):
                raise HTTPException(status_code=400, detail="Basket is full")

            # Добавление гриба в корзину
            mushroom.basket_id = basket.id

            session.add(mushroom)

            try:
                await session.commit()
            except Exception as e:
                print(f"Error during commit: {e}")
                raise HTTPException(status_code=500, detail="Failed to add mushroom to basket")

            await session.refresh(mushroom)

    async def delete_mushroom_from_basket(self, basket_id: int, mushroom_id: int):
        async with async_session_maker() as session:
            # Проверка существования корзины
            basket = await self._get_basket_with_mushrooms(basket_id)

            # Проверка существования гриба
            mushroom_repo = MushroomRepository()
            mushroom = await mushroom_repo.get_one(mushroom_id)
            if not mushroom:
                raise HTTPException(status_code=404, detail="Mushroom not found")

            if mushroom.basket_id != basket.id:
                raise HTTPException(status_code=400, detail="Mushroom is not in this basket")

            # Удаление гриба из корзины
            mushroom.basket_id = None
            await session.commit()

            updated_basket = await self.get_basket_with_mushrooms(basket_id)

            basket_dict = {
                "id": updated_basket.id,
                "owner": updated_basket.owner,
                "capacity": updated_basket.capacity,
                "mushrooms": [
                    {
                        "id": mushroom.id,
                        "name": mushroom.name,
                        "is_edible": mushroom.is_edible,
                        "weight": mushroom.weight,
                        "freshness": mushroom.freshness
                    }
                    for mushroom in updated_basket.mushrooms
                ],
            }

            return BasketFilled.model_validate(basket_dict)

