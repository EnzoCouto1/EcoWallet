import models
from sqlalchemy.orm import Session
from sqlalchemy import func


def calcular_receitas(db: Session):
    Saldo_receita = db.query(func.sum(models.TransacaoDB.valor)).filter(models.TransacaoDB.tipo == "receita").scalar()
    return Saldo_receita or 0.0


def calcular_despesas(db: Session):
    Saldo_despesa = db.query(func.sum(models.TransacaoDB.valor)).filter(models.TransacaoDB.tipo == "despesa").scalar()
    return Saldo_despesa or 0.0

def calcular_saldo(db: Session):
    receitas = calcular_receitas(db)
    despesas = calcular_despesas(db)
    saldo = receitas - despesas
    return saldo