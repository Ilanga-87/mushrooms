from typing import List

from fastapi import HTTPException

from mixins.basket_mixins import BasketRepositoryMixin
from models.models import BasketModel
from schemas.basket_schemas import BasketFilled, BasketCreate
from utils.repository import AbstractRepository


class BasketService:
    def __init__(self, basket_repo: AbstractRepository):
        self.basket_repo: AbstractRepository = basket_repo()

    async def get_all_baskets(self, skip: int = 0, limit: int = 10) -> List[BasketModel]:
        all_baskets = await self.basket_repo.get_all(skip=skip, limit=limit)
        return all_baskets

    async def create_single_basket(self, basket: BasketCreate) -> BasketModel:
        basket_dict = basket.model_dump()
        added_basket = await self.basket_repo.add_one(basket_dict)
        return added_basket

    async def get_single_basket(self, basket_id: int) -> BasketModel:
        basket = await self.basket_repo.get_one(basket_id)
        if not basket:
            raise HTTPException(status_code=404, detail="Object not found.")
        return basket

    async def delete_mushroom_from_basket(self, basket_id: int, mushroom_id: int):
        if isinstance(self.basket_repo, BasketRepositoryMixin):
            return await self.basket_repo.delete_mushroom_from_basket(basket_id, mushroom_id)
        else:
            raise NotImplementedError("This repository does not support unique methods.")

    async def get_basket_with_mushrooms(self, id: int):
        if isinstance(self.basket_repo, BasketRepositoryMixin):
            return await self.basket_repo.get_basket_with_mushrooms(id)
        else:
            raise NotImplementedError("This repository does not support unique methods.")

    async def add_mushroom_to_basket(self, basket_id: int, mushroom_id: int) -> BasketFilled:
        if isinstance(self.basket_repo, BasketRepositoryMixin):
            await self.basket_repo.add_mushroom_to_basket(basket_id, mushroom_id)
            return await self.basket_repo.get_basket_with_mushrooms(basket_id)
        else:
            raise NotImplementedError("This repository does not support unique methods.")
