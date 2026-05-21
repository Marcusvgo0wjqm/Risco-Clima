"""
Script para popular o banco de dados com dados de teste
"""
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import (
    ENSO, Precipitation, Temperature, AnalyticalCapacity, 
    Impact, RiskMatrix, RiskLevel
)
from app.services.risk_calculator import RiskCalculator

def seed_database():
    """Popula o banco com dados de teste"""
    db = SessionLocal()
    
    try:
        # Criar ENSO
        enso = ENSO(
            index_value="moderado",
            tms_anomaly=1.5,
            source="manual",
            date_observed=datetime.utcnow()
        )
        db.add(enso)
        db.commit()
        print(f"✓ ENSO criado: ID={enso.id}")
        
        # Criar Precipitação
        precipitation = Precipitation(
            index_value="101-150",
            accumulated_mm=125.5,
            hourly_intensity=15.5,
            persistence_hours=24,
            climatological_percentile=75.0,
            source="manual",
            forecast_date=datetime.utcnow()
        )
        db.add(precipitation)
        db.commit()
        print(f"✓ Precipitação criada: ID={precipitation.id}")
        
        # Criar Temperatura
        temperature = Temperature(
            index_value="mais_2",
            max_temp=32.5,
            avg_temp=28.0,
            thermal_persistence=18,
            climatological_anomaly=2.5,
            source="manual",
            forecast_date=datetime.utcnow()
        )
        db.add(temperature)
        db.commit()
        print(f"✓ Temperatura criada: ID={temperature.id}")
        
        # Criar Capacidade Analítica
        capacity = AnalyticalCapacity(
            capacity_level="elevada",
            specialized_team=True,
            continuous_monitoring=True,
            nowcasting_capability=True,
            prospective_analysis=True,
            hydrological_integration=True,
            human_validation=True,
            date_assessed=datetime.utcnow()
        )
        db.add(capacity)
        db.commit()
        print(f"✓ Capacidade Analítica criada: ID={capacity.id}")
        
        # Criar Impacto
        impact = Impact(
            index_value="severo",
            affected_population=50000,
            flood_areas_km2=25.5,
            critical_infrastructure_affected="Rodovia BR-116, Ponte do Guaíba",
            service_interruption_hours=12,
            human_damages="Sem perdas humanas relatadas",
            economic_damages_usd=500000.0,
            description="Possível alagamento em zonas baixas da cidade",
            date_assessed=datetime.utcnow()
        )
        db.add(impact)
        db.commit()
        print(f"✓ Impacto criado: ID={impact.id}")
        
        # Calcular Matriz de Risco
        calculator = RiskCalculator()
        risk_matrix = calculator.calculate_risk_matrix(
            db=db,
            enso_id=enso.id,
            precipitation_id=precipitation.id,
            temperature_id=temperature.id,
            analytical_capacity_id=capacity.id,
            impact_id=impact.id,
            forecast_horizon_hours=48,
            observations="Dados de teste para validação do sistema"
        )
        print(f"✓ Matriz de Risco criada: ID={risk_matrix.id}")
        print(f"  - Perigo Climático: {risk_matrix.climatic_hazard}")
        print(f"  - Probabilidade Ajustada: {risk_matrix.adjusted_probability}")
        print(f"  - Risco Final: {risk_matrix.final_risk}")
        print(f"  - Nível: {risk_matrix.risk_level.value}")
        
        print("\n✓ Banco de dados populado com sucesso!")
        
    except Exception as e:
        print(f"✗ Erro ao popular banco: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
