import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.exc import OperationalError

from config import configs
from database.db import Database
from main import app

pytestmark = pytest.mark.asyncio


async def test_database_connection():
    """
    Проверяет возможность подключения к базе данных.
    """
    database = Database(configs.DATABASE_URI)

    try:
        async with database._engine.connect():
            assert True
    except OperationalError:
        assert False


async def test_root():
    """
    Проверяет корневой эндпоинт.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == "service is working"


async def test_basket_root():
    """
    Проверяет корневой эндпоинт для корзины.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/baskets/")
    assert response.status_code == 200
    assert response.json() == "Basket service is working"


async def test_add_mushroom_to_basket():
    """
    Проверяет добавление гриба в корзину.
    """
    basket_id = 1
    mushroom_id = 1
    expected_basket = {
      "owner": "Иван Иванов",
      "capacity": 5000.0,
      "id": 1,
      "mushrooms": [
        {
          "name": "Белый гриб",
          "is_edible": True,
          "weight": 120.0,
          "freshness": True,
          "id": 1
        }
      ]
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/baskets/{basket_id}?mushroom_id={mushroom_id}")

    assert response.status_code == 200
    assert response.json() == expected_basket


async def test_add_mushroom_to_basket_nonexisting_basket():
    """
    Проверяет попытку добавления гриба в несуществующую корзину.
    """
    nonexistent_basket_id = 999
    mushroom_id = 1

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/baskets/{nonexistent_basket_id}?mushroom_id={mushroom_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Basket not found"


async def test_add_mushroom_to_basket_nonexisting_mushroom():
    """
    Проверяет попытку добавления несуществующего гриба в корзину.
    """
    basket_id = 1
    nonexistent_mushroom_id = 999

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/baskets/{basket_id}?mushroom_id={nonexistent_mushroom_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Mushroom not found"


async def test_add_mushroom_to_basket_overflow():
    """
    Проверяет добавление гриба в корзину с превышением лимита веса.
    """
    basket_id = 1

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/baskets/{basket_id}")  # Получаем текущую корзину
        basket = response.json()

    # Считаем лимит
    current_weight = sum(m["weight"] for m in basket["mushrooms"])
    limit = basket["capacity"]

    # Создаем новый гриб, который превышает лимит
    new_mushroom = {
        "name": "Большой гриб",
        "is_edible": True,
        "weight": limit - current_weight + 1,
        "freshness": True
    }

    # Добавляем новый гриб в бд
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/mushrooms/", json=new_mushroom)
        new_mushroom_id = response.json()["id"]

    # Пытаемся добавить гриб в корзину
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/baskets/{basket_id}?mushroom_id={new_mushroom_id}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Basket is full"


async def test_add_mushroom_to_basket_already_in_basket():
    """
    Проверяет добавление гриба в корзину, если он уже находится в другой корзине.
    """
    basket_id = 1
    mushroom_id = 1

    # Пытаемся добавить гриб в корзину первый раз
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/baskets/{basket_id}?mushroom_id={mushroom_id}")

    # Теперь пытаемся снова добавить этот же гриб в ту же корзину
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/baskets/{basket_id}?mushroom_id={mushroom_id}")

    # Проверяем, что получили ошибку, так как гриб уже в корзине
    assert response.status_code == 400
    assert response.json()["detail"] == "Mushroom is already in a basket"



async def test_get_single_basket():
    """
    Проверяет получение существующей корзины.
    """
    expected_basket = {
      "owner": "Иван Иванов",
      "capacity": 5000.0,
      "id": 1,
      "mushrooms": [
        {
          "name": "Белый гриб",
          "is_edible": True,
          "weight": 120.0,
          "freshness": True,
          "id": 1
        }
      ]
}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/baskets/1")
    assert response.status_code == 200
    assert response.json() == expected_basket


async def test_get_single_basket_non_existing_id():
    """
    Проверяет поведение при запросе несуществующей корзины.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/baskets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Basket not found"}



async def test_delete_mushroom_from_basket():
    """
    Проверяет удаление гриба из корзины.
    """
    basket_id = 1
    mushroom_id = 1

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/baskets/{basket_id}?mushroom_id={mushroom_id}")

    assert response.status_code == 200
    assert response.json() == {"message": "Mushroom successfully deleted."}


async def test_delete_mushroom_from_basket_nonexisting_basket():
    """
    Проверяет попытку добавления гриба в несуществующую корзину.
    """
    nonexistent_basket_id = 999
    mushroom_id = 1

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/baskets/{nonexistent_basket_id}?mushroom_id={mushroom_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Basket not found"


async def test_delete_mushroom_from_basket_nonexisting_mushroom():
    """
    Проверяет попытку добавления несуществующего гриба в корзину.
    """
    basket_id = 1
    nonexistent_mushroom_id = 999

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(f"/baskets/{basket_id}?mushroom_id={nonexistent_mushroom_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Mushroom not found"


async def test_create_single_basket():
    """
    Проверяет создание новой корзины.
    """
    new_basket = {
      "owner": "Петр Петров",
      "capacity": 3000
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/baskets/", json=new_basket)

    assert response.status_code == 201
    response_json = response.json()
    assert "id" in response_json


