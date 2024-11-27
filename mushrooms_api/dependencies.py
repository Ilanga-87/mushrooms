from repositories.mushroom_repository import MushroomRepository
from services.mushroom_service import MushroomService


def mushrooms_service():
    return MushroomService(MushroomRepository)
