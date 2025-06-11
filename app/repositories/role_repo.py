from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories import SQLModelRepository
from app.models import Role

class RoleRepository(SQLModelRepository[Role]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Role,session=session)