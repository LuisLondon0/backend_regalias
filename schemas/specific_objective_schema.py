from pydantic import BaseModel, Field

class SpecificObjectiveCreate(BaseModel):
    general_objective_id: int
    description: str = Field(..., min_length=1, max_length=255, description="Description of the specific objective")

class SpecificObjectiveResponse(BaseModel):
    id: int
    general_objective_id: int
    description: str = Field(..., description="Description of the specific objective")