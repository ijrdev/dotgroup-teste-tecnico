import re

from pydantic import BaseModel, Field, field_validator

class GetAllInModel(BaseModel):
    titulo: str | None = Field(None, min_length = 2, max_length = 200, title = 'Título', description = 'Título.')
    autor: str | None = Field(None, min_length = 3, max_length = 100, title = 'Autor', description = 'Autor.')

    @field_validator("titulo", "autor", mode = "before")
    @classmethod
    def clean_value_validator(cls, valor: str | None) -> str | None:
        try:
            if valor:
                return re.sub(r"\s+", " ", valor).strip()
            
            return None
        except Exception as ex:
            raise
        