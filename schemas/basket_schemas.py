from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from .mushroom_schemas import Mushroom


class BasketBase(BaseModel):
    owner: str
    capacity: float

    @field_validator("capacity")
    def capacity_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("capacity must be a positive integer")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "owner": "Иван Иванов",
                    "capacity": 5000.0,
                }
            ]
        }
    }


    class ConfigDict:
        from_attributes = True


class BasketCreate(BasketBase):
    pass


class Basket(BasketBase):
    id: int


class BasketFilled(Basket):
    mushrooms: Optional[List[Mushroom]] = []

    class ConfigDict:
        from_attributes = True
