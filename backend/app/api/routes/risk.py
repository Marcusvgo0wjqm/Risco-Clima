from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.models import RiskMatrix
from app.schemas import RiskMatrixCreate, RiskMatrixResponse
from app.services.risk_calculator import RiskCalculator
from app.services.alert_service import AlertService
from app.services.audit_service import AuditService
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/risk", tags=["Risk Matrix"])
risk_calculator = RiskCalculator()
alert_service = AlertService()
audit_service = AuditService()

@router.post("/calculate", response_model=RiskMatrixResponse, status_code=201)
def calculate_risk(
    risk_data: RiskMatrixCreate,
    db: Session = Depends(get_db)
):
    """
    Calcula uma nova matriz de risco
    """
    try:
        risk_matrix = risk_calculator.calculate_risk_matrix(
            db=db,
            enso_id=risk_data.enso_id,
            precipitation_id=risk_data.precipitation_id,
            temperature_id=risk_data.temperature_id,
            analytical_capacity_id=risk_data.analytical_capacity_id,
            impact_id=risk_data.impact_id,
            forecast_horizon_hours=risk_data.forecast_horizon_hours,
            observations=risk_data.observations
        )
        
        # Gerar alerta automaticamente
        alert_service.auto_generate_alert(db, risk_matrix)
        
        # Registrar na auditoria
        audit_service.log_action(
            db=db,
            action="create",
            entity_type="risk_matrix",
            risk_matrix_id=risk_matrix.id,
            changes={
                "climatic_hazard": risk_matrix.climatic_hazard,
                "adjusted_probability": risk_matrix.adjusted_probability,
                "final_risk": risk_matrix.final_risk,
                "risk_level": risk_matrix.risk_level.value
            }
        )
        
        return risk_matrix
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[RiskMatrixResponse])
def list_risk_matrices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    risk_level: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    Lista matrizes de risco com filtros opcionais
    """
    query = db.query(RiskMatrix)
    
    if risk_level:
        query = query.filter(RiskMatrix.risk_level == risk_level)
    
    return query.order_by(RiskMatrix.calculation_timestamp.desc()).offset(skip).limit(limit).all()

@router.get("/{risk_id}", response_model=RiskMatrixResponse)
def get_risk_matrix(
    risk_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna uma matriz de risco específica
    """
    risk_matrix = db.query(RiskMatrix).filter(RiskMatrix.id == risk_id).first()
    if not risk_matrix:
        raise HTTPException(status_code=404, detail="Matriz de risco não encontrada")
    return risk_matrix

@router.get("/{risk_id}/audit-trail")
def get_risk_audit_trail(
    risk_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna a trilha de auditoria completa de uma matriz de risco
    """
    risk_matrix = db.query(RiskMatrix).filter(RiskMatrix.id == risk_id).first()
    if not risk_matrix:
        raise HTTPException(status_code=404, detail="Matriz de risco não encontrada")
    
    audit_logs = audit_service.get_audit_trail_for_risk_matrix(db, risk_id)
    
    return {
        "risk_matrix_id": risk_id,
        "audit_logs": [
            {
                "id": log.id,
                "action": log.action,
                "entity_type": log.entity_type,
                "user_id": log.user_id,
                "technical_opinion": log.technical_opinion,
                "justification": log.justification,
                "timestamp": log.timestamp
            }
            for log in audit_logs
        ]
    }

@router.get("/dashboard/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db)
):
    """
    Retorna resumo para o dashboard operacional
    """
    # Matriz de risco mais recente
    latest_risk = db.query(RiskMatrix).order_by(
        RiskMatrix.calculation_timestamp.desc()
    ).first()
    
    # Contadores por nível de risco
    from sqlalchemy import func
    risk_counts = db.query(
        RiskMatrix.risk_level,
        func.count(RiskMatrix.id).label("count")
    ).group_by(RiskMatrix.risk_level).all()
    
    risk_distribution = {
        risk_level: count
        for risk_level, count in risk_counts
    }
    
    # Alertas ativos
    from app.models import Alert
    active_alerts = db.query(Alert).filter(Alert.is_active == True).count()
    
    return {
        "latest_risk_matrix": latest_risk.id if latest_risk else None,
        "latest_risk_level": latest_risk.risk_level.value if latest_risk else None,
        "latest_risk_value": latest_risk.final_risk if latest_risk else None,
        "risk_distribution": risk_distribution,
        "active_alerts_count": active_alerts,
        "timestamp": datetime.utcnow()
    }
