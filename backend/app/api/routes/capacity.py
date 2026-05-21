from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models import AnalyticalCapacity
from app.schemas import AnalyticalCapacityCreate, AnalyticalCapacityResponse
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/analytical-capacity", tags=["Analytical Capacity"])

@router.post("/", response_model=AnalyticalCapacityResponse, status_code=201)
def create_analytical_capacity(
    capacity_data: AnalyticalCapacityCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo registro de capacidade analítica
    """
    capacity = AnalyticalCapacity(
        capacity_level=capacity_data.capacity_level,
        specialized_team=capacity_data.specialized_team,
        continuous_monitoring=capacity_data.continuous_monitoring,
        nowcasting_capability=capacity_data.nowcasting_capability,
        prospective_analysis=capacity_data.prospective_analysis,
        hydrological_integration=capacity_data.hydrological_integration,
        human_validation=capacity_data.human_validation,
        date_assessed=capacity_data.date_assessed
    )
    
    db.add(capacity)
    db.commit()
    db.refresh(capacity)
    
    logger.info(f"Capacidade analítica criada: ID={capacity.id}, Nível={capacity.capacity_level}")
    
    return capacity

@router.get("/", response_model=List[AnalyticalCapacityResponse])
def list_analytical_capacity(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros de capacidade analítica
    """
    return db.query(AnalyticalCapacity).offset(skip).limit(limit).all()

@router.get("/{capacity_id}", response_model=AnalyticalCapacityResponse)
def get_analytical_capacity(
    capacity_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna um registro de capacidade analítica específico
    """
    capacity = db.query(AnalyticalCapacity).filter(AnalyticalCapacity.id == capacity_id).first()
    if not capacity:
        raise HTTPException(status_code=404, detail="Capacidade analítica não encontrada")
    return capacity

@router.put("/{capacity_id}", response_model=AnalyticalCapacityResponse)
def update_analytical_capacity(
    capacity_id: int,
    capacity_data: AnalyticalCapacityCreate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um registro de capacidade analítica
    """
    capacity = db.query(AnalyticalCapacity).filter(AnalyticalCapacity.id == capacity_id).first()
    if not capacity:
        raise HTTPException(status_code=404, detail="Capacidade analítica não encontrada")
    
    capacity.capacity_level = capacity_data.capacity_level
    capacity.specialized_team = capacity_data.specialized_team
    capacity.continuous_monitoring = capacity_data.continuous_monitoring
    capacity.nowcasting_capability = capacity_data.nowcasting_capability
    capacity.prospective_analysis = capacity_data.prospective_analysis
    capacity.hydrological_integration = capacity_data.hydrological_integration
    capacity.human_validation = capacity_data.human_validation
    capacity.date_assessed = capacity_data.date_assessed
    
    db.commit()
    db.refresh(capacity)
    
    logger.info(f"Capacidade analítica atualizada: ID={capacity.id}")
    
    return capacity

@router.delete("/{capacity_id}", status_code=204)
def delete_analytical_capacity(
    capacity_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta um registro de capacidade analítica
    """
    capacity = db.query(AnalyticalCapacity).filter(AnalyticalCapacity.id == capacity_id).first()
    if not capacity:
        raise HTTPException(status_code=404, detail="Capacidade analítica não encontrada")
    
    db.delete(capacity)
    db.commit()
    
    logger.info(f"Capacidade analítica deletada: ID={capacity_id}")

@router.get("/latest")
def get_latest_capacity(
    db: Session = Depends(get_db)
):
    """
    Retorna a capacidade analítica mais recente
    """
    capacity = db.query(AnalyticalCapacity).order_by(
        AnalyticalCapacity.date_assessed.desc()
    ).first()
    
    if not capacity:
        raise HTTPException(status_code=404, detail="Nenhuma capacidade analítica registrada")
    
    return capacity
