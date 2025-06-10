from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import status,HTTPException

from app.services import AsyncCrudService
from .auth_service import AuthService
from app.models import User
from app.schemas import UserRead,UserUpdate,UserCreate,UserAuth,UserInDb
from app.repositories import UserRepository

class UserService(AsyncCrudService[User,UserRead,UserCreate,UserUpdate]):
    def __init__(
        self,
        session: AsyncSession,
    ):
        repo = UserRepository(session)
        super().__init__(
            model=User,
            repo=repo,
            session=session,
            read_schema=UserRead,
            create_schema=UserCreate,
            update_schema=UserUpdate,
        )
    
    async def get_by_email(self, email: str) ->  UserRead:
        user = await self.repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        return UserRead.model_validate(user)
    
    async def authenticate_user(self,payload:UserAuth)-> UserInDb:
        user = await self.repo.get_by_email(payload.email)
        data = user.model_dump()
        user_db = UserInDb.model_validate(user,from_attributes=True)
        if not AuthService().verify_password(
            payload.password,
            user_db.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_db
    
    async def create(self, payload:UserCreate) -> UserRead:
        if payload.password != payload.password2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )
        if await self.repo.get_by_email(payload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        new_user = payload.model_dump()
        new_user['hashed_password'] = AuthService().get_password_hash(payload.password)
        del new_user['password']
        del new_user['password2']
        new_user = await self.repo.create(User(**new_user))
        user = UserRead.model_validate(new_user)
        return user