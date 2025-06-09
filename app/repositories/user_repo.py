from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories import SQLModelRepository
from app.models import User

class UserRepository(SQLModelRepository[User]):
    def __init__(self,session: AsyncSession):
        super().__init__(model=User,session=session)
        
    async def get_by_email(self,email: str):
        return await self.get_one_by_field("email",email)