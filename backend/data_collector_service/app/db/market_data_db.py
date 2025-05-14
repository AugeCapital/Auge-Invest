from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

from .market_data_models import Base # Import Base from your models file

load_dotenv()

# TODO: Mover a URL do banco para variáveis de ambiente e um arquivo de configuração centralizado ou específico do serviço
# Exemplo: MARKET_DATABASE_URL = "postgresql://user:password@host:port/market_data_db"
# Usaremos uma URL diferente da de autenticação, assumindo um banco de dados separado para dados de mercado.
MARKET_DATABASE_URL = os.getenv("MARKET_DATABASE_URL", "postgresql://augeuser:augepass@localhost:5432/auge_market_data_db")

engine = create_engine(MARKET_DATABASE_URL)
SessionLocalMarket = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_market_data_tables():
    """
    Cria as tabelas de dados de mercado no banco de dados se não existirem.
    Em um ambiente de produção, migrações com Alembic são mais apropriadas.
    """
    Base.metadata.create_all(bind=engine)

# Função para obter uma sessão do banco de dados de mercado
def get_market_db():
    db = SessionLocalMarket()
    try:
        yield db
    finally:
        db.close()

