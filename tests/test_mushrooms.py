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


async def test_get_single_mushroom():
    """
    Проверяет получение существующего гриба.
    """
    expected_mushroom = {
        "id": 1,
        "name": "Белый гриб",
        "is_edible": True,
        "weight": 150.0,
        "freshness": True,
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/mushrooms/1")
    assert response.status_code == 200
    assert response.json() == expected_mushroom


async def test_get_single_mushroom_non_existing_id():
    """
    Проверяет поведение при запросе несуществующего гриба.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/mushrooms/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Object not found."}


async def test_add_single_mushroom_standard():
    """
    Проверяет добавление нового гриба.
    """
    new_mushroom = {
        "name": "Лисичка",
        "is_edible": True,
        "weight": 100.0,
        "freshness": True
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/mushrooms/", json=new_mushroom)
    assert response.status_code == 201

    response_json = response.json()
    assert response_json["name"] == new_mushroom["name"]
    assert response_json["is_edible"] == new_mushroom["is_edible"]
    assert response_json["weight"] == new_mushroom["weight"]
    assert response_json["freshness"] == new_mushroom["freshness"]


async def test_update_single_mushroom_standard():
    """
    Проверяет обновление данных гриба.
    """
    update_data = {"weight": 120.0}
    expected_mushroom = {
        "id": 1,
        "name": "Белый гриб",
        "is_edible": True,
        "weight": 120.0,
        "freshness": True,
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/mushrooms/1", json=update_data)
    assert response.status_code == 200
    assert response.json() == expected_mushroom


async def test_update_single_mushroom_non_existing_id():
    """
    Проверяет поведение при обновлении несуществующего гриба.
    """
    update_data = {"weight": 200.0}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/mushrooms/999", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "This entry does not exist"}


