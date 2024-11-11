from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=255, description="Description of the project")

class ProjectResponse(ProjectCreate):
    id: int