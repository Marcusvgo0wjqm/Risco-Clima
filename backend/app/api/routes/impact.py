from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models import Impact
from app.schemas import ImpactCreate, ImpactResponse
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/impact", tags=["Impact"])

@router.post("/", response_model=ImpactResponse, status_code=201)
def create_impact(
    impact_data: ImpactCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo registro de impacto
    """
    impact = Impact(
        index_value=impact_data.index_value,
        affected_population=impact_data.affected_population,
        flood_areas_km2=impact_data.flood_areas_km2,
        critical_infrastructure_affected=impact_data.critical_infrastructure_affected,
        service_interruption_hours=impact_data.service_interruption_hours,
        human_damages=impact_data.human_damages,
        economic_damages_usd=impact_data.economic_damages_usd,
        description=impact_data.description,
        date_assessed=impact_data.date_assessed
    )
    
    db.add(impact)
    db.commit()
    db.refresh(impact)
    
    logger.info(f"Impacto criado: ID={impact.id}, Índice={impact.index_value}")
    
    return impact

@router.get("/", response_model=List[ImpactResponse])
def list_impact(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros de impacto
    """
    return db.query(Impact).offset(skip).limit(limit).all()

@router.get("/{impact_id}", response_model=ImpactResponse)
def get_impact(
    impact_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna um registro de impacto específico
    """
    impact = db.query(Impact).filter(Impact.id == impact_id).first()
    if not impact:
        raise HTTPException(status_code=404, detail="Impacto não encontrado")
    return impact

@router.put("/{impact_id}", response_model=ImpactResponse)
def update_impact(
    impact_id: int,
    impact_data: ImpactCreate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um registro de impacto
    """
    impact = db.query(Impact).filter(Impact.id == impact_id).first()
    if not impact:
        raise HTTPException(status_code=404, detail="Impacto não encontrado")
    
    impact.index_value = impact_data.index_value
    impact.affected_population = impact_data.affected_population
    impact.flood_areas_km2 = impact_data.flood_areas_km2
    impact.critical_infrastructure_affected = impact_data.critical_infrastructure_affected
    impact.service_interruption_hours = impact_data.service_interruption_hours
    impact.human_damages = impact_data.human_damages
    impact.economic_damages_usd = impact_data.economic_damages_usd
    impact.description = impact_data.description
    impact.date_assessed = impact_data.date_assessed
    
    db.commit()
    db.refresh(impact)
    
    logger.info(f"Impacto atualizado: ID={impact.id}")
    
    return impact

@router.delete("/{impact_id}", status_code=204)
def delete_impact(
    impact_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta um registro de impacto
    """
    impact = db.query(Impact).filter(Impact.id == impact_id).first()
    if not impact:
        raise HTTPException(status_code=404, detail="Impacto não encontrado")
    
    db.delete(impact)
    db.commit()
    
    logger.info(f"Impacto deletado: ID={impact_id}")
