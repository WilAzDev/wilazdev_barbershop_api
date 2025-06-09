from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_async_session
from app.services import (
    UserService
)

async def get_user_service(
    session: AsyncSession = Depends(get_async_session)
) -> UserService:
    return UserService(session)