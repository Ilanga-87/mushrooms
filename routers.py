from baskets_api.basket_app import router as basket_router
from mushrooms_api.mushroom_app import router as mushroom_router

all_routers = [
    basket_router,
    mushroom_router,
]
