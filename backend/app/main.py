from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from app.core.config import get_settings
from app.core.logger import get_logger
from app.api.routes import enso, risk, precipitation, temperature, impact, capacity, alerts, audit
from app.db.session import Base, engine

# Criar as tabelas
Base.metadata.create_all(bind=engine)

# Configurações
settings = get_settings()
logger = get_logger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="Plataforma de Avaliação Prospectiva de Risco Climático",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar hosts permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(enso.router)
app.include_router(precipitation.router)
app.include_router(temperature.router)
app.include_router(impact.router)
app.include_router(capacity.router)
app.include_router(risk.router)
app.include_router(alerts.router)
app.include_router(audit.router)

# Health Check
@app.get("/health")
def health_check():
    """Verifica a saúde da aplicação"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow(),
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

# Raiz
@app.get("/")
def root():
    """Endpoint raiz"""
    return {
        "message": "Bem-vindo à Plataforma de Avaliação Prospectiva de Risco Climático",
        "docs": "/docs",
        "health": "/health"
    }

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Erro não tratado: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
