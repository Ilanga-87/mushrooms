from typing import Optional

from pydantic import BaseModel, field_validator


class MushroomBase(BaseModel):
    name: str
    is_edible: bool
    weight: float
    freshness: bool

    @field_validator("weight")
    def weight_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("weight must be a positive integer")
        return v


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Белый гриб",
                    "is_edible": True,
                    "weight": 150.0,
                    "freshness": True,
                }
            ]
        }
    }


class MushroomCreate(MushroomBase):
    pass


class MushroomUpdate(MushroomBase):
    name: Optional[str] = None
    is_edible: Optional[bool] = None
    weight: Optional[float] = None
    freshness: Optional[bool] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Белый гриб",
                    "is_edible": True,
                    "weight": 150.0,
                    "freshness": True,
                }
            ]
        }
    }


class Mushroom(MushroomBase):
    id: int

    class ConfigDict:
        from_attributes = True

