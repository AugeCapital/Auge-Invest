import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from ..db.market_data_db import get_market_db, SessionLocalMarket # Import session and db getter
from ..models.market_data_models import TimeSeriesData # Import the model

# TODO: Mover para um arquivo de configuração ou variáveis de ambiente
BCB_API_BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados"

SERIES_CODES = {
    "selic_meta": 432,
    "selic_diaria": 11,
    "ipca_mensal": 433,
    "dolar_venda_ptax": 1,
}

class BCBService:
    def __init__(self):
        load_dotenv()
        pass

    def _save_time_series_data(self, db: Session, serie_name: str, data: list, source: str = "BCB_SGS"):
        """
        Salva ou atualiza os dados da série temporal no banco de dados.
        """
        saved_count = 0
        for item in data:
            try:
                # A API do BCB retorna data no formato DD/MM/YYYY
                # O valor pode ser string, precisa converter para float
                record_date_str = item.get("data")
                record_value_str = item.get("valor")

                if record_date_str is None or record_value_str is None:
                    print(f"Registro inválido para {serie_name} em {record_date_str}, faltando data ou valor.")
                    continue
                
                record_date = datetime.strptime(record_date_str, "%d/%m/%Y").date()
                record_value = float(record_value_str)

                # Verifica se o registro já existe para evitar duplicatas (UniqueConstraint fará isso no DB tbm)
                existing_record = db.query(TimeSeriesData).filter_by(serie_name=serie_name, date=record_date).first()
                
                if existing_record:
                    if existing_record.value != record_value: # Atualiza se o valor mudou
                        existing_record.value = record_value
                        existing_record.updated_at = datetime.now(datetime.timezone.utc)
                        # print(f"Atualizando {serie_name} para {record_date}: {record_value}")
                    # else: # Não faz nada se o valor for o mesmo
                        # print(f"Registro para {serie_name} em {record_date} já existe e é igual.")
                else:
                    db_record = TimeSeriesData(
                        serie_name=serie_name,
                        date=record_date,
                        value=record_value,
                        source=source
                    )
                    db.add(db_record)
                    # print(f"Adicionando {serie_name} para {record_date}: {record_value}")
                saved_count +=1
            except ValueError as e:
                print(f"Erro ao processar registro para {serie_name}: {item}. Erro: {e}")
                continue # Pula para o próximo item em caso de erro de conversão
            except Exception as e:
                print(f"Erro inesperado ao salvar registro {item} para {serie_name}: {e}")
                db.rollback() # Importante reverter em caso de erro na transação
                continue
        
        try:
            db.commit()
            if saved_count > 0:
                 print(f"{saved_count} registros processados/salvos para {serie_name}.")
        except Exception as e:
            db.rollback()
            print(f"Erro ao commitar transações para {serie_name}: {e}")

    def get_serie_data(self, serie_name: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Optional[list]:
        if serie_name not in SERIES_CODES:
            print(f"Erro: Código da série {serie_name} não encontrado.")
            return None

        codigo_serie = SERIES_CODES[serie_name]
        url = f"{BCB_API_BASE_URL.format(codigo_serie=codigo_serie)}?formato=json"
        params = {}

        if not start_date and not end_date:
            end_dt_obj = datetime.now()
            # Por padrão, busca os últimos 7 dias para atualizações diárias, ou mais para backfill inicial
            # Para séries mensais como IPCA, buscar um período maior pode ser necessário se não rodar todo dia
            if serie_name == "ipca_mensal":
                 start_dt_obj = end_dt_obj - timedelta(days=90) # Ex: últimos 3 meses para IPCA
            elif serie_name == "selic_meta":
                 start_dt_obj = end_dt_obj - timedelta(days=365) # Ex: último ano para Selic Meta
            else:
                 start_dt_obj = end_dt_obj - timedelta(days=7)
            params["dataInicial"] = start_dt_obj.strftime("%d/%m/%Y")
            params["dataFinal"] = end_dt_obj.strftime("%d/%m/%Y")
        else:
            if start_date: params["dataInicial"] = start_date
            if end_date: params["dataFinal"] = end_date
        
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar dados da série {serie_name} do BCB: {e}")
            return None
        except ValueError as e:
            print(f"Erro ao processar JSON da série {serie_name} do BCB: {e}")
            return None

    def fetch_and_store_serie(self, serie_name: str, db: Session):
        print(f"Buscando dados da série {serie_name}...")
        # Para a primeira carga ou cargas menos frequentes, pode-se passar um start_date mais antigo
        # Ex: self.get_serie_data(serie_name, start_date="01/01/2020")
        data = self.get_serie_data(serie_name)
        if data:
            self._save_time_series_data(db=db, serie_name=serie_name, data=data)
        else:
            print(f"Não foi possível obter dados da série {serie_name}.")

    def run_all_fetches(self):
        db: Session = next(get_market_db()) # Obtem uma sessão do banco de dados
        try:
            self.fetch_and_store_serie("selic_meta", db)
            self.fetch_and_store_serie("ipca_mensal", db)
            self.fetch_and_store_serie("dolar_venda_ptax", db)
            # Adicionar outras séries aqui
        finally:
            db.close() # Fecha a sessão

# Exemplo de uso (para ser chamado pelo agendador)
if __name__ == "__main__":
    # Este if __name__ == "__main__": é para teste local do script.
    # A inicialização das tabelas deve ocorrer no main.py do serviço.
    from .db.market_data_db import create_market_data_tables
    create_market_data_tables() # Garante que as tabelas existam para o teste
    
    bcb_service = BCBService()
    bcb_service.run_all_fetches()

