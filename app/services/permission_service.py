from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import apaginate

from app.services import AsyncCrudService
from app.schemas import PermissionRead,PermissionCreate,PermissionUpdate,PermissionSync
from app.models import Permission
from app.repositories import PermissionRepository

class PermissionService(AsyncCrudService[Permission,PermissionRead,PermissionCreate,PermissionUpdate]):
    def __init__(self, session: AsyncSession):
        self.repo = PermissionRepository(session)
        super().__init__(
            model=Permission,
            repo=self.repo,
            read_schema=PermissionRead,
            create_schema=PermissionCreate,
            update_schema=PermissionUpdate
        )
        
    async def get_role_permissions(self,role_id:int) -> Page[PermissionRead]:
        query = self.repo.get_role_permissions_query(role_id)
        result = await apaginate(self.repo.session,query)
        result.items = [self.read_schema.model_validate(item) for item in result.items]
        return result
    
    async def get_user_permissions(self,user_id:int) ->Page[PermissionRead]:
        query = self.repo.get_user_permissions_query(user_id)
        result = await apaginate(self.repo.session,query)
        result.items = [self.read_schema.model_validate(item) for item in result.items]
        return result
    
    async def sync_role_permissions(self,role_id:int,payload:PermissionSync) -> Page[PermissionRead]:
        await self.repo.add_role_missing_permissions(role_id,payload.permissions_id)
        await self.repo.remove_role_extra_permissions(role_id,payload.permissions_id)
        return await self.get_role_permissions(role_id)
    
    async def sync_user_permissions(self,user_id:int,payload:PermissionSync) -> Page[PermissionRead]:
        await self.repo.add_user_missing_permissions(user_id,payload.permissions_id)
        await self.repo.remove_user_extra_permissions(user_id,payload.permissions_id)
        return await self.get_user_permissions(user_id)