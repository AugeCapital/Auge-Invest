from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from ..db.market_data_db import get_market_db
from ..models.market_data_models import TimeSeriesData # Assuming your model is here
from ..schemas.market_data_schemas import TimeSeriesDataRead # To be created

router = APIRouter()

# TODO: Add pagination, more filtering options (e.g., date range for specific series)

@router.get("/series/{serie_name}", response_model=List[TimeSeriesDataRead])
async def read_time_series_data(
    serie_name: str,
    db: Session = Depends(get_market_db),
    start_date: Optional[date] = Query(None, description="Filter data from this date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter data up to this date (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=1000, description="Limit the number of results") # Default limit 100, max 1000
):
    """
    Retrieve time series data for a specific series name.
    Allows filtering by date range and limiting the number of results.
    Data is returned in descending order of date (most recent first).
    """
    query = db.query(TimeSeriesData).filter(TimeSeriesData.serie_name == serie_name)

    if start_date:
        query = query.filter(TimeSeriesData.date >= start_date)
    if end_date:
        query = query.filter(TimeSeriesData.date <= end_date)
    
    # Order by date descending to get the most recent data first
    data_points = query.order_by(TimeSeriesData.date.desc()).limit(limit).all()
    
    if not data_points:
        # It's better to return an empty list if no data is found for a valid series name
        # raise HTTPException(status_code=404, detail=f"No data found for series: {serie_name}")
        return []
        
    return data_points

@router.get("/series/available", response_model=List[str])
async def get_available_series_names(db: Session = Depends(get_market_db)):
    """
    Get a list of unique series names available in the database.
    """
    distinct_series = db.query(TimeSeriesData.serie_name).distinct().all()
    return [s[0] for s in distinct_series]

# TODO: Add more specific endpoints if needed, e.g., latest value for a series

