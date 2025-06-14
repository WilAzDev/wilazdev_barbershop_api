from typing import Optional,TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    
class UserHasRole(SQLModel,table=True):
    user_id: int = Field(foreign_key="user.id",primary_key=True,ondelete='CASCADE')
    role_id: int = Field(foreign_key="role.id",primary_key=True,ondelete='CASCADE')

class Role(SQLModel,table=True):
    id:Optional[int] = Field(default=None,primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": True})
    description: str = Field(sa_column_kwargs={"nullable": True})
    
    users: list["User"] = Relationship(back_populates="roles",link_model=UserHasRole,cascade_delete=True)