from typing import List

from fastapi import HTTPException

from models.models import MushroomModel
from schemas.mushroom_schemas import MushroomCreate, MushroomUpdate, Mushroom
from utils.repository import AbstractRepository


class MushroomService:
    def __init__(self, mushroom_repo: AbstractRepository):
        self.mushroom_repo: AbstractRepository = mushroom_repo()

    async def create_single_mushroom(self, mushroom: MushroomCreate) -> MushroomModel:
        mushroom_dict = mushroom.model_dump()
        added_mushroom = await self.mushroom_repo.add_one(mushroom_dict)
        return added_mushroom

    async def get_all_mushrooms(self, skip: int = 0, limit: int = 10) -> List[MushroomModel]:
        all_mushrooms = await self.mushroom_repo.get_all(skip=skip, limit=limit)
        return all_mushrooms

    async def get_single_mushroom(self, id: int) -> Mushroom:
        mushroom = await self.mushroom_repo.get_one(id)
        mushroom_data = {
            "id": mushroom.id,
            "name": mushroom.name,
            "is_edible": mushroom.is_edible,
            "weight": mushroom.weight,
            "freshness": mushroom.freshness
        }
        return Mushroom.model_validate(mushroom_data)

    async def update_single_mushroom(self, id: int, mushroom_data: MushroomUpdate) -> MushroomModel:
        update_dict = mushroom_data.model_dump(exclude_unset=True)
        updated_mushroom = await self.mushroom_repo.update_one(id, **update_dict)
        if not updated_mushroom:
            raise HTTPException(status_code=404, detail="Object not found.")
        return updated_mushroom
