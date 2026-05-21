from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

# =====================
# ENSO Schemas
# =====================

class ENSOIndexEnum(str, Enum):
    NEUTRALIDADE = "neutralidade"
    FRACO = "fraco"
    MODERADO = "moderado"
    FORTE = "forte"
    MUITO_FORTE = "muito_forte"

class ENSOCreate(BaseModel):
    index_value: ENSOIndexEnum
    tms_anomaly: float = Field(..., description="Anomalia de Temperatura da Superfície do Mar")
    source: str = Field(default="manual", description="Fonte do dado (manual, noaa, cptec)")
    date_observed: datetime

class ENSOResponse(ENSOCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# =====================
# Precipitation Schemas
# =====================

class PrecipitationIndexEnum(str, Enum):
    ATE_50 = "até_50"
    DE_51_A_100 = "51-100"
    DE_101_A_150 = "101-150"
    DE_151_A_250 = "151-250"
    ACIMA_250 = "acima_250"

class PrecipitationCreate(BaseModel):
    index_value: PrecipitationIndexEnum
    accumulated_mm: float
    hourly_intensity: Optional[float] = None
    persistence_hours: Optional[int] = None
    climatological_percentile: Optional[float] = None
    source: str = Field(default="manual")
    forecast_date: datetime
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PrecipitationResponse(PrecipitationCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# =====================
# Temperature Schemas
# =====================

class TemperatureIndexEnum(str, Enum):
    NORMAL = "normal"
    MAIS_1 = "mais_1"
    MAIS_2 = "mais_2"
    MAIS_3 = "mais_3"
    MAIS_4_PERSISTENTE = "mais_4_persistente"

class TemperatureCreate(BaseModel):
    index_value: TemperatureIndexEnum
    max_temp: float
    avg_temp: Optional[float] = None
    thermal_persistence: Optional[int] = None
    climatological_anomaly: Optional[float] = None
    source: str = Field(default="manual")
    forecast_date: datetime
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class TemperatureResponse(TemperatureCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# =====================
# Analytical Capacity Schemas
# =====================

class CapacityLevelEnum(str, Enum):
    BAIXA = "baixa"
    MODERADA = "moderada"
    ELEVADA = "elevada"
    ESPECIALIZADA = "especializada"
    AVANCADA = "avançada"

class AnalyticalCapacityCreate(BaseModel):
    capacity_level: CapacityLevelEnum
    specialized_team: bool = False
    continuous_monitoring: bool = False
    nowcasting_capability: bool = False
    prospective_analysis: bool = False
    hydrological_integration: bool = False
    human_validation: bool = False
    date_assessed: datetime

class AnalyticalCapacityResponse(AnalyticalCapacityCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# =====================
# Impact Schemas
# =====================

class ImpactIndexEnum(str, Enum):
    INSIGNIFICANTE = "insignificante"
    BAIXO = "baixo"
    MODERADO = "moderado"
    SEVERO = "severo"
    CRITICO = "crítico"

class ImpactCreate(BaseModel):
    index_value: ImpactIndexEnum
    affected_population: Optional[int] = None
    flood_areas_km2: Optional[float] = None
    critical_infrastructure_affected: Optional[str] = None
    service_interruption_hours: Optional[int] = None
    human_damages: Optional[str] = None
    economic_damages_usd: Optional[float] = None
    description: Optional[str] = None
    date_assessed: datetime

class ImpactResponse(ImpactCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# =====================
# Risk Matrix Schemas
# =====================

class RiskLevelEnum(str, Enum):
    BAIXO = "baixo"
    MODERADO = "moderado"
    ALTO = "alto"
    EXTREMO = "extremo"
    CRITICO = "crítico"

class RiskMatrixCreate(BaseModel):
    enso_id: int
    precipitation_id: int
    temperature_id: int
    analytical_capacity_id: int
    impact_id: int
    forecast_horizon_hours: Optional[int] = None
    observations: Optional[str] = None

class RiskMatrixResponse(BaseModel):
    id: int
    climatic_hazard: float
    adjusted_probability: float
    final_risk: float
    risk_level: RiskLevelEnum
    calculation_timestamp: datetime
    forecast_horizon_hours: Optional[int]
    observations: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# =====================
# Alert Schemas
# =====================

class AlertLevelEnum(str, Enum):
    ATENCAO = "atenção"
    ALERTA = "alerta"
    ALERTA_ALTO = "alerta_alto"
    ALERTA_EXTREMO = "alerta_extremo"

class AlertCreate(BaseModel):
    risk_matrix_id: int
    alert_level: AlertLevelEnum
    title: str
    description: str
    expires_at: Optional[datetime] = None
    recipients: Optional[list] = None

class AlertResponse(AlertCreate):
    id: int
    is_active: bool
    issued_at: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# =====================
# Audit Log Schemas
# =====================

class AuditLogCreate(BaseModel):
    risk_matrix_id: Optional[int] = None
    alert_id: Optional[int] = None
    user_id: Optional[str] = None
    action: str
    entity_type: str
    changes: Optional[dict] = None
    technical_opinion: Optional[str] = None
    justification: Optional[str] = None

class AuditLogResponse(AuditLogCreate):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True
