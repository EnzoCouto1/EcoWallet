from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app, get_db
from models import Base
import pytest


TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

#substitui o "get_db" original
# Em vez de conectar no Postgres, conecta no SQLite
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#   FastAPI troca o banco real pelo fake
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Zera o banco antes de CADA teste
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_criar_e_listar_transacao():
    
    payload = {
        "descricao": "Teste Simples",
        "valor": 50.0,
        "tipo": "receita"
    }
    response_post = client.post("/transacoes", json=payload)
    
    # Verifica se criou
    assert response_post.status_code == 200
    dados_post = response_post.json()
    assert dados_post["transacao"]["descricao"] == "Teste Simples"
    assert "id" in dados_post["transacao"]


    response_get = client.get("/transacoes")
    
    assert response_get.status_code == 200
    lista_transacoes = response_get.json()
    assert len(lista_transacoes) == 1
    assert lista_transacoes[0]["descricao"] == "Teste Simples"

def test_saldo_vazio():
    # Banco não tem nada.
    # O saldo deve ser 0.0, e não dar erro.
    response = client.get("/saldo")
    
    assert response.status_code == 200
    dados = response.json()
    assert dados["Saldo total: "] == 0.0

def test_fluxo_completo_saldo():
    # Adiciona Receita de 100
    client.post("/transacoes", json={"descricao": "Ganhei", "valor": 100, "tipo": "receita"})
    
    # Adiciona Despesa de 30
    client.post("/transacoes", json={"descricao": "Gastei", "valor": 30, "tipo": "despesa"})
    
    # Saldo
    response = client.get("/saldo")
    dados = response.json()
    
    assert dados["Saldo total: "] == 70.0