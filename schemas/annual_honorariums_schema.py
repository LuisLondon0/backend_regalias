from pydantic import BaseModel, Field

class AnnualHonorariumsSchema(BaseModel):
    talentid: int = Field(..., description="Unique identifier for the talent")
    honorariumamount: float = Field(..., description="Amount of the honorarium")
    hourvalue: str = Field(..., description="Hourly value of the honorarium")
    year: int = Field(..., description="Year of the honorarium")
    weekofyears: int = Field(..., description="Week of the year of the honorarium")
    totalamount: float = Field(..., description="Total amount of the honorarium")

class AnnualHonorariumsResponse(AnnualHonorariumsSchema):
    id: int = Field(..., description="Unique identifier for the honorarium")