from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_async_session
from app.services import (
    UserService,
    RoleService,
    PermissionService
)

async def get_user_service(
    session: AsyncSession = Depends(get_async_session)
) -> UserService:
    return UserService(session)

async def get_role_service(
    session: AsyncSession = Depends(get_async_session)
) -> RoleService:
    return RoleService(session)

async def get_permission_service(
    session: AsyncSession = Depends(get_async_session)
) -> PermissionService:
    return PermissionService(session)