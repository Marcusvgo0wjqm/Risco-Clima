# Clima Risk Platform

Plataforma de Avaliação Prospectiva de Risco Climático para Porto Alegre

## Estrutura do Projeto

```
clima-risk-platform/
├── backend/          # FastAPI + Python
├── frontend/         # Next.js + React
├── docker-compose.yml
└── .github/          # GitHub Actions CI/CD
```

## Início Rápido

### Com Docker Compose

```bash
docker-compose up
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Localmente

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Arquitetura

- **Backend**: FastAPI com SQLAlchemy + PostgreSQL
- **Frontend**: Next.js com TypeScript e Tailwind CSS
- **Database**: PostgreSQL com extensão PostGIS
- **Cache**: Redis
- **Container**: Docker + Docker Compose

## Variáveis de Ambiente

Criar arquivo `.env` na raiz do projeto:

```
DATABASE_URL=postgresql://clima_user:clima_password@localhost:5432/clima_risk_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
DEBUG=False
```

## Módulos Principais

### Backend
- **ENSO Module**: Gestão de índices ENSO
- **Precipitation Module**: Previsão de precipitação
- **Temperature Module**: Anomalias térmicas
- **Risk Calculator**: Cálculo da matriz de risco
- **Alert System**: Sistema de alertas automáticos
- **Audit Logger**: Rastreabilidade analítica

### Frontend
- **Dashboard**: Visualização operacional
- **Risk Matrix**: Exibição da matriz de risco
- **Manual Input**: Inserção manual de dados
- **Alert Management**: Gerenciamento de alertas
- **Audit Log Viewer**: Visualização de logs

## Documentação

- [Backend Docs](./backend/README.md)
- [Frontend Docs](./frontend/README.md)

## Licença

MIT
