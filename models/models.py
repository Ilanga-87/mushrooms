from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from schemas.basket_schemas import BasketFilled, Basket
from schemas.mushroom_schemas import Mushroom

Base = declarative_base()


class BasketModel(Base):
    __tablename__ = "baskets"

    id = Column(Integer, primary_key=True)
    owner = Column(String, nullable=False)
    capacity = Column(Float, nullable=False)
    mushrooms = relationship("MushroomModel", backref="basket")

    def to_read_model(self) -> Basket:
        return Basket(
            id=self.id,
            owner=self.owner,
            capacity=self.capacity,
        )

    def to_read_model_with_mushrooms(self) -> BasketFilled:
        mushrooms_data = [mushroom.to_read_model() for mushroom in self.mushrooms]
        return BasketFilled(
            id=self.id,
            owner=self.owner,
            capacity=self.capacity,
            mushrooms=mushrooms_data,
        )


class MushroomModel(Base):
    __tablename__ = "mushrooms"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_edible = Column(Boolean, nullable=False)
    weight = Column(Float, nullable=False)
    freshness = Column(Boolean, nullable=False)
    basket_id = Column(Integer, ForeignKey("baskets.id", ondelete="SET NULL"), nullable=True)

    def to_read_model(self) -> Mushroom:
        return Mushroom(
            id=self.id,
            name=self.name,
            is_edible=self.is_edible,
            weight=self.weight,
            freshness=self.freshness,
        )
