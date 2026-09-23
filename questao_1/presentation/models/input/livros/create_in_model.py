import re

from datetime import date

from pydantic import BaseModel, Field, field_validator

class CreateInModel(BaseModel):
    data_publicacao: date = Field(..., ge = date(1, 1, 1), le = date.today(), title = 'Data Publicação', description = 'Data Publicação.')
    titulo: str = Field(..., min_length = 2, max_length = 200, title = 'Título', description = 'Título.')
    autor: str = Field(..., min_length = 3, max_length = 100, title = 'Autor', description = 'Autor.')
    resumo: str = Field(..., min_length = 1, max_length = 1000, title = 'Resumo', description = 'Resumo.')

    @field_validator("titulo", "autor", "resumo", mode = "before")
    @classmethod
    def clean_value_validator(cls, valor: str) -> str:
        try:
            return re.sub(r"\s+", " ", valor).strip()
        except Exception as ex:
            raise
        