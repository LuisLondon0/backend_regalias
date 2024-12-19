from pydantic import BaseModel, Field


class TrainingEventSchema(BaseModel):
    entity: str = Field(..., description="Name of the entity")
    theme: str = Field(..., description="Theme of the event")
    justification: str = Field(..., description="Justification the event")
    quantity: int = Field(..., description="Quantity of the events")
    total: float = Field(..., description="Total value of the events")
    activity_id: int = Field(..., description="Unique identifier for the activity")


class TrainingEventResponse(TrainingEventSchema):
    id: int = Field(..., description="Unique identifier for the software")
