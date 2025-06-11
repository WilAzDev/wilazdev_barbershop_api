from typing import Dict,Annotated
from fastapi import APIRouter, Depends,status,Response
from fastapi.responses import JSONResponse
from fastapi_pagination import Page

from app.schemas import (
    RoleRead,
    RoleCreate,
    RoleUpdate,
    TokenData
)
from app.services import RoleService
from app.dependencies import get_role_service
from app.security import get_current_user

router = APIRouter(prefix="/roles",tags=["roles"])

@router.get(
    "/",
    response_model=Page[RoleRead],
    tags=["get_list"],
)
async def get_roles(
    current_user:Annotated[TokenData, Depends(get_current_user)],
    service: RoleService = Depends(get_role_service)
):
    return await service.list()

@router.get(
    "/{role_id}",
    response_model=RoleRead,
    tags=["get_by"]
)
async def get_role(
    current_user:Annotated[TokenData, Depends(get_current_user)],
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
    current_user:Annotated[TokenData, Depends(get_current_user)],
    role: RoleCreate,
    service: RoleService = Depends(get_role_service)
):
    return await service.create(role)

@router.put(
    "/{role_id}",
    response_model=RoleRead,
    tags=["update"]
)
async def update_role(
    current_user:Annotated[TokenData, Depends(get_current_user)],
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
    current_user:Annotated[TokenData, Depends(get_current_user)],
    role_id: int,
    service: RoleService = Depends(get_role_service)
):
    result = await service.delete(role_id)
    return Response(
        status_code=status.HTTP_200_OK,
        content=result['message']
    )