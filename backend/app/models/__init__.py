from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON
from geoalchemy2 import Geometry
from datetime import datetime
import enum

from app.db.session import Base

class ENSOIndex(str, enum.Enum):
    NEUTRALIDADE = "neutralidade"
    FRACO = "fraco"
    MODERADO = "moderado"
    FORTE = "forte"
    MUITO_FORTE = "muito_forte"

class PrecipitationIndex(str, enum.Enum):
    ATE_50 = "até_50"
    DE_51_A_100 = "51-100"
    DE_101_A_150 = "101-150"
    DE_151_A_250 = "151-250"
    ACIMA_250 = "acima_250"

class TemperatureIndex(str, enum.Enum):
    NORMAL = "normal"
    MAIS_1 = "mais_1"
    MAIS_2 = "mais_2"
    MAIS_3 = "mais_3"
    MAIS_4_PERSISTENTE = "mais_4_persistente"

class CapacityLevel(str, enum.Enum):
    BAIXA = "baixa"
    MODERADA = "moderada"
    ELEVADA = "elevada"
    ESPECIALIZADA = "especializada"
    AVANCADA = "avançada"

class ImpactIndex(str, enum.Enum):
    INSIGNIFICANTE = "insignificante"
    BAIXO = "baixo"
    MODERADO = "moderado"
    SEVERO = "severo"
    CRITICO = "crítico"

class RiskLevel(str, enum.Enum):
    BAIXO = "baixo"           # 1-4
    MODERADO = "moderado"     # 5-9
    ALTO = "alto"             # 10-14
    EXTREMO = "extremo"       # 15-19
    CRITICO = "crítico"       # 20-25

class AlertLevel(str, enum.Enum):
    ATENCAO = "atenção"
    ALERTA = "alerta"
    ALERTA_ALTO = "alerta_alto"
    ALERTA_EXTREMO = "alerta_extremo"

# Modelo ENSO
class ENSO(Base):
    __tablename__ = "enso"
    
    id = Column(Integer, primary_key=True, index=True)
    index_value = Column(Enum(ENSOIndex), nullable=False)
    tms_anomaly = Column(Float, nullable=False)  # Temperatura superfície do mar
    source = Column(String, default="manual")  # manual, noaa, cptec
    date_observed = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    risk_matrices = relationship("RiskMatrix", back_populates="enso")

# Modelo Precipitação
class Precipitation(Base):
    __tablename__ = "precipitation"
    
    id = Column(Integer, primary_key=True, index=True)
    index_value = Column(Enum(PrecipitationIndex), nullable=False)
    accumulated_mm = Column(Float, nullable=False)
    hourly_intensity = Column(Float, nullable=True)
    persistence_hours = Column(Integer, nullable=True)
    climatological_percentile = Column(Float, nullable=True)
    source = Column(String, default="manual")  # ecmwf, gfs, inmet, etc
    forecast_date = Column(DateTime, nullable=False)
    geometry = Column(Geometry('POINT'), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    risk_matrices = relationship("RiskMatrix", back_populates="precipitation")

# Modelo Temperatura
class Temperature(Base):
    __tablename__ = "temperature"
    
    id = Column(Integer, primary_key=True, index=True)
    index_value = Column(Enum(TemperatureIndex), nullable=False)
    max_temp = Column(Float, nullable=False)
    avg_temp = Column(Float, nullable=True)
    thermal_persistence = Column(Integer, nullable=True)  # em horas
    climatological_anomaly = Column(Float, nullable=True)
    source = Column(String, default="manual")
    forecast_date = Column(DateTime, nullable=False)
    geometry = Column(Geometry('POINT'), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    risk_matrices = relationship("RiskMatrix", back_populates="temperature")

# Modelo de Capacidade Analítica
class AnalyticalCapacity(Base):
    __tablename__ = "analytical_capacity"
    
    id = Column(Integer, primary_key=True, index=True)
    capacity_level = Column(Enum(CapacityLevel), nullable=False)
    specialized_team = Column(Boolean, default=False)
    continuous_monitoring = Column(Boolean, default=False)
    nowcasting_capability = Column(Boolean, default=False)
    prospective_analysis = Column(Boolean, default=False)
    hydrological_integration = Column(Boolean, default=False)
    human_validation = Column(Boolean, default=False)
    date_assessed = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    risk_matrices = relationship("RiskMatrix", back_populates="analytical_capacity")

# Modelo de Impacto
class Impact(Base):
    __tablename__ = "impact"
    
    id = Column(Integer, primary_key=True, index=True)
    index_value = Column(Enum(ImpactIndex), nullable=False)
    affected_population = Column(Integer, nullable=True)
    flood_areas_km2 = Column(Float, nullable=True)
    critical_infrastructure_affected = Column(String, nullable=True)
    service_interruption_hours = Column(Integer, nullable=True)
    human_damages = Column(String, nullable=True)
    economic_damages_usd = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    date_assessed = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    risk_matrices = relationship("RiskMatrix", back_populates="impact")

# Modelo de Matriz de Risco (núcleo)
class RiskMatrix(Base):
    __tablename__ = "risk_matrix"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Referências às variáveis primárias
    enso_id = Column(Integer, ForeignKey("enso.id"), nullable=False)
    precipitation_id = Column(Integer, ForeignKey("precipitation.id"), nullable=False)
    temperature_id = Column(Integer, ForeignKey("temperature.id"), nullable=False)
    analytical_capacity_id = Column(Integer, ForeignKey("analytical_capacity.id"), nullable=False)
    impact_id = Column(Integer, ForeignKey("impact.id"), nullable=False)
    
    # Cálculos da matriz
    climatic_hazard = Column(Float, nullable=False)  # PC = (0.4*PP) + (0.35*EN) + (0.25*OC)
    adjusted_probability = Column(Float, nullable=False)  # PC * FCA
    final_risk = Column(Float, nullable=False)  # Probabilidade * Impacto
    risk_level = Column(Enum(RiskLevel), nullable=False)
    
    # Metadados
    calculation_timestamp = Column(DateTime, server_default=func.now())
    forecast_horizon_hours = Column(Integer, nullable=True)  # 24, 48, 72, 120, 240
    observations = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    enso = relationship("ENSO", back_populates="risk_matrices")
    precipitation = relationship("Precipitation", back_populates="risk_matrices")
    temperature = relationship("Temperature", back_populates="risk_matrices")
    analytical_capacity = relationship("AnalyticalCapacity", back_populates="risk_matrices")
    impact = relationship("Impact", back_populates="risk_matrices")
    alerts = relationship("Alert", back_populates="risk_matrix")
    audit_logs = relationship("AuditLog", back_populates="risk_matrix")

# Modelo de Alertas
class Alert(Base):
    __tablename__ = "alert"
    
    id = Column(Integer, primary_key=True, index=True)
    risk_matrix_id = Column(Integer, ForeignKey("risk_matrix.id"), nullable=False)
    alert_level = Column(Enum(AlertLevel), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    issued_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=True)
    recipients = Column(JSON, nullable=True)  # Lista de e-mails/telefones
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    risk_matrix = relationship("RiskMatrix", back_populates="alerts")
    audit_logs = relationship("AuditLog", back_populates="alert")

# Modelo de Log de Auditoria
class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    risk_matrix_id = Column(Integer, ForeignKey("risk_matrix.id"), nullable=True)
    alert_id = Column(Integer, ForeignKey("alert.id"), nullable=True)
    user_id = Column(String, nullable=True)
    action = Column(String, nullable=False)  # create, update, delete, validate
    entity_type = Column(String, nullable=False)  # enso, precipitation, temperature, etc
    changes = Column(JSON, nullable=True)  # Mudanças realizadas
    technical_opinion = Column(Text, nullable=True)
    justification = Column(Text, nullable=True)
    timestamp = Column(DateTime, server_default=func.now())
    
    risk_matrix = relationship("RiskMatrix", back_populates="audit_logs")
    alert = relationship("Alert", back_populates="audit_logs")
