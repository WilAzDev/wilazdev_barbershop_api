from typing import Dict
from fastapi import APIRouter,Depends,status,Response
from fastapi.responses import JSONResponse
from fastapi_pagination import Page

from app.schemas import (
    PermissionRead,
    PermissionCreate,
    PermissionUpdate,
    PermissionSync
)
from app.services import PermissionService
from app.dependencies import get_permission_service
from app.security import Auth

router = APIRouter(prefix="/permissions",tags=["permissions"])

@router.get(
    "/",
    response_model=Page[PermissionRead],
    tags=["get_list"],
)
async def get_permissions(
    auth: Auth,
    service: PermissionService = Depends(get_permission_service)
):
    return await service.list(auth)

@router.get(
    "/count",
    response_model=int,
    tags=["get_count"],
)
async def count_roles(
    auth: Auth,
    service: PermissionService = Depends(get_permission_service)
):
    return await service.count()

@router.get(
    "/{role_id}",
    response_model=PermissionRead,
    tags=["get_by"],
)
async def get_permission(
    auth: Auth,
    role_id: int,
    service: PermissionService = Depends(get_permission_service)
):
    return await service.get(role_id)

@router.post(
    "/",
    response_model=PermissionRead,
    tags=["create"],
    status_code=status.HTTP_201_CREATED
)
async def create_permission(
    auth: Auth,
    permission: PermissionCreate,
    service: PermissionService = Depends(get_permission_service)
):
    return await service.create(auth, permission)

@router.post(
    "/role/{role_id}/sync",
    response_model=Page[PermissionRead],
    tags=["roles"],
)
async def sync_role_permissions(
    auth: Auth,
    role_id: int,
    payload: PermissionSync,
    service: PermissionService = Depends(get_permission_service)
):
    return await service.sync_role_permissions(role_id, payload)

@router.post(
    "/user/{user_id}/sync",
    response_model=Page[PermissionRead],
    tags=["users"],
)
async def sync_user_permissions(
    auth: Auth,
    user_id: int,
    payload: PermissionSync,
    service: PermissionService = Depends(get_permission_service)
):
    return await service.sync_user_permissions(user_id, payload)

@router.put(
    "/{permission_id}",
    response_model=PermissionRead,
    tags=["update"],
)
async def update_permission(
    auth: Auth,
    permission_id: int,
    permission: PermissionUpdate,
    service: PermissionService = Depends(get_permission_service)
):
    return await service.update(permission_id, permission)

@router.delete(
    "/{permission_id}",
    response_model=Dict[str,str],
    tags=["delete"],
)
async def delete_permission(
    auth: Auth,
    permission_id: int,
    service: PermissionService = Depends(get_permission_service)
):
    result = await service.delete(permission_id)
    return Response(
        status_code=status.HTTP_200_OK,
        content=result['message']
    )


