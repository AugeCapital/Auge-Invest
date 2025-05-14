from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from .routers import auth_router, user_router # Importando os routers
from .db.database import create_db_and_tables, engine # Importando a função de criação de tabelas
from .utils import security # Para o oauth2_scheme

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando Auth Service...")
    # Cria as tabelas no banco de dados se não existirem.
    # Em um ambiente de produção, Alembic seria mais apropriado para migrações.
    create_db_and_tables()
    print("Banco de dados e tabelas verificados/criados.")
    yield
    print("Auth Service desligado.")

app = FastAPI(
    title="Auge Invest - Auth Service",
    description="Microsserviço para autenticação e gerenciamento de usuários da plataforma Auge Invest.",
    version="0.1.0",
    lifespan=lifespan
)

# Adicionando o OAuth2PasswordBearer scheme para ser usado nas dependências de segurança
security.oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="/auth/login/access-token")


@app.get("/ping", tags=["Health Check"])
async def ping():
    return {"message": "Auth Service is running!"}

# Incluindo os routers da aplicação
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])

# Para executar localmente (exemplo):
# cd auge_invest_project/backend/auth_service
# uvicorn app.main:app --reload --port 8001

