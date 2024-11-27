import logging
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, HTTPException

from schemas.basket_schemas import *
from schemas.mushroom_schemas import *
from services.mushroom_service import MushroomService
from .dependencies import mushrooms_service

logging.basicConfig(level=logging.INFO)

router = APIRouter(
    prefix="/mushrooms",
    tags=["Mushrooms"],
)


@router.get("/", response_model=List[Mushroom])
async def get_all_mushrooms(mushroom_service: Annotated[MushroomService, Depends(mushrooms_service)]):
    try:
        mushrooms = await mushroom_service.get_all_mushrooms()
        return mushrooms
    except HTTPException as e:
        print(str(e))
        raise e


@router.get("/{id}", response_model=Mushroom)
async def get_single_mushroom(
       mushroom_service: Annotated[MushroomService, Depends(mushrooms_service)], id: int
):
    try:
        mushroom = await mushroom_service.get_single_mushroom(id)
        return mushroom
    except HTTPException as e:
        raise e


@router.post("/", response_model=Mushroom, status_code=201)
async def create_single_mushroom(
        mushroom_service: Annotated[MushroomService, Depends(mushrooms_service)],
        mushroom_data: MushroomCreate
):
    try:
        mushroom = await mushroom_service.create_single_mushroom(mushroom_data)
        return mushroom
    except HTTPException as e:
        logging.error(f"HTTPException: {e.detail}")
        raise e


@router.put("/{id}", response_model=Mushroom)
async def update_single_mushroom(
    id: int,
    mushroom_service: Annotated[MushroomService, Depends(mushrooms_service)],
    mushroom_data: MushroomUpdate
):
    try:
        mushroom = await mushroom_service.update_single_mushroom(id, mushroom_data)
        return mushroom
    except HTTPException as e:
        raise e
