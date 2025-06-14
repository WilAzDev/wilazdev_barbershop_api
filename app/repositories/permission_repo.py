from typing import List
from sqlmodel import select,delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories import SQLModelRepository
from app.models import Permission,RoleHasPermission,UserHasPermission

class PermissionRepository(SQLModelRepository[Permission]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Permission,session=session)
        
    def get_role_permissions_query(self, role_id: int):
        query = select(Permission).join(RoleHasPermission).where(RoleHasPermission.role_id == role_id)
        return query
    
    def get_user_permissions_query(self, user_id: int):
        query = select(Permission).join(UserHasPermission).where(UserHasPermission.user_id == user_id)
        return query
    
    async def add_role_missing_permissions(self,role_id:int,permissions_id:List[int]):
        query = self.get_role_permissions_query(role_id)
        existing_permissions = await self.session.exec(query)
        existing_permissions_id = [p.id for p in existing_permissions]
        permissions_to_add_id = set(permissions_id) - set(existing_permissions_id)
        permissions_to_add = [
            RoleHasPermission(role_id=role_id,permission_id=p_id)
            for p_id in permissions_to_add_id
        ]
        self.session.add_all(permissions_to_add)
        await self.session.commit()
        
    async def add_user_missing_permissions(self,user_id:int,permissions_id:List[int]):
        query = self.get_user_permissions_query(user_id)
        existing_permissions = await self.session.exec(query)
        existing_permissions_id = [p.id for p in existing_permissions]
        permissions_to_add_id = set(permissions_id) - set(existing_permissions_id)
        permissions_to_add = [
            UserHasPermission(user_id=user_id,permission_id=p_id)
            for p_id in permissions_to_add_id
        ]
        self.session.add_all(permissions_to_add)
        await self.session.commit()
        
    async def remove_role_extra_permissions(self,role_id:int,permissions_id:List[int]):
        query = delete(RoleHasPermission)\
            .where(RoleHasPermission.role_id == role_id)\
            .where(~RoleHasPermission.permission_id.in_(permissions_id))
        await self.session.exec(query)
        await self.session.commit()
        
    async def remove_user_extra_permissions(self,user_id:int,permissions_id:List[int]):
        query = delete(UserHasPermission)\
            .where(UserHasPermission.user_id == user_id)\
            .where(~UserHasPermission.permission_id.in_(permissions_id))
        await self.session.exec(query)
        await self.session.commit()