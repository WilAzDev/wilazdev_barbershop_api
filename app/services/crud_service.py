from typing import TypeVar, Generic, Dict, Any, Type
from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import apaginate
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel

from app.repositories import SQLModelRepository

ModelType = TypeVar('ModelType', bound=SQLModel)
ReadSchema = TypeVar('ReadSchema', bound=BaseModel)
CreateSchema = TypeVar('CreateSchema',bound=BaseModel)
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)

class AsyncCrudService(Generic[ModelType,ReadSchema,CreateSchema,UpdateSchema]):
    def __init__(
        self,
        model: Type[ModelType],
        repo: SQLModelRepository[ModelType],
        session: AsyncSession
    ):
        self.model = model
        self.repo = repo
        self.session = session

    async def count(self) -> int:
        return await self.repo.get_count()
    
    async def list(self) -> Page[ReadSchema]:
        query = self.repo.get_query()
        result =  await apaginate(self.repo.session,query)
        result.items = [ReadSchema.model_validate(item) for item in result.items]
        return result

    async def get(self, id: int) -> ReadSchema:
        item = await self.repo.get_by_id(id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found for id {id}"
            )
        return ReadSchema.model_validate(item)
    
    async def create(self, payload: CreateSchema) -> ReadSchema:
        obj = self.model(**payload.model_dump())
        result = await self.repo.create(obj)
        return ReadSchema.model_validate(result)
    
    async def update(self, id: int, payload: UpdateSchema) -> ReadSchema:
        item = await self.get(id)
        data = payload.model_dump(exclude_unset=True)
        result = await self.repo.update(item, data)
        return ReadSchema.model_validate(result)
    
    async def delete(self, id: int) -> Dict[str,Any]:
        obj = await self.get(id)
        await self.repo.delete(obj)
        return {"message": f"{self.model.__name__} deleted item with id {id}"}