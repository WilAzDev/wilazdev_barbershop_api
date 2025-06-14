from typing import Optional,List
from pydantic import BaseModel,ConfigDict,Field

class PermissionBase(BaseModel):
    name:str
    description: Optional[str] = None
    
class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionCreate):
    name: Optional[str] = None

class PermissionRead(PermissionBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class PermissionSync(BaseModel):
    permissions_id: List[int] = Field(default_factory=list)