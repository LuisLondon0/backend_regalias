from pydantic import BaseModel, Field

class RoleCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=255, description="Description of the role")

class RoleResponse(RoleCreate):
    id: int = Field(..., description="Unique identifier of the role")