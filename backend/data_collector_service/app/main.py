from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers import market_data_router # Import the new market data router
from .db.market_data_db import create_market_data_tables # For initial table creation
from .services import data_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando Data Collector Service...")
    # Create market data tables if they don't exist. 
    # In production, Alembic migrations are preferred.
    create_market_data_tables()
    print("Banco de dados de mercado e tabelas verificados/criados.")
    
    data_scheduler.start() # Start the scheduler for data collection
    print("Agendador de coleta de dados iniciado.")
    yield
    data_scheduler.shutdown() # Shutdown the scheduler gracefully
    print("Agendador de coleta de dados parado.")
    print("Data Collector Service desligado.")

app = FastAPI(
    title="Auge Invest - Data Collector Service",
    description="Microsserviço responsável pela coleta, armazenamento e fornecimento de dados de mercado para a plataforma Auge Invest.",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/ping", tags=["Health Check"])
async def ping():
    return {"message": "Data Collector Service is running!"}

# Include the market data router
app.include_router(market_data_router.router, prefix="/market-data", tags=["Market Data"])

# To run locally (example):
# cd auge_invest_project/backend/data_collector_service
# uvicorn app.main:app --reload --port 8002

