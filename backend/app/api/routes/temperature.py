from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models import Temperature
from app.schemas import TemperatureCreate, TemperatureResponse
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/temperature", tags=["Temperature"])

@router.post("/", response_model=TemperatureResponse, status_code=201)
def create_temperature(
    temp_data: TemperatureCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo registro de temperatura
    """
    temperature = Temperature(
        index_value=temp_data.index_value,
        max_temp=temp_data.max_temp,
        avg_temp=temp_data.avg_temp,
        thermal_persistence=temp_data.thermal_persistence,
        climatological_anomaly=temp_data.climatological_anomaly,
        source=temp_data.source,
        forecast_date=temp_data.forecast_date
    )
    
    db.add(temperature)
    db.commit()
    db.refresh(temperature)
    
    logger.info(f"Temperatura criada: ID={temperature.id}, Índice={temperature.index_value}")
    
    return temperature

@router.get("/", response_model=List[TemperatureResponse])
def list_temperature(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros de temperatura
    """
    return db.query(Temperature).offset(skip).limit(limit).all()

@router.get("/{temp_id}", response_model=TemperatureResponse)
def get_temperature(
    temp_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna um registro de temperatura específico
    """
    temperature = db.query(Temperature).filter(Temperature.id == temp_id).first()
    if not temperature:
        raise HTTPException(status_code=404, detail="Temperatura não encontrada")
    return temperature

@router.put("/{temp_id}", response_model=TemperatureResponse)
def update_temperature(
    temp_id: int,
    temp_data: TemperatureCreate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um registro de temperatura
    """
    temperature = db.query(Temperature).filter(Temperature.id == temp_id).first()
    if not temperature:
        raise HTTPException(status_code=404, detail="Temperatura não encontrada")
    
    temperature.index_value = temp_data.index_value
    temperature.max_temp = temp_data.max_temp
    temperature.avg_temp = temp_data.avg_temp
    temperature.thermal_persistence = temp_data.thermal_persistence
    temperature.climatological_anomaly = temp_data.climatological_anomaly
    temperature.source = temp_data.source
    temperature.forecast_date = temp_data.forecast_date
    
    db.commit()
    db.refresh(temperature)
    
    logger.info(f"Temperatura atualizada: ID={temperature.id}")
    
    return temperature

@router.delete("/{temp_id}", status_code=204)
def delete_temperature(
    temp_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta um registro de temperatura
    """
    temperature = db.query(Temperature).filter(Temperature.id == temp_id).first()
    if not temperature:
        raise HTTPException(status_code=404, detail="Temperatura não encontrada")
    
    db.delete(temperature)
    db.commit()
    
    logger.info(f"Temperatura deletada: ID={temp_id}")
