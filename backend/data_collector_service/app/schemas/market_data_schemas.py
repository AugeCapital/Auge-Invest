from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class TimeSeriesDataRead(BaseModel):
    id: int
    serie_name: str
    date: date
    value: float
    source: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True # Pydantic V2, formerly orm_mode

# TODO: Add other schemas if needed for different data types or API responses

