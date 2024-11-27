from abc import abstractmethod, ABC
from typing import Any


class BasketRepositoryMixin(ABC):
    @abstractmethod
    async def get_basket_with_mushrooms(self, id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def add_mushroom_to_basket(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def delete_mushroom_from_basket(self, *args, **kwargs) -> Any:
        raise NotImplementedError
