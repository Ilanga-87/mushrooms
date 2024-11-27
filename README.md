
  
# FastAPI приложение для работы с 2 сущностями: грибы и корзинки (с грибами)
Функциональность:  
  
- POST Создать гриб
- PUT Обновить информацию о грибе
- GET Получить конкретный гриб (по id)

- POST Создать корзинку
- POST Положить в корзинку гриб
- DELETE Удалить из корзинки гриб
- GET Получить конкретную корзинку (по id). (Вместе с развернутой инфой по грибам) 
  
## Пререквизиты  
- Docker  
Ставить базу данных отдельно не требуется, в Докере есть PostgreSQL. Если запущены другие версии PostgreSQL, могут возникнуть конфликты из-за порта

## Подготовка окружения
В директории с проектом cоздайте файл .env. Пример наполнения:  
  ```
ENV=dev
POSTGRES_DB=harvest
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

  
## Установка  
Из директории с проектом запустите команду  
  ```
 docker compose up -d --build
 ```
 Сервис доступен по адресу http://127.0.0.1:8000
  
  
## Миграции  
  ```
docker exec mushroomapp alembic upgrade head
```
## Тестирование  
Для заполнения базы данных тестовыми данными  
  ```
 docker exec mushroomapp python database/populate_db.py  
 ```
Для запуска тестов  
  ```
 docker exec mushroomapp python -m pytest tests/test_mushrooms.py
 ```
```
docker exec mushroomapp python -m pytest tests/test_baskets.py
```