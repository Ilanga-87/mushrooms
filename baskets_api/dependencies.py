from repositories.basket_repository import BasketRepository
from services.basket_service import BasketService


def baskets_service():
    return BasketService(BasketRepository)
