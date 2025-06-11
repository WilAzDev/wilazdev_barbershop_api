from typing import Optional,TYPE_CHECKING,List
from sqlmodel import SQLModel,Field,Relationship

from .role import Role,UserHasRole

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"nullable": False})
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False})
    is_active: bool = Field(sa_column_kwargs={"default": True})
    hashed_password: str = Field(sa_column_kwargs={"nullable": False})
    
    roles : List["Role"] = Relationship(back_populates="user",link_model=UserHasRole)