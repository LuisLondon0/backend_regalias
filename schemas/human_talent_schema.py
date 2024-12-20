from pydantic import BaseModel, Field
from typing import Optional

class HumanTalentCreate(BaseModel):
    activityid: int = Field(..., description="Unique identifier for the activity")
    feevalueid: int = Field(..., description="Unique identifier for the fee value")
    entity: Optional[str] = Field(None, description="Name of the entity")
    position: str = Field(..., description="Name of the position")
    justification: str = Field(..., description="Justification for the talent")
    quantity: int = Field(..., description="Quantity of the talent")

class HumanTalentResponse(HumanTalentCreate):
    id: int = Field(..., description="Unique identifier for the human talent")