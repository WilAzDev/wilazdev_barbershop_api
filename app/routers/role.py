from typing import Dict,Annotated,List
from fastapi import APIRouter, Depends,status,Response
from fastapi.responses import JSONResponse
from fastapi_pagination import Page

from app.schemas import (
    RoleRead,
    RoleCreate,
    RoleUpdate,
    TokenData,
    RoleSync
)
from app.services import RoleService
from app.dependencies import get_role_service
from app.security import CurrentUser

router = APIRouter(prefix="/roles",tags=["roles"])

@router.get(
    "/",
    response_model=Page[RoleRead],
    tags=["get_list"],
)
async def get_roles(
    current_user:CurrentUser,
    service: RoleService = Depends(get_role_service)
):
    return await service.list()

@router.get(
    "/{role_id}",
    response_model=RoleRead,
    tags=["get_by"]
)
async def get_role(
    current_user:CurrentUser,
    role_id: int,
    service: RoleService = Depends(get_role_service)
):
    return await service.get(role_id)

@router.post(
    "/",
    response_model=RoleRead,
    tags=["create"],
    status_code=status.HTTP_201_CREATED
)
async def create_role(
    current_user:CurrentUser,
    role: RoleCreate,
    service: RoleService = Depends(get_role_service)
):
    return await service.create(role)

@router.post(
    "/user/{user_id}/sync",
    response_model=Page[RoleRead],
    tags=["user_roles"]
)
async def sync_user_roles(
    current_user:CurrentUser,
    user_id: int,
    payload:RoleSync,
    service: RoleService = Depends(get_role_service)
):
    return await service.sync_roles(user_id, payload)

@router.put(
    "/{role_id}",
    response_model=RoleRead,
    tags=["update"]
)
async def update_role(
    current_user:CurrentUser,
    role_id: int,
    payload: RoleUpdate,
    service: RoleService = Depends(get_role_service)
):
    return await service.update(role_id, payload)

@router.delete(
    "/{role_id}",
    response_model=Dict[str,str],
    tags=["delete"]
)
async def delete_role(
    current_user:CurrentUser,
    role_id: int,
    service: RoleService = Depends(get_role_service)
):
    result = await service.delete(role_id)
    return Response(
        status_code=status.HTTP_200_OK,
        content=result['message']
    )