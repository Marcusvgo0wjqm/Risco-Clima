"""
Testes básicos para a API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup():
    """Setup para cada teste"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_health():
    """Testa o endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_root():
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_enso():
    """Testa criação de ENSO"""
    enso_data = {
        "index_value": "moderado",
        "tms_anomaly": 1.5,
        "source": "manual",
        "date_observed": "2024-05-20T10:00:00"
    }
    response = client.post("/api/enso/", json=enso_data)
    assert response.status_code == 201
    assert response.json()["index_value"] == "moderado"
    assert response.json()["tms_anomaly"] == 1.5

def test_list_enso():
    """Testa listagem de ENSO"""
    # Criar alguns ENSOs
    for i in range(3):
        enso_data = {
            "index_value": "fraco",
            "tms_anomaly": 0.5 + i,
            "source": "manual",
            "date_observed": "2024-05-20T10:00:00"
        }
        client.post("/api/enso/", json=enso_data)
    
    response = client.get("/api/enso/")
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_create_precipitation():
    """Testa criação de precipitação"""
    precip_data = {
        "index_value": "101-150",
        "accumulated_mm": 125.5,
        "source": "manual",
        "forecast_date": "2024-05-20T10:00:00"
    }
    response = client.post("/api/precipitation/", json=precip_data)
    assert response.status_code == 201
    assert response.json()["accumulated_mm"] == 125.5

def test_create_temperature():
    """Testa criação de temperatura"""
    temp_data = {
        "index_value": "mais_2",
        "max_temp": 32.5,
        "source": "manual",
        "forecast_date": "2024-05-20T10:00:00"
    }
    response = client.post("/api/temperature/", json=temp_data)
    assert response.status_code == 201
    assert response.json()["max_temp"] == 32.5

def test_create_impact():
    """Testa criação de impacto"""
    impact_data = {
        "index_value": "severo",
        "affected_population": 50000,
        "flood_areas_km2": 25.5,
        "date_assessed": "2024-05-20T10:00:00"
    }
    response = client.post("/api/impact/", json=impact_data)
    assert response.status_code == 201
    assert response.json()["index_value"] == "severo"

def test_create_analytical_capacity():
    """Testa criação de capacidade analítica"""
    capacity_data = {
        "capacity_level": "elevada",
        "specialized_team": True,
        "continuous_monitoring": True,
        "date_assessed": "2024-05-20T10:00:00"
    }
    response = client.post("/api/analytical-capacity/", json=capacity_data)
    assert response.status_code == 201
    assert response.json()["capacity_level"] == "elevada"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
