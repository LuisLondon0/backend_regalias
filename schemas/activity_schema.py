from typing import Optional
from pydantic import BaseModel, Field

class ActivityCreate(BaseModel):
    specific_objective_id: int = Field(..., description="ID of the specific objective")
    description: str = Field(..., min_length=1, max_length=500, description="Description of the activity")
    product: Optional[str] = Field(None, min_length=0, max_length=255, description="Result that will be obtained by carrying out the activity (if applicable)")
    verification_method: Optional[str] = Field(None, min_length=0, max_length=255, description="The way in which compliance with the activity will be verified (if applicable)")
    product_indicator: Optional[str] = Field(None, min_length=0, max_length=255, description="Quantity of products (if applicable)")

class ActivityResponse(ActivityCreate):
    id: int = Field(..., description="Unique identifier for the activity")