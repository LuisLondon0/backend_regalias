from pydantic import BaseModel, Field

class RoleCreate(BaseModel):
    description: str = Field(..., description="Description of the role")

class RoleResponse(RoleCreate):
    id: int = Field(..., description="Unique identifier of the role")