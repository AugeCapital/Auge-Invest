from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from .services.bcb_service import BCBService
# TODO: Importar outros serviços de coleta (ex: B3, notícias)

# Inicializa o scheduler
scheduler = AsyncIOScheduler(timezone="America/Sao_Paulo")

def schedule_bcb_data_collection():
    """
    Agenda a coleta de dados do Banco Central do Brasil.
    """
    bcb_service = BCBService()
    
    # Agendar Selic Meta para rodar diariamente (ex: às 08:00)
    # A API do BCB para Selic meta pode não ser atualizada diariamente, ajustar conforme necessidade.
    scheduler.add_job(
        bcb_service.fetch_and_store_selic_meta, 
        CronTrigger(hour=8, minute=0, day_of_week='mon-fri'), 
        id="fetch_selic_meta", 
        name="Coleta Selic Meta BCB",
        replace_existing=True
    )
    
    # Agendar IPCA Mensal para rodar mensalmente (ex: dia 10 às 09:00)
    # O IPCA é divulgado em datas específicas, ajustar o agendamento.
    scheduler.add_job(
        bcb_service.fetch_and_store_ipca_mensal, 
        CronTrigger(day=10, hour=9, minute=0), 
        id="fetch_ipca_mensal", 
        name="Coleta IPCA Mensal BCB",
        replace_existing=True
    )
    
    # Agendar Dólar PTAX Venda para rodar diariamente (ex: às 18:00 após fechamento)
    scheduler.add_job(
        bcb_service.fetch_and_store_dolar_ptax, 
        CronTrigger(hour=18, minute=0, day_of_week='mon-fri'),
        id="fetch_dolar_ptax", 
        name="Coleta Dólar PTAX BCB",
        replace_existing=True
    )
    print("Tarefas de coleta de dados do BCB agendadas.")

# TODO: Adicionar funções para agendar coleta de outras fontes (B3, notícias, etc.)

def start():
    """
    Inicia o scheduler e as tarefas agendadas.
    """
    if not scheduler.running:
        schedule_bcb_data_collection()
        # Chamar outras funções de agendamento aqui
        scheduler.start()
        print(f"Scheduler iniciado. Próxima execução de tarefas agendadas: {scheduler.get_jobs()}")
    else:
        print("Scheduler já está em execução.")

def shutdown():
    """
    Para o scheduler de forma graciosa.
    """
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler parado.")

# Exemplo de como iniciar o scheduler (isso seria chamado no lifespan do FastAPI)
# if __name__ == "__main__":
#     start()
#     # Mantém o script rodando para o scheduler funcionar em background (se não for em um server FastAPI)
#     try:
#         while True:
#             pass
#     except (KeyboardInterrupt, SystemExit):
#         shutdown()

