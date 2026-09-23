import uvicorn, logging, sys, warnings, traceback, json

from http import HTTPStatus
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from application.messages.http_message import HttpMessage
from presentation.controllers.livros_controller import LivrosController
from presentation.responses.api_response import ApiResponse
from presentation.middlewares.rate_limit import RateLimit
from infrastructure.globals.general_global import GeneralGlobal

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa os recursos globais da aplicação durante seu ciclo de vida."""
    
    try:
        logging.info("Carregando informações globais...")
        
        GeneralGlobal()
        
        logging.info("Informações globais carregadas com sucesso!")

        yield
    except Exception as ex: 
        traceback.print_exc()
        logging.error(ex)
        
        exit(0)

app: FastAPI = FastAPI(
    lifespan = lifespan,
    openapi_url = "/openapi.json",
    docs_url = "/documentacao",
    redoc_url = None,
    title = "Biblioteca Virtual",
    description = "API para cadastro e consulta de livros.",
    version = "1.0.0",
    separate_input_output_schemas = True,
    swagger_ui_parameters = {"defaultModelsExpandDepth": -1}
)

app.state.limiter = RateLimit().limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(CORSMiddleware, allow_origins = ["*"], allow_methods = ["*"], allow_headers = ["*"], expose_headers = ["*"], allow_credentials = True)
app.add_middleware(GZipMiddleware) 
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RequestValidationError)
async def request_validation_error_exception_handler(request: Request, requestValidationError: RequestValidationError) -> JSONResponse:
    """Trata erros de validação com uso do pydantic das requisições."""
    
    try:
        if requestValidationError:
            messages: dict = {
                "missing": "tem que existir.",
                "string_too_short": "contém o tamanho menor do que o permitido.",
                "string_too_long": "contém o tamanho maior do que o permitido.",
                "too_short": "possui a quantidade dos itens menor do que a permitida.",
                "too_long": "possui a quantidade dos itens maior do que a permitida",
                "string_type": "deve ser do tipo string.",
                "string_parsing": "deve ser do tipo string.",
                "bool_type": "deve ser do tipo bool.",
                "bool_parsing": "deve ser do tipo bool.",
                "list_type": "deve ser do tipo array.",
                "list_parsing": "deve ser do tipo array.",
                "int_type": "deve ser do tipo inteiro.",
                "int_parsing": "deve ser do tipo inteiro.",
                "float_type": "deve ser do tipo flutuante.",
                "float_parsing": "deve ser do tipo flutuante.",
                "dict_type": "deve ser do tipo objeto/dicionário.",
                "less_than_equal": "deve ser menor ou igual ao valor padrão.",
                "greater_than_equal": "deve ser maior ou igual ao valor padrão.",
                "value_error": "possui o valor inválido.",
                "literal_error": "deve ser um dos valores permitidos.",
                "json_invalid": "possui um corpo JSON inválido.",
                "greater_than": "deve ser maior ou igual ao valor padrão.",
                "date_from_datetime_inexact": "possui o valor inválido.",
                "date_from_datetime_parsing": "possui o valor inválido.",
            }
            
            erros: list = []
            
            for error in requestValidationError.errors():
                if len(error["loc"]) == 2:
                    erros.append(f"{error['loc'][1]} {messages[error['type']]}")
                elif len(error["loc"]) == 3: 
                    erros.append(f"{error['loc'][2]} {messages[error['type']]}")
                else:
                    erros.append(f"{error['loc'][0]} {messages[error['type']]}")
            
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
            
            return ApiResponse.http_erros(erros, HTTPStatus.UNPROCESSABLE_ENTITY)
    except Exception as ex:
        traceback.print_exc()
        
        return ApiResponse.http_message(HttpMessage.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_exception_handler(request: Request, rate_limit_exceeded: RateLimitExceeded):
    """Trata requisições que excederam o limite de acesso configurado."""
    
    try:
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
        
        return ApiResponse.http_message(HttpMessage.TOO_MANY_REQUESTS.value, HTTPStatus.TOO_MANY_REQUESTS)
    except Exception as ex:
        traceback.print_exc()
        
        return ApiResponse.http_message(HttpMessage.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR)

@app.exception_handler(StarletteHTTPException)
async def scarlette_http_exception_handler(request: Request, starlette_ex: StarletteHTTPException) -> JSONResponse:
    """Trata exceções HTTP do Starlette."""
    
    try:
        description: str | None = None
        
        if starlette_ex.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            description = HttpMessage.METHOD_NOT_ALLOWED.value
        elif starlette_ex.status_code == HTTPStatus.UNAUTHORIZED:
            description = HttpMessage.UNAUTHORIZED.value
        elif starlette_ex.status_code == HTTPStatus.FORBIDDEN:
            description = HttpMessage.FORBIDDEN.value
        elif starlette_ex.status_code == HTTPStatus.NOT_FOUND:
            description = HttpMessage.NOT_FOUND.value
        else:
            description = starlette_ex.detail
        
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
        
        return ApiResponse.http_message(description, starlette_ex.status_code)
    except Exception as ex:
        traceback.print_exc()
        
        return ApiResponse.http_message(HttpMessage.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, http_ex: HTTPException) -> JSONResponse:
    """Trata exceções HTTP do FastAPI."""
    
    try:
        description: str | None = None
        
        if http_ex.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
            description = HttpMessage.METHOD_NOT_ALLOWED.value
        elif http_ex.status_code == HTTPStatus.UNAUTHORIZED:
            description = HttpMessage.UNAUTHORIZED.value
        elif http_ex.status_code == HTTPStatus.FORBIDDEN:
            description = HttpMessage.FORBIDDEN.value
        elif http_ex.status_code == HTTPStatus.NOT_FOUND:
            description = HttpMessage.NOT_FOUND.value
        else:
            description = http_ex.detail
        
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
        
        return ApiResponse.http_message(description, http_ex.status_code)
    except Exception as ex:
        traceback.print_exc()
        
        return ApiResponse.http_message(HttpMessage.INTERNAL_SERVER_ERROR.value, HTTPStatus.INTERNAL_SERVER_ERROR)

app.include_router(LivrosController.router)

if __name__ == "__main__":
    try:
        warnings.filterwarnings('ignore')
        
        logging.basicConfig(
            stream = sys.stdout, 
            level = logging.INFO, 
            encoding = "utf-8", 
            datefmt = "%d/%m/%Y %H:%M:%S", 
            format = "%(asctime)s - %(levelname)s - %(message)s"
        )
        
        uvicorn.run(app, host = '0.0.0.0', port = 8000, http = 'auto', proxy_headers = True)
    except Exception as ex:
        traceback.print_exc()
        
        exit(0)
