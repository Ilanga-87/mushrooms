import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi import Query, APIRouter

from schemas.basket_schemas import *
from services.basket_service import BasketService
from .dependencies import baskets_service

logging.basicConfig(level=logging.INFO)

router = APIRouter(
    prefix="/baskets",
    tags=["Baskets"],
)


@router.get("/")
async def root():
    return "Basket service is working"


@router.get("/{basket_id}", response_model=BasketFilled)
async def get_single_basket(
       basket_service: Annotated[BasketService, Depends(baskets_service)], basket_id: int
):
    try:
        basket = await basket_service.get_basket_with_mushrooms(basket_id)
        return basket
    except HTTPException as e:
        raise e


@router.post("/", response_model=Basket, status_code=201)
async def create_single_basket(
        basket_service: Annotated[BasketService, Depends(baskets_service)],
        basket_data: BasketCreate
):
    try:
        basket = await basket_service.create_single_basket(basket_data)
        return basket
    except HTTPException as e:
        logging.error(f"HTTPException: {e.detail}")
        raise e


@router.delete("/{basket_id}")
async def delete_mushroom_from_basket(
        basket_service: Annotated[BasketService, Depends(baskets_service)],
        basket_id: int,
        mushroom_id: int = Query(..., alias="mushroom_id")
):
    try:
        updated_basket = await basket_service.delete_mushroom_from_basket(basket_id, mushroom_id)
        if updated_basket:
            return {"message": "Mushroom successfully deleted."}
    except HTTPException as e:
        raise e


@router.post("/{basket_id}", response_model=BasketFilled)
async def add_mushroom_to_basket(
        basket_service: Annotated[BasketService, Depends(baskets_service)],
        basket_id: int,
        mushroom_id: int = Query(..., alias="mushroom_id")
):
    try:
        filled_basket = await basket_service.add_mushroom_to_basket(basket_id, mushroom_id)
        return filled_basket
    except HTTPException as e:
        raise e
