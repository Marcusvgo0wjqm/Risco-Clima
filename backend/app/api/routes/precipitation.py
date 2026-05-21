from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models import Precipitation
from app.schemas import PrecipitationCreate, PrecipitationResponse
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/precipitation", tags=["Precipitation"])

@router.post("/", response_model=PrecipitationResponse, status_code=201)
def create_precipitation(
    precip_data: PrecipitationCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo registro de precipitação
    """
    precipitation = Precipitation(
        index_value=precip_data.index_value,
        accumulated_mm=precip_data.accumulated_mm,
        hourly_intensity=precip_data.hourly_intensity,
        persistence_hours=precip_data.persistence_hours,
        climatological_percentile=precip_data.climatological_percentile,
        source=precip_data.source,
        forecast_date=precip_data.forecast_date
    )
    
    db.add(precipitation)
    db.commit()
    db.refresh(precipitation)
    
    logger.info(f"Precipitação criada: ID={precipitation.id}, Índice={precipitation.index_value}")
    
    return precipitation

@router.get("/", response_model=List[PrecipitationResponse])
def list_precipitation(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros de precipitação
    """
    return db.query(Precipitation).offset(skip).limit(limit).all()

@router.get("/{precip_id}", response_model=PrecipitationResponse)
def get_precipitation(
    precip_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna um registro de precipitação específico
    """
    precipitation = db.query(Precipitation).filter(Precipitation.id == precip_id).first()
    if not precipitation:
        raise HTTPException(status_code=404, detail="Precipitação não encontrada")
    return precipitation

@router.put("/{precip_id}", response_model=PrecipitationResponse)
def update_precipitation(
    precip_id: int,
    precip_data: PrecipitationCreate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um registro de precipitação
    """
    precipitation = db.query(Precipitation).filter(Precipitation.id == precip_id).first()
    if not precipitation:
        raise HTTPException(status_code=404, detail="Precipitação não encontrada")
    
    precipitation.index_value = precip_data.index_value
    precipitation.accumulated_mm = precip_data.accumulated_mm
    precipitation.hourly_intensity = precip_data.hourly_intensity
    precipitation.persistence_hours = precip_data.persistence_hours
    precipitation.climatological_percentile = precip_data.climatological_percentile
    precipitation.source = precip_data.source
    precipitation.forecast_date = precip_data.forecast_date
    
    db.commit()
    db.refresh(precipitation)
    
    logger.info(f"Precipitação atualizada: ID={precipitation.id}")
    
    return precipitation

@router.delete("/{precip_id}", status_code=204)
def delete_precipitation(
    precip_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta um registro de precipitação
    """
    precipitation = db.query(Precipitation).filter(Precipitation.id == precip_id).first()
    if not precipitation:
        raise HTTPException(status_code=404, detail="Precipitação não encontrada")
    
    db.delete(precipitation)
    db.commit()
    
    logger.info(f"Precipitação deletada: ID={precip_id}")
