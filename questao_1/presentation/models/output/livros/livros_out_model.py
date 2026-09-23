from pydantic import BaseModel, Field

class LivrosOutModel(BaseModel):
    id: int = Field(0)
    data_cadastro: str = Field("")
    data_publicacao: str = Field("")
    titulo: str = Field("")
    autor: str = Field("")
    resumo: str = Field("")
