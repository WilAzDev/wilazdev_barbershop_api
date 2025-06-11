from typing import Optional
from pydantic import BaseModel,ConfigDict

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    name: Optional[str] = None
    
class RoleRead(RoleBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)