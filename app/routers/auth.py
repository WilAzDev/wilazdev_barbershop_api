from typing import Annotated
from fastapi import (
    APIRouter,
    Depends
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from app.schemas import Token,UserAuth,UserInDb
from app.services import UserService,AuthService
from app.dependencies import get_user_service
from app.models import User

router = APIRouter(prefix='/auth',tags=['auth'])

@router.post(
    "/login",
    tags=['login'],
    response_model=Token,
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserService = Depends(get_user_service),
):
    
    try:
        user:UserInDb = await service.authenticate_user(UserAuth(email=form_data.username,password=form_data.password))
        access_token = AuthService().create_access_token({
            'id':user.id,
            'sub':user.email
        })

        return Token(access_token=access_token,token_type='bearer')
    except Exception as e:
        return JSONResponse(content={'error':str(e)},status_code=401)