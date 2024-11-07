from pydantic import BaseModel, model_validator, Field
from pydantic import PositiveFloat
from datetime import datetime


class RequestModel(BaseModel):
    date: datetime = Field(default=datetime.now())
    operating_mode_from: float = Field(ge=0, lt=24, default=9.0)
    operating_mode_to: float = Field(ge=0, lt=24, default=18.0)
    sla_time: PositiveFloat

    @model_validator(mode='before')
    def check_model(cls, values):
        if values.get('operating_mode_from') >= values.get('operating_mode_to'):
            raise ValueError("'To' value must be greater than 'From' value")
        return values


class ResponseModel(BaseModel):
    deadline: datetime
