from pydantic import BaseModel, Field

class StudentPredictionInput(BaseModel):
    hours_studied: float = Field(ge=0, le=24)
    attendance : float = Field(ge=0,le=100)
    previous_score : float =Field(ge=0,le=100)


class StudentPredictionOutput(BaseModel):
    predicted_score : float