import sys, pytest

from http import HTTPStatus
from datetime import date

from fastapi.testclient import TestClient

sys.path.insert(0, "questao_1")

from app import app
from services.livros_service import LivrosService

@pytest.fixture
def client():
    try:
        return TestClient(app)
    except Exception as ex:
        raise

def test_criar_livro_retorna_livro_criado(client, monkeypatch):
    livro_criado = {
        "id": 1,
        "data_cadastro": "2026-09-22T10:00:00",
        "data_publicacao": "2020-01-01",
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "resumo": "Boas praticas para desenvolvimento de software.",
    }

    monkeypatch.setattr(LivrosService, "create", lambda self, data: livro_criado)

    response = client.post(
        "/livros/",
        json = {
            "data_publicacao": "2020-01-01",
            "titulo": "Clean Code",
            "autor": "Robert C. Martin",
            "resumo": "Boas praticas para desenvolvimento de software.",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == livro_criado

def test_criar_livro_retorna_422_quando_payload_e_invalido(client):
    response = client.post(
        "/livros/",
        json = {
            "data_publicacao": "2020-01-01",
            "titulo": "A",
            "autor": "AB",
            "resumo": "Resumo valido",
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
    assert "erros" in response.json()

def test_consultar_livros_retorna_resultados_filtrados(client, monkeypatch):
    livros = [
        {
            "id": 1,
            "data_cadastro": "2026-09-22T10:00:00",
            "data_publicacao": date(2020, 1, 1),
            "titulo": "Clean Code",
            "autor": "Robert C. Martin",
            "resumo": "Boas praticas.",
        }
    ]

    monkeypatch.setattr(LivrosService, "get_all", lambda self, data: livros)

    response = client.get("/livros/?titulo=Clean")

    assert response.status_code == HTTPStatus.OK
    assert response.json()[0]["titulo"] == "Clean Code"

def test_consultar_livros_retorna_400_sem_filtro(client):
    response = client.get("/livros/")

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"message": "Nenhum filtro informado para realizar a consulta."}
