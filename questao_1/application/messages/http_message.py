from enum import Enum

class HttpMessage(Enum):
    OK = 'Operação realizada com sucesso!'
    CREATED = 'Recurso criado com sucesso!'
    BAD_REQUEST = 'Não foi possível realizar a operação.'
    UNAUTHORIZED = 'Autenticação inválida.'
    FORBIDDEN = 'Acesso ao recurso negado.'
    NOT_FOUND = 'Recurso não encontrado.'
    METHOD_NOT_ALLOWED = 'Solicitação não permitida.'
    UNPROCESSABLE_ENTITY = 'Dados da solicitação possuem erros de validação.'
    INTERNAL_SERVER_ERROR = 'Algo inesperado aconteceu, tente novamente.'
    TOO_MANY_REQUESTS = "Limite de requisições excedidas, tente novamente em instantes."
