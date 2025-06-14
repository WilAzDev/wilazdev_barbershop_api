from typing import Optional,TYPE_CHECKING,List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .role import Role
    from .user import User
    
class RoleHasPermission(SQLModel,table=True):
    __tablename__ = "role_has_permission"
    role_id: int = Field(foreign_key="role.id", primary_key=True,ondelete='CASCADE')
    permission_id: int = Field(foreign_key="permission.id",primary_key=True,ondelete='CASCADE')

class UserHasPermission(SQLModel,table=True):
    __tablename__ = "user_has_permission"
    user_id: int = Field(foreign_key="user.id",primary_key=True,ondelete='CASCADE')
    permission_id: int = Field(foreign_key="permission.id",primary_key=True,ondelete='CASCADE')
    
class Permission(SQLModel,table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": True})
    description: str = Field(sa_column_kwargs={"nullable": True})
    
    users: List['User'] = Relationship(back_populates="permissions",link_model=UserHasPermission)
    roles: List['Role'] = Relationship(back_populates="permissions",link_model=RoleHasPermission)