from abc import ABC, abstractmethod
from typing import Any, List

from fastapi import HTTPException
from sqlalchemy import select, insert, exists, update
from sqlalchemy.exc import IntegrityError

from database.db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def get_one(self, item: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, item: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 10) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: Any, **kwargs) -> Any:
        raise NotImplementedError


    def __call__(self):
        return self


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def get_all(self, skip: int = 0, limit: int = 10) -> List[model]:
        async with async_session_maker() as session:
            stmt = select(self.model).offset(skip).limit(limit)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            if len(res) == 0:
                raise HTTPException(status_code=404, detail="Object not found.")
            return res

    async def get_one(self, id: int) -> model:
        try:
            async with async_session_maker() as session:
                stmt = select(self.model).where(self.model.id == id)
                res = await session.execute(stmt)
                obj = res.scalar()
                if not obj:
                    raise HTTPException(status_code=404, detail="Object not found.")
                return obj

        except Exception as e:
            print(f"Error fetching object: {e}")
            raise

    async def add_one(self, data: dict) -> model:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            try:
                res = await session.execute(stmt)
                await session.commit()
                return res.scalar()
            except IntegrityError as e:
                raise HTTPException(
                    status_code=500, detail=str(e)
                )

            except Exception as e:
                print("Error occurred while executing query:", str(e))
                raise

    async def update_one(self, id: int, **kwargs):
        async with async_session_maker() as session:
            stmt_exist = select(exists().where(getattr(self.model, "id") == id))
            res_exist = await session.execute(stmt_exist)
            if not res_exist.scalar():
                raise HTTPException(status_code=404, detail="This entry does not exist")

            stmt = (
                update(self.model)
                .where(getattr(self.model, "id") == id)
                .values(**kwargs)
                .returning(self.model)
            )
            try:
                res = await session.execute(stmt)
                await session.commit()
                return res.scalar()
            except IntegrityError as e:
                raise HTTPException(
                    status_code=500, detail=str(e)
                )

            except Exception as e:
                print("Error occurred while executing query:", e)
                raise
