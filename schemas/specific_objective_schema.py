from pydantic import BaseModel, Field

class SpecificObjectiveCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=255, description="Description of the specific objective")
    project_id: int = Field(..., description="ID of the project")

class SpecificObjectiveResponse(SpecificObjectiveCreate):
    id: int = Field(..., description="Unique identifier for the specific objective")