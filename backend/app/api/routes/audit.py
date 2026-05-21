from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models import AuditLog
from app.schemas import AuditLogCreate, AuditLogResponse
from app.services.audit_service import AuditService
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/audit", tags=["Audit"])
audit_service = AuditService()

@router.post("/", response_model=AuditLogResponse, status_code=201)
def create_audit_log(
    log_data: AuditLogCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo log de auditoria
    """
    audit_log = audit_service.log_action(
        db=db,
        action=log_data.action,
        entity_type=log_data.entity_type,
        risk_matrix_id=log_data.risk_matrix_id,
        alert_id=log_data.alert_id,
        user_id=log_data.user_id,
        changes=log_data.changes,
        technical_opinion=log_data.technical_opinion,
        justification=log_data.justification
    )
    return audit_log

@router.get("/", response_model=List[AuditLogResponse])
def list_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    entity_type: str = Query(None),
    risk_matrix_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """
    Lista logs de auditoria com filtros opcionais
    """
    logs = audit_service.get_audit_logs(
        db=db,
        risk_matrix_id=risk_matrix_id,
        entity_type=entity_type,
        limit=limit + skip
    )
    return logs[skip:skip + limit]

@router.get("/{log_id}", response_model=AuditLogResponse)
def get_audit_log(
    log_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna um log de auditoria específico
    """
    log = db.query(AuditLog).filter(AuditLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log de auditoria não encontrado")
    return log

@router.get("/risk-matrix/{risk_matrix_id}/trail")
def get_risk_matrix_audit_trail(
    risk_matrix_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna a trilha de auditoria completa de uma matriz de risco
    """
    logs = audit_service.get_audit_trail_for_risk_matrix(db, risk_matrix_id)
    
    if not logs:
        raise HTTPException(status_code=404, detail="Nenhum log encontrado para esta matriz")
    
    return {
        "risk_matrix_id": risk_matrix_id,
        "logs": [
            {
                "id": log.id,
                "action": log.action,
                "entity_type": log.entity_type,
                "user_id": log.user_id,
                "technical_opinion": log.technical_opinion,
                "justification": log.justification,
                "timestamp": log.timestamp,
                "changes": log.changes
            }
            for log in logs
        ]
    }

@router.get("/user/{user_id}")
def get_user_audit_logs(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Retorna todos os logs de um usuário específico
    """
    logs = db.query(AuditLog).filter(
        AuditLog.user_id == user_id
    ).order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    
    return logs

@router.post("/validation")
def log_validation(
    risk_matrix_id: int,
    user_id: str,
    technical_opinion: str,
    db: Session = Depends(get_db)
):
    """
    Registra uma validação técnica
    """
    audit_log = audit_service.log_validation(
        db=db,
        risk_matrix_id=risk_matrix_id,
        user_id=user_id,
        technical_opinion=technical_opinion
    )
    return audit_log

@router.post("/manual-update")
def log_manual_update(
    entity_type: str,
    entity_id: int,
    user_id: str,
    changes: dict,
    technical_opinion: str,
    justification: str,
    db: Session = Depends(get_db)
):
    """
    Registra uma atualização manual com parecer técnico
    """
    audit_log = audit_service.log_manual_update(
        db=db,
        entity_type=entity_type,
        entity_id=entity_id,
        user_id=user_id,
        changes=changes,
        technical_opinion=technical_opinion,
        justification=justification
    )
    return audit_log
