# Guia de Início Rápido - Clima Risk Platform

## 📋 Pré-requisitos

- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento local)
- Node.js 20+ (para desenvolvimento local)

## 🚀 Inicialização Rápida com Docker

### 1. Preparar variáveis de ambiente

```bash
# Backend
cd backend
cp .env.example .env

# Frontend
cd ../frontend
cp .env.example .env.local
```

### 2. Iniciar os serviços

```bash
cd ..  # Volta à raiz do projeto
docker-compose up
```

Aguarde alguns minutos para que todos os serviços iniciem. Você verá mensagens de log indicando que o PostgreSQL, Redis, Backend e Frontend estão rodando.

### 3. Acessar a plataforma

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

## 🛠️ Desenvolvimento Local

### Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# Iniciar servidor
uvicorn app.main:app --reload
```

O servidor estará disponível em http://localhost:8000

### Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env.local
# Editar .env.local com suas configurações

# Iniciar servidor de desenvolvimento
npm run dev
```

A aplicação estará disponível em http://localhost:3000

## 📊 Populando Banco de Dados com Dados de Teste

```bash
cd backend
python seed.py
```

Isso criará registros de teste que você pode usar para explorar a plataforma.

## 🧪 Executar Testes

```bash
cd backend
pytest tests.py -v
```

## 📚 Estrutura do Projeto

```
clima-risk-platform/
├── backend/              # API FastAPI + Python
│   ├── app/             # Código da aplicação
│   ├── requirements.txt  # Dependências Python
│   ├── Dockerfile       # Container do backend
│   └── seed.py          # Script para popular BD
├── frontend/            # Interface React + Next.js
│   ├── src/
│   ├── package.json     # Dependências Node
│   ├── Dockerfile       # Container do frontend
│   └── next.config.js   # Configuração Next.js
├── docker-compose.yml   # Orquestração de containers
└── README.md           # Documentação geral
```

## 🔑 Funcionalidades Principais

### Dashboard Operacional
- Visualização em tempo real do nível de risco
- Status de alertas ativos
- Distribuição de riscos por nível
- Gráficos e métricas operacionais

### Inserção Manual de Dados
- Formulário para inserir:
  - Índice ENSO
  - Precipitação prevista
  - Anomalias térmicas
  - Impacto esperado
- Cálculo automático da matriz de risco
- Geração automática de alertas

### Sistema de Alertas
- Níveis: Atenção, Alerta, Alerta Alto, Extremo
- Filtros por nível de severidade
- Informações de vigência

### Auditoria Analítica
- Rastreabilidade completa de operações
- Parecer técnico dos meteorologistas
- Justificativas operacionais
- Histórico de mudanças

## 📡 Endpoints da API

### ENSO
- `POST /api/enso/` - Criar ENSO
- `GET /api/enso/` - Listar ENSO
- `GET /api/enso/{id}` - Obter ENSO
- `PUT /api/enso/{id}` - Atualizar ENSO
- `DELETE /api/enso/{id}` - Deletar ENSO

### Precipitação
- `POST /api/precipitation/` - Criar
- `GET /api/precipitation/` - Listar
- `GET /api/precipitation/{id}` - Obter
- `PUT /api/precipitation/{id}` - Atualizar
- `DELETE /api/precipitation/{id}` - Deletar

### Temperatura
- `POST /api/temperature/` - Criar
- `GET /api/temperature/` - Listar
- `GET /api/temperature/{id}` - Obter
- `PUT /api/temperature/{id}` - Atualizar
- `DELETE /api/temperature/{id}` - Deletar

### Matriz de Risco
- `POST /api/risk/calculate` - Calcular risco
- `GET /api/risk/` - Listar matrizes
- `GET /api/risk/{id}` - Obter matriz
- `GET /api/risk/{id}/audit-trail` - Trilha de auditoria
- `GET /api/risk/dashboard/summary` - Resumo

### Alertas
- `POST /api/alerts/` - Criar alerta
- `GET /api/alerts/` - Listar alertas
- `GET /api/alerts/{id}` - Obter alerta
- `PUT /api/alerts/{id}/deactivate` - Desativar
- `POST /api/alerts/clean-expired` - Limpar expirados

### Auditoria
- `POST /api/audit/` - Criar log
- `GET /api/audit/` - Listar logs
- `GET /api/audit/{id}` - Obter log
- `GET /api/audit/risk-matrix/{id}/trail` - Trilha de matriz

## 🔧 Variáveis de Ambiente

### Backend (.env)
```
DATABASE_URL=postgresql://clima_user:clima_password@localhost:5432/clima_risk_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=sua-secret-key-aqui
DEBUG=False
LOG_LEVEL=INFO
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

### Porta já em uso
```bash
# Matar processo usando a porta (Linux/Mac)
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Banco de dados não conecta
```bash
# Reiniciar container do PostgreSQL
docker-compose down
docker-compose up -d postgres
docker-compose up
```

### Módulo Python não encontrado
```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

## 📞 Suporte

Para mais informações, consulte:
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [Documentação Geral](./README.md)

## 📄 Licença

MIT
