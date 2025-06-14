from typing import List
from sqlmodel import select,delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories import SQLModelRepository
from app.models import Role,UserHasRole

class RoleRepository(SQLModelRepository[Role]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Role,session=session)
    
    def get_user_roles_query(self, user_id: int):
        query = select(Role).join(UserHasRole).where(UserHasRole.user_id == user_id)
        return query
    
    async def add_user_missing_roles(self,user_id:int,roles_id:List[int]):
        query = self.get_user_roles_query(user_id)
        
        existing_roles = await self.session.exec(query)
        current_roles_id = [r.id for r in existing_roles]
        roles_to_add_id = set(roles_id) - set(current_roles_id)
        roles_to_add = [
            UserHasRole(user_id=user_id,role_id=r_id)
            for r_id in roles_to_add_id
        ]
        self.session.add_all(roles_to_add)
        await self.session.commit()
    
    async def remove_user_extra_roles(self,user_id:int, roles_id:List[int]):
        query = delete(UserHasRole)\
            .where(UserHasRole.user_id == user_id)\
            .where(~UserHasRole.role_id.in_(roles_id))
        await self.session.exec(query)
        await self.session.commit()