from pydantic import BaseModel, Field

class FeeValueCreate(BaseModel):
    managmentlevel: str = Field(..., min_length=1, max_length=255, description="Name of the managment level")
    category: str = Field(..., min_length=1, max_length=255, description="Name of the category")
    academicsuitability: str = Field(..., min_length=1, max_length=255, description="Name of the academic suitability")
    minimumexperience: int = Field(..., description="Minimum experience required")
    monthlyfee: float = Field(..., description="Monthly fee")
    monthlyfeewithtaxes: float = Field(..., description="Monthly fee without taxes")

class FeeValueResponse(FeeValueCreate):
    id: int = Field(..., description="Unique identifier for the fee value")