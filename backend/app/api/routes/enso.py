from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models import ENSO
from app.schemas import ENSOCreate, ENSOResponse
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/enso", tags=["ENSO"])

@router.post("/", response_model=ENSOResponse, status_code=201)
def create_enso(
    enso_data: ENSOCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo registro ENSO
    """
    enso = ENSO(
        index_value=enso_data.index_value,
        tms_anomaly=enso_data.tms_anomaly,
        source=enso_data.source,
        date_observed=enso_data.date_observed
    )
    
    db.add(enso)
    db.commit()
    db.refresh(enso)
    
    logger.info(f"ENSO criado: ID={enso.id}, Índice={enso.index_value}")
    
    return enso

@router.get("/", response_model=List[ENSOResponse])
def list_enso(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todos os registros ENSO
    """
    return db.query(ENSO).offset(skip).limit(limit).all()

@router.get("/{enso_id}", response_model=ENSOResponse)
def get_enso(
    enso_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna um registro ENSO específico
    """
    enso = db.query(ENSO).filter(ENSO.id == enso_id).first()
    if not enso:
        raise HTTPException(status_code=404, detail="ENSO não encontrado")
    return enso

@router.put("/{enso_id}", response_model=ENSOResponse)
def update_enso(
    enso_id: int,
    enso_data: ENSOCreate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um registro ENSO
    """
    enso = db.query(ENSO).filter(ENSO.id == enso_id).first()
    if not enso:
        raise HTTPException(status_code=404, detail="ENSO não encontrado")
    
    enso.index_value = enso_data.index_value
    enso.tms_anomaly = enso_data.tms_anomaly
    enso.source = enso_data.source
    enso.date_observed = enso_data.date_observed
    
    db.commit()
    db.refresh(enso)
    
    logger.info(f"ENSO atualizado: ID={enso.id}")
    
    return enso

@router.delete("/{enso_id}", status_code=204)
def delete_enso(
    enso_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta um registro ENSO
    """
    enso = db.query(ENSO).filter(ENSO.id == enso_id).first()
    if not enso:
        raise HTTPException(status_code=404, detail="ENSO não encontrado")
    
    db.delete(enso)
    db.commit()
    
    logger.info(f"ENSO deletado: ID={enso_id}")
