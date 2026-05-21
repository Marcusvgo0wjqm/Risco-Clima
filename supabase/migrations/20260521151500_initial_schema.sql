-- Habilitar a extensão PostGIS se não estiver habilitada
CREATE EXTENSION IF NOT EXISTS postgis;

-- Criar tipos ENUM correspondentes às regras de negócios e schemas Pydantic
CREATE TYPE ensoindex AS ENUM ('neutralidade', 'fraco', 'moderado', 'forte', 'muito_forte');
CREATE TYPE precipitationindex AS ENUM ('até_50', '51-100', '101-150', '151-250', 'acima_250');
CREATE TYPE temperatureindex AS ENUM ('normal', 'mais_1', 'mais_2', 'mais_3', 'mais_4_persistente');
CREATE TYPE capacitylevel AS ENUM ('baixa', 'moderada', 'elevada', 'especializada', 'avançada');
CREATE TYPE impactindex AS ENUM ('insignificante', 'baixo', 'moderado', 'severo', 'crítico');
CREATE TYPE risklevel AS ENUM ('baixo', 'moderado', 'alto', 'extremo', 'crítico');
CREATE TYPE alertlevel AS ENUM ('atenção', 'alerta', 'alerta_alto', 'alerta_extremo');

-- Tabela ENSO
CREATE TABLE enso (
    id SERIAL PRIMARY KEY, 
    index_value ensoindex NOT NULL, 
    tms_anomaly FLOAT NOT NULL, 
    source VARCHAR DEFAULT 'manual', 
    date_observed TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);
CREATE INDEX ix_enso_id ON enso (id);

-- Tabela Precipitação
CREATE TABLE precipitation (
    id SERIAL PRIMARY KEY, 
    index_value precipitationindex NOT NULL, 
    accumulated_mm FLOAT NOT NULL, 
    hourly_intensity FLOAT, 
    persistence_hours INTEGER, 
    climatological_percentile FLOAT, 
    source VARCHAR DEFAULT 'manual', 
    forecast_date TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    geometry geometry(POINT,-1), 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);
CREATE INDEX ix_precipitation_id ON precipitation (id);
CREATE INDEX idx_precipitation_geometry ON precipitation USING gist (geometry);

-- Tabela Temperatura
CREATE TABLE temperature (
    id SERIAL PRIMARY KEY, 
    index_value temperatureindex NOT NULL, 
    max_temp FLOAT NOT NULL, 
    avg_temp FLOAT, 
    thermal_persistence INTEGER, 
    climatological_anomaly FLOAT, 
    source VARCHAR DEFAULT 'manual', 
    forecast_date TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    geometry geometry(POINT,-1), 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);
CREATE INDEX ix_temperature_id ON temperature (id);
CREATE INDEX idx_temperature_geometry ON temperature USING gist (geometry);

-- Tabela Capacidade Analítica
CREATE TABLE analytical_capacity (
    id SERIAL PRIMARY KEY, 
    capacity_level capacitylevel NOT NULL, 
    specialized_team BOOLEAN DEFAULT FALSE, 
    continuous_monitoring BOOLEAN DEFAULT FALSE, 
    nowcasting_capability BOOLEAN DEFAULT FALSE, 
    prospective_analysis BOOLEAN DEFAULT FALSE, 
    hydrological_integration BOOLEAN DEFAULT FALSE, 
    human_validation BOOLEAN DEFAULT FALSE, 
    date_assessed TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);
CREATE INDEX ix_analytical_capacity_id ON analytical_capacity (id);

-- Tabela Impacto
CREATE TABLE impact (
    id SERIAL PRIMARY KEY, 
    index_value impactindex NOT NULL, 
    affected_population INTEGER, 
    flood_areas_km2 FLOAT, 
    critical_infrastructure_affected VARCHAR, 
    service_interruption_hours INTEGER, 
    human_damages VARCHAR, 
    economic_damages_usd FLOAT, 
    description TEXT, 
    date_assessed TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);
CREATE INDEX ix_impact_id ON impact (id);

-- Tabela Matriz de Risco (núcleo)
CREATE TABLE risk_matrix (
    id SERIAL PRIMARY KEY, 
    enso_id INTEGER NOT NULL REFERENCES enso (id), 
    precipitation_id INTEGER NOT NULL REFERENCES precipitation (id), 
    temperature_id INTEGER NOT NULL REFERENCES temperature (id), 
    analytical_capacity_id INTEGER NOT NULL REFERENCES analytical_capacity (id), 
    impact_id INTEGER NOT NULL REFERENCES impact (id), 
    climatic_hazard FLOAT NOT NULL, 
    adjusted_probability FLOAT NOT NULL, 
    final_risk FLOAT NOT NULL, 
    risk_level risklevel NOT NULL, 
    calculation_timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    forecast_horizon_hours INTEGER, 
    observations TEXT, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);
CREATE INDEX ix_risk_matrix_id ON risk_matrix (id);

-- Tabela Alertas
CREATE TABLE alert (
    id SERIAL PRIMARY KEY, 
    risk_matrix_id INTEGER NOT NULL REFERENCES risk_matrix (id), 
    alert_level alertlevel NOT NULL, 
    title VARCHAR NOT NULL, 
    description TEXT NOT NULL, 
    is_active BOOLEAN DEFAULT TRUE, 
    issued_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    expires_at TIMESTAMP WITHOUT TIME ZONE, 
    recipients JSON, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);
CREATE INDEX ix_alert_id ON alert (id);

-- Tabela Log de Auditoria
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY, 
    risk_matrix_id INTEGER REFERENCES risk_matrix (id), 
    alert_id INTEGER REFERENCES alert (id), 
    user_id VARCHAR, 
    action VARCHAR NOT NULL, 
    entity_type VARCHAR NOT NULL, 
    changes JSON, 
    technical_opinion TEXT, 
    justification TEXT, 
    timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);
CREATE INDEX ix_audit_log_id ON audit_log (id);
