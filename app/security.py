from typing import Annotated
from fastapi import Depends, status,HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.services import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    current_user = AuthService().decode_access_token(token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return current_user