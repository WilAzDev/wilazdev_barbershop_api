from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import apaginate

from app.services import AsyncCrudService
from app.schemas import RoleRead,RoleCreate,RoleUpdate,RoleSync
from app.models import Role
from app.repositories import RoleRepository

class RoleService(AsyncCrudService[Role,RoleRead,RoleCreate,RoleUpdate]):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.repo = RoleRepository(session)
        super().__init__(
            model=Role,
            repo=self.repo,
            session=session,
            read_schema=RoleRead,
            create_schema=RoleCreate,
            update_schema=RoleUpdate,
        )
    
    async def get_user_roles(self,user_id:int)-> Page[RoleRead]:
        query = self.repo.get_user_roles_query(user_id)
        result = await apaginate(self.repo.session,query)
        result.items = [self.read_schema.model_validate(item) for item in result.items]
        return result
    
    async def sync_user_roles(self, user_id: int, payload:RoleSync)->Page[RoleRead]:
        await self.repo.add_user_missing_roles(user_id,payload.roles_id)
        await self.repo.remove_user_extra_roles(user_id,payload.roles_id)
        return await self.get_user_roles(user_id)