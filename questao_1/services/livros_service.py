from http import HTTPStatus
from typing import List

from fastapi import HTTPException

from infrastructure.repositories.livros_repository import LivrosRepository

class LivrosService():
    def __init__(self) -> None:
        self.livros_repository: LivrosRepository = LivrosRepository()

    def create(self, data: dict) -> dict:
        try:
            return dict(self.livros_repository.create(data))
        except Exception as ex:
            raise
    
    def get_all(self, data: dict) -> List[dict]:
        try:
            filters: dict = {key: value for key, value in data.items() if value}
            
            if not filters:
                raise HTTPException(HTTPStatus.BAD_REQUEST, "Nenhum filtro informado para realizar a consulta.")
            
            return [dict(row) for row in self.livros_repository.get_all(filters)]
        except Exception as ex:
            raise
