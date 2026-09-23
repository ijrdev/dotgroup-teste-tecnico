from typing import Any

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

class ApiResponse():
    @classmethod
    def http_message(cls, message: str, status_code: int) -> JSONResponse:
        try:
            return JSONResponse(jsonable_encoder({ "message": message }), status_code = status_code)
        except Exception as ex:
            raise
    
    @classmethod
    def http_data(cls, payload: Any, status_code: int) -> JSONResponse:
        try:
            return JSONResponse(jsonable_encoder(payload), status_code = status_code)
        except Exception as ex:
            raise
    
    @classmethod
    def http_erros(cls, erros: list, status_code: int) -> JSONResponse:
        try:
            return JSONResponse(jsonable_encoder({ "erros": erros }), status_code = status_code)
        except Exception as ex:
            raise

