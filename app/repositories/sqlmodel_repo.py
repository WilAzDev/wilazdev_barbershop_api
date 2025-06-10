from typing import Type,TypeVar,Generic,Dict, Any, List,Optional
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func

ModelType = TypeVar('ModelType',bound=SQLModel)

class SQLModelRepository(Generic[ModelType]):
    def __init__(self,model: Type[ModelType],session:AsyncSession):
        self.model = model
        self.session = session
        
    def get_query(self):
        return select(self.model)
    
    async def get_count(self)->int:
        statement = select(func.count()).select_from(self.model)
        result = await self.session.execute(statement)
        return result.scalar_one()
    
    async def get_by_id(self,item_id:int) -> Optional[ModelType]:
        return await self.session.get(self.model,item_id)
    
    async def get_many_by_field(self,field_name:str,value:Any) -> Optional[List[ModelType]]:
        statement = select(self.model).where(getattr(self.model,field_name)==value)
        result = await self.session.exec(statement)
        return result.all()
    
    async def get_one_by_field(self,field_name:str,value:Any) -> Optional[ModelType]:
        statement = select(self.model).where(getattr(self.model,field_name)==value)
        result = await self.session.exec(statement)
        return result.one_or_none()
    
    async def create(self, item:ModelType) -> ModelType:
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item
    
    async def update(self, item: ModelType, data: Dict[str, Any]) -> ModelType:
        for key,value in data.items():
            setattr(item,key,value)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item
    
    async def delete(self, item: ModelType) -> None:
        self.session.delete(item)
        await self.session.commit()