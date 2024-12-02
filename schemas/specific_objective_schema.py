from pydantic import BaseModel, Field

class SpecificObjectiveCreate(BaseModel):
    description: str = Field(..., description="Description of the specific objective")
    project_id: int = Field(..., description="ID of the project")

class SpecificObjectiveResponse(SpecificObjectiveCreate):
    id: int = Field(..., description="Unique identifier for the specific objective")