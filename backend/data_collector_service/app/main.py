from fastapi import FastAPI
from contextlib import asynccontextmanager

# from .routers import collector_router # No direct endpoints for now
from .db.database import create_market_data_tables # Placeholder, to be created
from .services import data_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando Data Collector Service...")
    # create_market_data_tables() # TODO: Implement this function and a proper DB setup for market data
    # print("Banco de dados de mercado e tabelas verificados/criados.")
    
    data_scheduler.start() # Start the scheduler
    print("Agendador de coleta de dados iniciado.")
    yield
    data_scheduler.shutdown() # Shutdown the scheduler gracefully
    print("Agendador de coleta de dados parado.")
    print("Data Collector Service desligado.")

app = FastAPI(
    title="Auge Invest - Data Collector Service",
    description="Microsserviço responsável pela coleta e armazenamento de dados de mercado para a plataforma Auge Invest.",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/ping", tags=["Health Check"])
async def ping():
    return {"message": "Data Collector Service is running!"}

# No direct routers for now, service runs scheduled tasks.

# To run locally (example, if it had endpoints or for testing scheduler):
# cd auge_invest_project/backend/data_collector_service
# uvicorn app.main:app --reload --port 8002

