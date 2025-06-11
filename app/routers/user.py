from typing import Dict,Annotated
from fastapi import APIRouter, Depends,status,Response
from fastapi.responses import JSONResponse
from fastapi_pagination import Page

from app.schemas import (
    UserRead,
    UserCreate,
    UserUpdate,
    TokenData
)
from app.services import UserService
from app.dependencies import get_user_service
from app.security import get_current_user

router = APIRouter(prefix="/users",tags=["users"])

@router.get(
    "/",
    response_model=Page[UserRead],
    tags=["get_list"]
)
async def list_users(
    current_user:Annotated[TokenData,Depends(get_current_user)],
    service:UserService = Depends(get_user_service)
):
    return await service.list()

@router.get(
    "/{user_id}",
    response_model=UserRead,
    tags=["get_by"]
)
async def get_user(
    current_user:Annotated[TokenData,Depends(get_current_user)],
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
    current_user:Annotated[TokenData,Depends(get_current_user)],
    service:UserService = Depends(get_user_service)
):
    try:
        return await service.get(current_user.id)
    except Exception as e:
        return JSONResponse(content={"error":str(e)},status_code=status.HTTP_404_NOT_FOUND)

@router.post(
    "/",
    response_model=UserRead,
    tags=["create"],
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    payload: UserCreate, 
    service: UserService = Depends(get_user_service)):
    try:
        return await service.create(payload)
    except Exception as e:
        return JSONResponse(content={"error": str(e)},status_code=status.HTTP_400_BAD_REQUEST)

@router.put(
    "/{user_id}",
    response_model=UserRead,
    tags=["update"]
)
async def update_user(
    current_user:Annotated[TokenData,Depends(get_current_user)],
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
    current_user:Annotated[TokenData,Depends(get_current_user)],
    user_id: int, 
    service: UserService = Depends(get_user_service)
):
    result = await service.delete(user_id)
    return Response(
        status_code=status.HTTP_200_OK,
        content=result['message'],
    )

