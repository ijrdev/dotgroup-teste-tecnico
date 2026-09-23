import logging, traceback, json

from typing import List
from http import HTTPStatus

from fastapi import Request, APIRouter, HTTPException, Body, Query
from starlette.responses import JSONResponse
from slowapi import Limiter

from application.messages.http_message import HttpMessage
from presentation.middlewares.rate_limit import RateLimit
from services.livros_service import LivrosService
from presentation.models.input.livros.create_in_model import CreateInModel
from presentation.models.input.livros.get_all_in_model import GetAllInModel
from presentation.models.output.livros.livros_out_model import LivrosOutModel
from presentation.models.output.message_model import MessageModel
from presentation.models.output.validation_model import ValidationModel
from presentation.responses.api_response import ApiResponse

limiter: Limiter = RateLimit().limiter

class LivrosController():
    router: APIRouter = APIRouter(
        prefix = "/livros",
        tags = ["Livros"],
        responses = {
            200: {
                "description": str(HttpMessage.OK.value)
            },
            400: {
                "description": str(HttpMessage.BAD_REQUEST.value),
                "model": MessageModel
            },
            401: {
                "description": str(HttpMessage.UNAUTHORIZED.value),
                "model": MessageModel
            },
            403: {
                "description": str(HttpMessage.FORBIDDEN.value),
                "model": MessageModel,
            },
            404: {
                "description": str(HttpMessage.NOT_FOUND.value),
                "model": MessageModel
            },
            405: {
                "description": str(HttpMessage.METHOD_NOT_ALLOWED.value),
                "model": MessageModel
            },
            422: {
                "description": str(HttpMessage.UNPROCESSABLE_ENTITY.value),
                "model": ValidationModel
            },
            429: {
                "description": str(HttpMessage.TOO_MANY_REQUESTS.value),
                "model": MessageModel
            },
            500: {
                "description": str(HttpMessage.INTERNAL_SERVER_ERROR.value),
                "model": MessageModel
            }
        }
    )
    
    @router.post(
        "/",
        response_model = LivrosOutModel,
        summary = "Cadastrar livro",
        description = (
            "Cadastra um novo livro na biblioteca. "
            "A data de publicação não pode ser futura, e os campos de título, "
            "autor e resumo possuem validações de tamanho e conteúdo."
        )
    )
    @limiter.limit("10/minute")
    async def create(request: Request, livros_in_model: CreateInModel = Body()) -> JSONResponse:
        """Recebe os dados obrigatórios e retorna o livro cadastrado."""
        
        status_code: int | None =  None
        error_message: str | None = None
        
        try:
            return ApiResponse.http_data(LivrosService().create(livros_in_model.model_dump()), HTTPStatus.CREATED)
        except HTTPException as http_ex:
            status_code = http_ex.status_code
            error_message = str(http_ex.detail)
            
            traceback.print_exc()
            logging.error(http_ex.detail)
            
            return ApiResponse.http_message(http_ex.detail, http_ex.status_code)
        except Exception as ex:
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            error_message = str(ex)
            
            traceback.print_exc()
            logging.error(ex)
            
            return ApiResponse.http_message(HttpMessage.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR)
        finally:
            if status_code and error_message:
                payload: str | None = None
                
                try:
                    payload = json.dumps(await request.json(), ensure_ascii = False)
                except:
                    try:
                        payload = (await request.body()).decode()
                        
                        payload = payload if payload else None
                    except:
                        payload = None
                
                # Local ideal para salvar logs.
    
    @router.get(
        "/",
        response_model = List[LivrosOutModel],
        summary = "Consultar livros",
        description = (
            "Consulta livros por título, autor ou pelos dois filtros combinados. "
            "É obrigatório informar pelo menos um filtro; a busca utiliza "
            "correspondência parcial e combina os filtros com AND."
        )
    )
    @limiter.limit("10/minute")
    async def get_all(request: Request, get_all_in_model: GetAllInModel = Query()) -> JSONResponse:
        """Retorna livros filtrados por título, autor ou ambos."""
        
        status_code: int | None =  None
        error_message: str | None = None
        
        try:
            return ApiResponse.http_data(LivrosService().get_all(get_all_in_model.model_dump()), HTTPStatus.OK)
        except HTTPException as http_ex:
            status_code = http_ex.status_code
            error_message = str(http_ex.detail)
            
            traceback.print_exc()
            logging.error(http_ex.detail)
            
            return ApiResponse.http_message(http_ex.detail, http_ex.status_code)
        except Exception as ex:
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            error_message = str(ex)
            
            traceback.print_exc()
            logging.error(ex)
            
            return ApiResponse.http_message(HttpMessage.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR)
        finally:
            if status_code and error_message:
                payload: str | None = None
                
                try:
                    payload = json.dumps(await request.json(), ensure_ascii = False)
                except:
                    try:
                        payload = (await request.body()).decode()
                        
                        payload = payload if payload else None
                    except:
                        payload = None
                
                # Local ideal para salvar logs.
