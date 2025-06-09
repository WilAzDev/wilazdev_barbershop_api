from typing import Dict
from fastapi import APIRouter, Depends,Response,status
from fastapi_pagination import Page

from app.schemas import (
    UserRead,
    UserCreate,
    UserUpdate,
)
from app.services import UserService
from app.dependencies import get_user_service

router = APIRouter(prefix="/users",tags=["users"])

@router.get(
    "/",
    response_model=Page[UserRead],
    tags=["get_list"]
)
async def list_users(service:UserService = Depends(get_user_service)):
    return await service.list()

@router.get(
    "/{user_id}",
    response_model=UserRead,
    tags=["get_by"]
)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return await service.get(user_id)

@router.get(
    "/email/{user_email}",
    response_model=UserRead,
    tags=["get_by"]
)
async def get_user_by_email(user_email: str, service: UserService = Depends(get_user_service)):
    return await service.get_by_email(user_email)

@router.post(
    "/",
    response_model=UserRead,
    tags=["create"]
)
async def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create(payload)

@router.put(
    "/{user_id}",
    response_model=UserRead,
    tags=["update"]
)
async def update_user(user_id: int, payload: UserUpdate, service: UserService = Depends(get_user_service)):
    return await service.update(user_id, payload)

@router.delete(
    "/{user_id}",
    response_model=Dict[str,str],
)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    result = await service.delete(user_id)
    return Response(
        status_code=status.HTTP_200_OK,
        content=result['message'],
    )

