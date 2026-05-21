from sqlalchemy.orm import Session
from datetime import datetime
from app.models import (
    ENSO, Precipitation, Temperature, AnalyticalCapacity, Impact,
    RiskMatrix, RiskLevel
)
from app.schemas import (
    ENSOCreate, PrecipitationCreate, TemperatureCreate,
    AnalyticalCapacityCreate, ImpactCreate, RiskMatrixCreate
)
from app.core.logger import get_logger

logger = get_logger(__name__)

class RiskCalculator:
    """
    Serviço para cálculo da matriz de risco
    
    Fórmulas:
    - PC (Perigo Climático) = (0,4 × PP) + (0,35 × EN) + (0,25 × OC)
    - Probabilidade Ajustada = PC × FCA
    - Risco Final = Probabilidade × Impacto
    """
    
    # Mapeamento de índices para valores numéricos
    ENSO_VALUES = {
        "neutralidade": 1,
        "fraco": 2,
        "moderado": 3,
        "forte": 4,
        "muito_forte": 5,
    }
    
    PRECIPITATION_VALUES = {
        "até_50": 1,
        "51-100": 2,
        "101-150": 3,
        "151-250": 4,
        "acima_250": 5,
    }
    
    TEMPERATURE_VALUES = {
        "normal": 1,
        "mais_1": 2,
        "mais_2": 3,
        "mais_3": 4,
        "mais_4_persistente": 5,
    }
    
    CAPACITY_VALUES = {
        "baixa": 0.70,
        "moderada": 0.80,
        "elevada": 0.90,
        "especializada": 1.00,
        "avançada": 1.10,
    }
    
    IMPACT_VALUES = {
        "insignificante": 1,
        "baixo": 2,
        "moderado": 3,
        "severo": 4,
        "crítico": 5,
    }
    
    @staticmethod
    def calculate_climatic_hazard(
        precipitation_index: float,
        enso_index: float,
        temperature_index: float
    ) -> float:
        """
        Calcula o Perigo Climático (PC)
        PC = (0,4 × PP) + (0,35 × EN) + (0,25 × OC)
        """
        pc = (0.4 * precipitation_index) + (0.35 * enso_index) + (0.25 * temperature_index)
        return round(pc, 2)
    
    @staticmethod
    def calculate_adjusted_probability(
        climatic_hazard: float,
        capacity_factor: float
    ) -> float:
        """
        Calcula a Probabilidade Ajustada
        Probabilidade Ajustada = PC × FCA
        """
        probability = climatic_hazard * capacity_factor
        return round(probability, 2)
    
    @staticmethod
    def calculate_final_risk(
        probability: float,
        impact_value: float
    ) -> float:
        """
        Calcula o Risco Final
        Risco = Probabilidade × Impacto
        """
        risk = probability * impact_value
        return round(risk, 2)
    
    @staticmethod
    def classify_risk_level(risk_value: float) -> str:
        """
        Classifica o nível de risco baseado no valor
        
        1–4: baixo
        5–9: moderado
        10–14: alto
        15–19: extremo
        20–25: crítico
        """
        if risk_value <= 4:
            return RiskLevel.BAIXO.value
        elif risk_value <= 9:
            return RiskLevel.MODERADO.value
        elif risk_value <= 14:
            return RiskLevel.ALTO.value
        elif risk_value <= 19:
            return RiskLevel.EXTREMO.value
        else:
            return RiskLevel.CRITICO.value
    
    def calculate_risk_matrix(
        self,
        db: Session,
        enso_id: int,
        precipitation_id: int,
        temperature_id: int,
        analytical_capacity_id: int,
        impact_id: int,
        forecast_horizon_hours: int = None,
        observations: str = None
    ) -> RiskMatrix:
        """
        Realiza o cálculo completo da matriz de risco
        """
        # Buscar as entidades no banco
        enso = db.query(ENSO).filter(ENSO.id == enso_id).first()
        precipitation = db.query(Precipitation).filter(Precipitation.id == precipitation_id).first()
        temperature = db.query(Temperature).filter(Temperature.id == temperature_id).first()
        analytical_capacity = db.query(AnalyticalCapacity).filter(AnalyticalCapacity.id == analytical_capacity_id).first()
        impact = db.query(Impact).filter(Impact.id == impact_id).first()
        
        if not all([enso, precipitation, temperature, analytical_capacity, impact]):
            raise ValueError("Uma ou mais entidades de referência não foram encontradas")
        
        # Obter valores numéricos
        enso_value = self.ENSO_VALUES.get(enso.index_value.value, 1)
        precip_value = self.PRECIPITATION_VALUES.get(precipitation.index_value.value, 1)
        temp_value = self.TEMPERATURE_VALUES.get(temperature.index_value.value, 1)
        capacity_factor = self.CAPACITY_VALUES.get(analytical_capacity.capacity_level.value, 0.80)
        impact_value = self.IMPACT_VALUES.get(impact.index_value.value, 1)
        
        # Calcular PC
        climatic_hazard = self.calculate_climatic_hazard(precip_value, enso_value, temp_value)
        
        # Calcular Probabilidade Ajustada
        adjusted_probability = self.calculate_adjusted_probability(climatic_hazard, capacity_factor)
        
        # Calcular Risco Final
        final_risk = self.calculate_final_risk(adjusted_probability, impact_value)
        
        # Classificar nível de risco
        risk_level = self.classify_risk_level(final_risk)
        
        # Criar registro de matriz de risco
        risk_matrix = RiskMatrix(
            enso_id=enso_id,
            precipitation_id=precipitation_id,
            temperature_id=temperature_id,
            analytical_capacity_id=analytical_capacity_id,
            impact_id=impact_id,
            climatic_hazard=climatic_hazard,
            adjusted_probability=adjusted_probability,
            final_risk=final_risk,
            risk_level=RiskLevel[risk_level.upper().replace("_", "")],
            forecast_horizon_hours=forecast_horizon_hours,
            observations=observations
        )
        
        db.add(risk_matrix)
        db.commit()
        db.refresh(risk_matrix)
        
        logger.info(f"Matriz de risco calculada: ID={risk_matrix.id}, Risco={final_risk}, Nível={risk_level}")
        
        return risk_matrix
