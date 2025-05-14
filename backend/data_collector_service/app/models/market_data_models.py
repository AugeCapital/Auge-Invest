from sqlalchemy import Column, Integer, String, Float, Date, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class TimeSeriesData(Base):
    __tablename__ = "time_series_data"

    id = Column(Integer, primary_key=True, index=True)
    serie_name = Column(String, index=True, nullable=False)  # e.g., "selic_meta", "ipca_mensal", "dolar_venda_ptax"
    date = Column(Date, nullable=False, index=True) # Date of the data point
    value = Column(Float, nullable=False) # Value of the data point
    
    # Optional: For metadata or source tracking
    source = Column(String, default="BCB_SGS") # e.g., BCB_SGS, B3, Fundamentus
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Constraint to ensure that each serie has only one value per date
    __table_args__ = (UniqueConstraint("serie_name", "date", name="_serie_date_uc"),)

    def __repr__(self):
        return f"<TimeSeriesData(serie_name=\'{self.serie_name}\', date=\'{self.date}\', value={self.value})>"

# TODO: Add other models if needed, for example, for company fundamental data, news articles, etc.

# Example of how to create tables (to be called from a db setup script or main app lifespan)
# from sqlalchemy import create_engine
# DATABASE_URL = "postgresql://user:password@host:port/market_data_db"
# engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(bind=engine)

