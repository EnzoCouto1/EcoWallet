import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não foi encontrada no arquivo .env!")

# 2. O Motor (Engine)
# É ele que abre a conexão física com o banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. A Sessão (SessionLocal)
# É a "mesa de trabalho" temporária para cada requisição
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Todas as tabelas vão herdar dessa classe para o Python saber que são tabelas
Base = declarative_base()