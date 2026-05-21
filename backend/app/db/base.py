from app.models import (
    ENSO,
    Precipitation,
    Temperature,
    AnalyticalCapacity,
    Impact,
    RiskMatrix,
    Alert,
    AuditLog
)

# Importar todos os modelos para que alembic os reconheça
__all__ = [
    "ENSO",
    "Precipitation",
    "Temperature",
    "AnalyticalCapacity",
    "Impact",
    "RiskMatrix",
    "Alert",
    "AuditLog"
]
