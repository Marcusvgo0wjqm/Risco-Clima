from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models import AuditLog
from app.core.logger import get_logger

logger = get_logger(__name__)

class AuditService:
    """
    Serviço de auditoria analítica
    
    Registra todas as operações para rastreabilidade decisória
    """
    
    def log_action(
        self,
        db: Session,
        action: str,
        entity_type: str,
        risk_matrix_id: Optional[int] = None,
        alert_id: Optional[int] = None,
        user_id: Optional[str] = None,
        changes: Optional[Dict[str, Any]] = None,
        technical_opinion: Optional[str] = None,
        justification: Optional[str] = None
    ) -> AuditLog:
        """
        Registra uma ação no log de auditoria
        
        Args:
            action: Tipo de ação (create, update, delete, validate)
            entity_type: Tipo de entidade (enso, precipitation, temperature, etc)
            risk_matrix_id: ID da matriz de risco associada
            alert_id: ID do alerta associado
            user_id: ID do usuário que realizou a ação
            changes: Dicionário das mudanças realizadas
            technical_opinion: Parecer técnico do meteorologista
            justification: Justificativa operacional
        """
        audit_log = AuditLog(
            risk_matrix_id=risk_matrix_id,
            alert_id=alert_id,
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            changes=changes,
            technical_opinion=technical_opinion,
            justification=justification
        )
        
        db.add(audit_log)
        db.commit()
        db.refresh(audit_log)
        
        logger.info(
            f"Auditoria registrada: ID={audit_log.id}, "
            f"Ação={action}, Entidade={entity_type}, "
            f"Usuário={user_id}"
        )
        
        return audit_log
    
    def get_audit_logs(
        self,
        db: Session,
        risk_matrix_id: Optional[int] = None,
        entity_type: Optional[str] = None,
        limit: int = 100
    ) -> List[AuditLog]:
        """
        Retorna logs de auditoria com filtros opcionais
        """
        query = db.query(AuditLog)
        
        if risk_matrix_id:
            query = query.filter(AuditLog.risk_matrix_id == risk_matrix_id)
        
        if entity_type:
            query = query.filter(AuditLog.entity_type == entity_type)
        
        return query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    def get_audit_trail_for_risk_matrix(
        self,
        db: Session,
        risk_matrix_id: int
    ) -> List[AuditLog]:
        """
        Retorna a trilha de auditoria completa para uma matriz de risco
        """
        return db.query(AuditLog).filter(
            AuditLog.risk_matrix_id == risk_matrix_id
        ).order_by(AuditLog.timestamp.asc()).all()
    
    def log_manual_update(
        self,
        db: Session,
        entity_type: str,
        entity_id: int,
        user_id: str,
        changes: Dict[str, Any],
        technical_opinion: str,
        justification: str
    ) -> AuditLog:
        """
        Registra uma atualização manual com parecer técnico
        """
        return self.log_action(
            db=db,
            action="update",
            entity_type=entity_type,
            user_id=user_id,
            changes=changes,
            technical_opinion=technical_opinion,
            justification=justification
        )
    
    def log_validation(
        self,
        db: Session,
        risk_matrix_id: int,
        user_id: str,
        technical_opinion: str
    ) -> AuditLog:
        """
        Registra uma validação técnica de cenários
        """
        return self.log_action(
            db=db,
            action="validate",
            entity_type="risk_matrix",
            risk_matrix_id=risk_matrix_id,
            user_id=user_id,
            technical_opinion=technical_opinion
        )
