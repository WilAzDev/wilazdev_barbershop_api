from typing import Optional,List
from pydantic import BaseModel,ConfigDict,Field

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
    
class RoleSync(BaseModel):
    roles_id: List[int] = Field(default_factory=list)