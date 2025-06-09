from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import status,HTTPException

from app.services import AsyncCrudService
from app.models import User
from app.schemas import UserRead,UserUpdate,UserCreate
from app.repositories import UserRepository

class UserService(AsyncCrudService[User,UserRead,UserCreate,UserUpdate]):
    def __init__(
        self,
        session: AsyncSession,
    ):
        repo = UserRepository(session)
        super().__init__(model=User,repo=repo,session=session)
    
    async def get_by_email(self, email: str) ->  UserRead:
        user = await self.repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        return UserRead.model_validate(user)