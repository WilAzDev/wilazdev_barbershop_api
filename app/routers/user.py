from typing import Dict
from fastapi import APIRouter, Depends,status,Response
from fastapi_pagination import Page

from app.schemas import (
    UserRead,
    UserCreate,
    UserUpdate,
)
from app.services import UserService
from app.dependencies import get_user_service
from app.security import Auth

router = APIRouter(prefix="/users",tags=["users"])

@router.get(
    "/",
    response_model=Page[UserRead],
    tags=["get_list"],
)
async def list_users(
    auth:Auth,
    service:UserService = Depends(get_user_service)
):
    return await service.list()

@router.get(
    "/count",
    response_model=int,
    tags=["get_count"]
)
async def count_users(
    auth:Auth,
    service:UserService = Depends(get_user_service)
):
    return await service.count()

@router.get(
    "/{user_id}",
    response_model=UserRead,
    tags=["get_by"]
)
async def get_user(
    auth:Auth,
    user_id: int, 
    service: UserService = Depends(get_user_service)
):
    return await service.get(user_id)

@router.get(
    "/auth/me",
    response_model=UserRead,
    tags=['auth']
)
async def get_me(
    auth:Auth,
    service:UserService = Depends(get_user_service)
):
    return await service.get(auth.id)

@router.post(
    "/",
    response_model=UserRead,
    tags=["create"],
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    payload: UserCreate, 
    service: UserService = Depends(get_user_service)
):
    return await service.create(payload)

@router.put(
    "/{user_id}",
    response_model=UserRead,
    tags=["update"]
)
async def update_user(
    auth:Auth,
    user_id: int, 
    payload: UserUpdate, 
    service: UserService = Depends(get_user_service)
):
    return await service.update(user_id, payload)

@router.delete(
    "/{user_id}",
    response_model=Dict[str,str],
    tags=["delete"]
)
async def delete_user(
    auth:Auth,
    user_id: int, 
    service: UserService = Depends(get_user_service)
):
    result = await service.delete(user_id)
    return Response(
        status_code=status.HTTP_200_OK,
        content=result['message'],
    )

