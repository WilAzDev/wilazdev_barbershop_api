from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import status,HTTPException

from app.services import AsyncCrudService
from app.schemas import RoleRead,RoleCreate,RoleUpdate
from app.models import Role
from app.repositories import RoleRepository

class RoleService(AsyncCrudService[Role,RoleRead,RoleCreate,RoleUpdate]):
    def __init__(
        self,
        session: AsyncSession,
    ):
        repo = RoleRepository(session)
        super().__init__(
            model=Role,
            repo=repo,
            session=session,
            read_schema=RoleRead,
            create_schema=RoleCreate,
            update_schema=RoleUpdate,
        )