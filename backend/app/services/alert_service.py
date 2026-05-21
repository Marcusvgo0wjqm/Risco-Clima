from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from app.models import Alert, AlertLevel, RiskMatrix
from app.schemas import AlertCreate
from app.core.logger import get_logger

logger = get_logger(__name__)

class AlertService:
    """
    Serviço para gerenciamento de alertas automáticos
    
    Níveis de alerta:
    - Atenção: Monitorar situação
    - Alerta: Preparar estrutura operacional
    - Alerta Alto: Ativar protocolos de emergência
    - Alerta Extremo: Máxima mobilização
    """
    
    # Mapeamento de níveis de risco para níveis de alerta
    RISK_TO_ALERT_MAPPING = {
        "baixo": "atenção",
        "moderado": "alerta",
        "alto": "alerta_alto",
        "extremo": "alerta_extremo",
        "crítico": "alerta_extremo",
    }
    
    def create_alert(
        self,
        db: Session,
        risk_matrix_id: int,
        alert_level: str,
        title: str,
        description: str,
        expires_at: Optional[datetime] = None,
        recipients: Optional[List[str]] = None
    ) -> Alert:
        """
        Cria um novo alerta
        """
        # Validar se a matriz de risco existe
        risk_matrix = db.query(RiskMatrix).filter(RiskMatrix.id == risk_matrix_id).first()
        if not risk_matrix:
            raise ValueError(f"Matriz de risco ID {risk_matrix_id} não encontrada")
        
        # Se expira_at não for fornecido, definir padrão de 24 horas
        if not expires_at:
            expires_at = datetime.utcnow() + timedelta(hours=24)
        
        alert = Alert(
            risk_matrix_id=risk_matrix_id,
            alert_level=AlertLevel[alert_level.upper().replace("_", "")],
            title=title,
            description=description,
            expires_at=expires_at,
            recipients=recipients or []
        )
        
        db.add(alert)
        db.commit()
        db.refresh(alert)
        
        logger.info(f"Alerta criado: ID={alert.id}, Nível={alert_level}, Matriz={risk_matrix_id}")
        
        return alert
    
    def auto_generate_alert(
        self,
        db: Session,
        risk_matrix: RiskMatrix
    ) -> Optional[Alert]:
        """
        Gera automaticamente um alerta baseado no nível de risco
        """
        alert_level = self.RISK_TO_ALERT_MAPPING.get(risk_matrix.risk_level.value, "atenção")
        
        title = f"Alerta de Risco Climático - Nível {risk_matrix.risk_level.value.upper()}"
        description = (
            f"Matriz de risco calculada com valor final de {risk_matrix.final_risk}.\n"
            f"Perigo Climático: {risk_matrix.climatic_hazard}\n"
            f"Probabilidade Ajustada: {risk_matrix.adjusted_probability}\n"
            f"Observações: {risk_matrix.observations or 'Nenhuma'}"
        )
        
        return self.create_alert(
            db=db,
            risk_matrix_id=risk_matrix.id,
            alert_level=alert_level,
            title=title,
            description=description
        )
    
    def get_active_alerts(self, db: Session) -> List[Alert]:
        """
        Retorna todos os alertas ativos
        """
        return db.query(Alert).filter(Alert.is_active == True).all()
    
    def deactivate_alert(self, db: Session, alert_id: int) -> Alert:
        """
        Desativa um alerta
        """
        alert = db.query(Alert).filter(Alert.id == alert_id).first()
        if not alert:
            raise ValueError(f"Alerta ID {alert_id} não encontrado")
        
        alert.is_active = False
        db.commit()
        db.refresh(alert)
        
        logger.info(f"Alerta desativado: ID={alert_id}")
        
        return alert
    
    def clean_expired_alerts(self, db: Session) -> int:
        """
        Remove alertas expirados do banco de dados
        """
        expired_alerts = db.query(Alert).filter(
            Alert.expires_at <= datetime.utcnow(),
            Alert.is_active == True
        ).all()
        
        count = len(expired_alerts)
        for alert in expired_alerts:
            alert.is_active = False
        
        db.commit()
        
        logger.info(f"{count} alertas expirados foram desativados")
        
        return count
