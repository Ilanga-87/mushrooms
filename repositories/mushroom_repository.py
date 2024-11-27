from models.models import MushroomModel
from utils.repository import SQLAlchemyRepository


class MushroomRepository(SQLAlchemyRepository):
    model = MushroomModel
