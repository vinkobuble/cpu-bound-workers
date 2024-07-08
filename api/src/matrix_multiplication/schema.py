from typing import List

from pydantic import BaseModel, field_validator, Field
from pydantic_core.core_schema import ValidationInfo


class Matrix(BaseModel):
    data: List[List[float]] = Field(min_length=1)

    @field_validator('data', mode='after')
    @classmethod
    def validate_data_size(cls, data: List[List[float]], info: ValidationInfo) -> List[List[float]]:
        if len(data) == 0:
            raise ValueError("data cannot be empty.")
        n = len(data[0])
        for row in data:
            if len(row) != n:
                raise ValueError("All rows have to be of the same size.")
        return data


class MultiplyMatricesRequestBody(BaseModel):
    a: Matrix
    b: Matrix
