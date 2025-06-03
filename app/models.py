from typing import Optional
from sqlmodel import SQLModel,Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"nullable": False})
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False})
    hashed_password: str = Field(sa_column_kwargs={"nullable": False})