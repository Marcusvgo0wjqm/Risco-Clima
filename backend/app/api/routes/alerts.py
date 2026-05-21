from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models import Alert
from app.schemas import AlertCreate, AlertResponse
from app.services.alert_service import AlertService
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])
alert_service = AlertService()

@router.post("/", response_model=AlertResponse, status_code=201)
def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo alerta
    """
    try:
        alert = alert_service.create_alert(
            db=db,
            risk_matrix_id=alert_data.risk_matrix_id,
            alert_level=alert_data.alert_level,
            title=alert_data.title,
            description=alert_data.description,
            expires_at=alert_data.expires_at,
            recipients=alert_data.recipients
        )
        return alert
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[AlertResponse])
def list_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """
    Lista alertas com filtros opcionais
    """
    query = db.query(Alert)
    
    if active_only:
        query = query.filter(Alert.is_active == True)
    
    return query.order_by(Alert.issued_at.desc()).offset(skip).limit(limit).all()

@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna um alerta específico
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    return alert

@router.put("/{alert_id}/deactivate", response_model=AlertResponse)
def deactivate_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """
    Desativa um alerta
    """
    try:
        alert = alert_service.deactivate_alert(db, alert_id)
        return alert
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{alert_id}", status_code=204)
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta um alerta
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    
    db.delete(alert)
    db.commit()
    
    logger.info(f"Alerta deletado: ID={alert_id}")

@router.get("/risk-matrix/{risk_matrix_id}")
def get_alerts_by_risk_matrix(
    risk_matrix_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna todos os alertas associados a uma matriz de risco
    """
    alerts = db.query(Alert).filter(Alert.risk_matrix_id == risk_matrix_id).all()
    return alerts

@router.post("/clean-expired")
def clean_expired_alerts(
    db: Session = Depends(get_db)
):
    """
    Remove alertas expirados
    """
    count = alert_service.clean_expired_alerts(db)
    return {"message": f"{count} alertas expirados foram desativados"}
