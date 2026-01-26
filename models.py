from sqlalchemy import Column, Integer, String, Float
from database import Base

class TransacaoDB(Base):
    __tablename__ = "transacoes"  # Nome da tabela no Postgres

    # Aqui definimos as colunas
    id = Column(Integer, primary_key=True, index=True) 
    descricao = Column(String)                         
    valor = Column(Float)                              
    tipo = Column(String)                              
    data = Column(String)                              