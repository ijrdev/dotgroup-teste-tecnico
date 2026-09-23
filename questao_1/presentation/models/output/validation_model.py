from typing import List

from pydantic import BaseModel, Field

class ValidationModel(BaseModel):
    erros: List[str] = Field([""])