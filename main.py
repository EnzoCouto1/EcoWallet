from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Generator, Optional
from enum import Enum
from datetime import datetime
import models
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import services


# MÁGICA: Isso vai no banco e cria as tabelas definidas no models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="EcoWallet API")



# Criamos um "Enum" para obrigar que o tipo seja apenas um desses dois.
class TipoTransacao(str, Enum):
    receita = "receita"
    despesa = "despesa"

class Transacao(BaseModel):
    id: Optional[int] = None  # O ID será gerado automaticamente pelo banco independente do que o usuário envie
    descricao: str            # Ex: "Almoço", "Salário"
    valor: float              # Ex: 30.50
    tipo: TipoTransacao       # Ex: "despesa"
    data: Optional[str] = None # Se não mandar, pegamos a data de hoje


def get_db():  
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"mensagem": "EcoWallet API rodando!", "doc": "Acesse /docs para testar"}

@app.post("/transacoes")
def criar_transacao(nova_transacao: Transacao, db: Session = Depends(get_db)):
    

    db_transacao = models.TransacaoDB(
        descricao=nova_transacao.descricao,
        valor=nova_transacao.valor,
        tipo=nova_transacao.tipo,
        data=nova_transacao.data or datetime.now().isoformat()
    )
    db.add(db_transacao)
    db.commit()
    db.refresh(db_transacao)


    
    return {
        "status": "sucesso", 
        "mensagem": "Transação registrada", 
        "transacao": db_transacao
    }

@app.get("/transacoes")
def listar_transacoes(db: Session = Depends(get_db)):
    return db.query(models.TransacaoDB).all()



@app.get("/saldo")
def calcular_saldo(db: Session = Depends(get_db)):
    saldo = services.calcular_saldo(db)
    return {"Saldo total: ": saldo}



@app.delete("/transacoes/{transacao_id}")
def deletar_transacao(transacao_id: int, db: Session = Depends(get_db)):

    transacao = db.query(models.TransacaoDB).filter(models.TransacaoDB.id == transacao_id).first()

    if transacao:
        db.delete(transacao)
        db.commit()
        return {"status": "sucesso", "mensagem": f"Transação {transacao_id} removida."}
        
    raise HTTPException(status_code=404, detail="Transação não encontrada.")



@app.put("/transacoes/{transacao_id}")
def atualizar_transacao(transacao_id: int, transacao_atualizada: Transacao, db: Session = Depends(get_db)):
    transacao = db.query(models.TransacaoDB).filter(models.TransacaoDB.id == transacao_id).first()
    if transacao:
        transacao.descricao = transacao_atualizada.descricao
        transacao.valor = transacao_atualizada.valor
        transacao.tipo = transacao_atualizada.tipo
        transacao.data = transacao_atualizada.data
        db.add(transacao)
        db.commit()
        db.refresh(transacao)
        return {"status": "sucesso", "mensagem": f"Transação {transacao_id} atualizada.", "transacao": transacao}
    raise HTTPException(status_code=404, detail="Transação não encontrada.")
