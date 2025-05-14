from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: Mover a URL do banco para variáveis de ambiente e um arquivo de configuração
# Exemplo: DATABASE_URL = "postgresql://user:password@host:port/database"
DATABASE_URL = os.getenv("AUTH_DATABASE_URL", "postgresql://augeuser:augepass@localhost:5432/auge_auth_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # TODO: Adicionar campos como is_active, is_superuser, last_login, etc.

def create_db_and_tables():
    # Esta função deve ser chamada no lifespan do FastAPI para criar as tabelas se não existirem
    # Em um ambiente de produção, migrações com Alembic são mais apropriadas.
    Base.metadata.create_all(bind=engine)

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

