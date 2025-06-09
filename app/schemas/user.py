from typing import Optional
from pydantic import BaseModel, EmailStr, Field,ConfigDict,model_validator

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(...,min_length=2,max_length=40)
    
class UserCreate(UserBase):
    password: str = Field(...,min_length=8,max_length=64)
    password2: str = Field(...,min_length=8,max_length=64)

class UserUpdate(UserCreate):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    password2: Optional[str] = None
    
class UserAuth(BaseModel):
    email: EmailStr
    password: str

class UserInDb(BaseModel):
    id: int
    password_hash: str

class UserRead(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)