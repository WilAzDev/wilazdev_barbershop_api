import jwt
from datetime import datetime,timedelta,timezone
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi import status,HTTPException

from app.conf import get_settings
from app.schemas import TokenData

class AuthService:
    def __init__(self):
        self.settings = get_settings()
        self.pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")
        
    def verify_password(self, plain_password:str, hashed_password:str):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password:str):
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data:dict, expires_delta:timedelta=None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.settings.access_token_expire_minutes)
        to_encode.update({"exp":expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            self.settings.secret_key, 
            algorithm=self.settings.algorithm
        )
        return encoded_jwt
    
    def decode_access_token(self,token:str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error validating credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.settings.secret_key, algorithms=[self.settings.algorithm])
            email: str = payload.get("sub")
            id = payload.get("id")
            if not email:
                raise credentials_exception
            token_data = TokenData(email=email,id=id)
        except InvalidTokenError:
            raise credentials_exception
        
        return token_data
    