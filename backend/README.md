# Backend - Clima Risk Platform

API FastAPI para Plataforma de Avaliação Prospectiva de Risco Climático

## Estrutura

```
backend/
├── app/
│   ├── main.py              # Aplicação FastAPI
│   ├── core/                # Configuração central
│   │   ├── config.py        # Settings
│   │   ├── security.py      # Utilitários de segurança
│   │   └── logger.py        # Logger customizado
│   ├── models/              # Modelos SQLAlchemy
│   ├── schemas/             # Schemas Pydantic (validação)
│   ├── services/            # Lógica de negócio
│   │   ├── risk_calculator.py
│   │   ├── alert_service.py
│   │   └── audit_service.py
│   ├── api/routes/          # Rotas da API
│   │   ├── enso.py
│   │   ├── risk.py
│   │   ├── precipitation.py
│   │   ├── temperature.py
│   │   ├── alerts.py
│   │   └── audit.py
│   └── db/                  # Database
│       ├── session.py       # SQLAlchemy setup
│       ├── base.py          # Base models
│       └── migrations/      # Alembic migrations
├── requirements.txt
├── Dockerfile
└── .env
```

## Instalação

### Com Docker

```bash
docker-compose up backend
```

### Localmente

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## Executar

### Com Docker Compose
```bash
docker-compose up backend
```

### Localmente
```bash
uvicorn app.main:app --reload
```

## Endpoints Principais

### Health Check
- `GET /health` - Verifica saúde da aplicação

### ENSO
- `POST /api/enso/` - Criar ENSO
- `GET /api/enso/` - Listar ENSO
- `GET /api/enso/{id}` - Obter ENSO
- `PUT /api/enso/{id}` - Atualizar ENSO
- `DELETE /api/enso/{id}` - Deletar ENSO

### Risk Matrix
- `POST /api/risk/calculate` - Calcular matriz de risco
- `GET /api/risk/` - Listar matrizes
- `GET /api/risk/{id}` - Obter matriz
- `GET /api/risk/{id}/audit-trail` - Trilha de auditoria
- `GET /api/risk/dashboard/summary` - Resumo para dashboard

## Variáveis de Ambiente

Criar `.env`:

```
DATABASE_URL=postgresql://clima_user:clima_password@localhost:5432/clima_risk_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=sua-secret-key
DEBUG=False
LOG_LEVEL=INFO
```

## Documentação da API

Quando a aplicação está rodando:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Modelos de Dados

### ENSO
- Índice (1-5)
- Anomalia de TSM
- Fonte dos dados
- Data observada

### Precipitation
- Índice (1-5)
- Acumulado em mm
- Intensidade horária
- Persistência
- Percentil climatológico

### Temperature
- Índice (1-5)
- Temperatura máxima/média
- Persistência térmica
- Anomalia climatológica

### RiskMatrix
Núcleo da plataforma, integra:
- Perigo Climático (PC)
- Probabilidade Ajustada
- Risco Final
- Nível de Risco

### Alert
- Nível de alerta
- Título e descrição
- Status ativo/inativo
- Destinatários

### AuditLog
- Rastreabilidade completa
- Parecer técnico
- Justificativas operacionais

## Fórmulas

### Perigo Climático (PC)
```
PC = (0,4 × PP) + (0,35 × EN) + (0,25 × OC)
```

### Probabilidade Ajustada
```
Probabilidade = PC × FCA
```

### Risco Final
```
Risco = Probabilidade × Impacto
```

## Desenvolvimento

### Testes

```bash
pytest
```

### Migrações do Banco

```bash
# Criar nova migração
alembic revision --autogenerate -m "Descrição"

# Aplicar migrações
alembic upgrade head
```

## Segurança

- JWT para autenticação (em desenvolvimento)
- Password hashing com bcrypt
- CORS configurável
- Validação com Pydantic

## Logging

Logs estruturados com cores para desenvolvimento e formato texto para produção.

## Performance

- PostgreSQL com PostGIS para dados geoespaciais
- Redis para cache
- Índices otimizados nas tabelas principais
- Connection pooling

## License

MIT
