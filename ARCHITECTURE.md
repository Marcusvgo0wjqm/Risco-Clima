# Arquitetura - Plataforma de Risco Climático

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js + React)                  │
│                      Port: 3000                                 │
├──────────────┬──────────────┬────────────┬──────────┬───────────┤
│  Dashboard   │ Manual Input │  Alerts    │  Audit   │ History   │
│  (page.tsx)  │ (page.tsx)   │ (page.tsx) │(page.tsx)│(page.tsx) │
└──────────────┴──────────────┴────────────┴──────────┴───────────┘
                                    │
                        API HTTP/REST (JSON)
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│               BACKEND (FastAPI + Python)                        │
│                      Port: 8000                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  API Routes (35 endpoints)                                      │
│  ├── /api/enso/                                                 │
│  ├── /api/precipitation/                                        │
│  ├── /api/temperature/                                          │
│  ├── /api/impact/                                               │
│  ├── /api/analytical-capacity/                                  │
│  ├── /api/risk/                 ◄── Núcleo da Plataforma       │
│  ├── /api/alerts/                                               │
│  └── /api/audit/                                                │
│                                                                 │
│  Services (Lógica de Negócio)                                   │
│  ├── RiskCalculator             ◄── Fórmulas de Risco          │
│  ├── AlertService               ◄── Alertas Automáticos        │
│  └── AuditService               ◄── Rastreabilidade            │
│                                                                 │
│  Core                                                           │
│  ├── config.py          (Settings)                              │
│  ├── security.py        (JWT, Password)                         │
│  ├── logger.py          (Logging)                               │
│  └── database           (Session Management)                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         │                           │                      │
         ▼                           ▼                      ▼
    ┌─────────────┐            ┌─────────────┐      ┌──────────┐
    │ PostgreSQL  │            │   Redis     │      │ File     │
    │ + PostGIS   │            │   Cache     │      │ System   │
    │ Port: 5432  │            │ Port: 6379  │      │ (Logs)   │
    │             │            │             │      │          │
    │  Tabelas:   │            │ Sessions    │      │ /var/log │
    │  • enso     │            │ Celery      │      │          │
    │  • precip   │            │             │      └──────────┘
    │  • temp     │            └─────────────┘
    │  • impact   │
    │  • capacity │
    │  • risk     │
    │  • alert    │
    │  • audit    │
    │             │
    │ Volume:     │
    │ postgres_   │
    │ data        │
    │             │
    └─────────────┘
```

## Fluxo de Dados - Cálculo de Risco

```
ENTRADA
│
├─ Manual ou Automática
│
▼
┌───────────────────────────────────────┐
│   Dados Primários Recebidos            │
│  • ENSO                               │
│  • Precipitação Prevista              │
│  • Temperatura Anômala                │
│  • Capacidade Institucional           │
│  • Impacto Esperado                   │
└───────────────────────────────────────┘
│
▼
┌───────────────────────────────────────┐
│    Validação Pydantic Schemas         │
│   (Type Checking + Constraints)       │
└───────────────────────────────────────┘
│
▼
┌───────────────────────────────────────┐
│      RiskCalculator.calculate()        │
│                                       │
│  1. PC = (0.4×PP)+(0.35×EN)+(0.25×OC)│
│  2. Prob = PC × FCA                   │
│  3. Risk = Prob × Impact              │
│  4. Level = Classify(Risk)            │
└───────────────────────────────────────┘
│
▼
┌───────────────────────────────────────┐
│      Persistir RiskMatrix              │
│    (PostgreSQL + Timestamps)          │
└───────────────────────────────────────┘
│
▼
┌───────────────────────────────────────┐
│    AlertService.auto_generate()        │
│   (Se Risk > Threshold)               │
└───────────────────────────────────────┘
│
▼
┌───────────────────────────────────────┐
│    AuditService.log_action()           │
│  (Rastreabilidade Completa)           │
└───────────────────────────────────────┘
│
▼
┌───────────────────────────────────────┐
│  SAÍDA: Dashboard Atualizado           │
│  • Nível de Risco                     │
│  • Valor Final                        │
│  • Alertas Ativos                     │
│  • Histórico de Auditoria             │
└───────────────────────────────────────┘
```

## Camadas de Aplicação

```
┌─────────────────────────────────────────────────┐
│         PRESENTATION LAYER (Frontend)           │
│  React Components + Next.js Pages               │
│  TypeScript Types + Tailwind CSS                │
└─────────────────────────────────────────────────┘
                       ▲
                       │
                  HTTP/REST
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│         APPLICATION LAYER (Backend)             │
│  API Routes + Request Validation                │
│  Pydantic Schemas                               │
└─────────────────────────────────────────────────┘
                       ▲
                       │
                   Internal APIs
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│           BUSINESS LOGIC LAYER                  │
│  • RiskCalculator                               │
│  • AlertService                                 │
│  • AuditService                                 │
│  Fórmulas + Algoritmos                          │
└─────────────────────────────────────────────────┘
                       ▲
                       │
                  SQLAlchemy ORM
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│           DATA ACCESS LAYER                     │
│  SQLAlchemy Models                              │
│  PostgreSQL Connection Pool                     │
└─────────────────────────────────────────────────┘
                       ▲
                       │
                   SQL Queries
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│            DATABASE LAYER                       │
│  PostgreSQL + PostGIS                           │
│  8 Tabelas Normalizadas                         │
│  Indexes + Foreign Keys                         │
└─────────────────────────────────────────────────┘
```

## Modelo de Dados - Relacionamentos

```
┌─────────────┐
│    ENSO     │
├─────────────┤
│ id (PK)     │
│ index_value │
│ tms_anomaly │
│ source      │
│ date_obs    │
└──────┬──────┘
       │
       │ (1:N)
       │
       ▼
┌──────────────────┐         ┌──────────────────┐
│  PRECIPITATION   │         │  TEMPERATURE     │
├──────────────────┤         ├──────────────────┤
│ id (PK)          │         │ id (PK)          │
│ accumulated_mm   │         │ max_temp         │
│ index_value      │         │ index_value      │
│ source           │         │ source           │
│ forecast_date    │         │ forecast_date    │
└────────┬─────────┘         └────────┬─────────┘
         │                           │
         │ (N:1)                     │ (N:1)
         │                           │
         └───────────┬───────────────┘
                     │
                     ▼
         ┌──────────────────────┐
         │   RISK_MATRIX        │
         ├──────────────────────┤
         │ id (PK)              │
         │ enso_id (FK)         │ ◄──┐
         │ precip_id (FK)       │ ◄──┼─ Entrada
         │ temp_id (FK)         │ ◄──┤
         │ capacity_id (FK)     │ ◄──┘
         │ impact_id (FK)       │ ◄──┐
         │ climatic_hazard      │    │
         │ adjusted_prob        │ ◄──┼─ Cálculos
         │ final_risk           │    │
         │ risk_level           │    │
         │ calc_timestamp       │    │
         └──────────┬───────────┘    │
                    │                │
         ┌──────────┴─────────┐ ◄────┘
         │                    │
    (1:N)│                    │ (N:1)
         │                    │
         ▼                    │
    ┌────────────┐      ┌──────────────┐
    │   ALERT    │      │   IMPACT     │
    ├────────────┤      ├──────────────┤
    │ id (PK)    │      │ id (PK)      │
    │ risk_id(FK)│      │ index_value  │
    │ alert_level│      │ pop_affected │
    │ is_active  │      │ description  │
    │ expires_at │      │ date_assessed│
    └────────────┘      └──────────────┘
         │
         │ (1:N)
         │
         ▼
    ┌──────────────────┐
    │   AUDIT_LOG      │
    ├──────────────────┤
    │ id (PK)          │
    │ risk_id (FK)     │
    │ alert_id (FK)    │
    │ action           │
    │ entity_type      │
    │ tech_opinion     │
    │ justification    │
    │ timestamp        │
    └──────────────────┘

ANALYTICAL_CAPACITY
├──────────────────────┤
│ id (PK)              │
│ capacity_level       │
│ specialist_team      │
│ continuous_monitor   │
│ nowcasting           │
│ date_assessed        │
└──────────────────────┘
         ▲
         │ (N:1)
         │
    RISK_MATRIX
```

## Segurança - Fluxo de Autenticação

```
┌─────────────────────────────────────────────────┐
│           CLIENTE (Frontend)                    │
│                                                 │
│  1. Usuário insere credenciais                  │
│  2. POST /api/token                             │
│  3. Recebe JWT Token                            │
│  4. Armazena em localStorage                    │
│  5. Inclui em Authorization Header              │
└─────────────────────────────────────────────────┘
                       │
                POST /api/token
            {"username": "...", "password": "..."}
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│           SERVIDOR (Backend)                    │
│                                                 │
│  1. Validar credenciais                         │
│  2. Hash password com bcrypt                    │
│  3. Gerar JWT Token                             │
│  4. Retornar token                              │
└─────────────────────────────────────────────────┘
                       │
            200 {"access_token": "..."}
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│           CLIENTE com Token                     │
│                                                 │
│  GET /api/risk/                                 │
│  Headers: {                                     │
│    "Authorization": "Bearer eyJhbGc..."        │
│  }                                              │
└─────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│    MIDDLEWARE (FastAPI Dependency)              │
│                                                 │
│  1. Extrair token do header                     │
│  2. Decodificar JWT                             │
│  3. Validar assinatura                          │
│  4. Verificar expiração                         │
│  5. Recuperar usuário                           │
└─────────────────────────────────────────────────┘
         │ Válido          │ Inválido
         │                 │
         ▼                 ▼
    Continuar         401 Unauthorized
```

## Performance - Caching com Redis

```
┌─────────────────────────────────────┐
│    Frontend Request                 │
│  GET /api/risk/dashboard/summary    │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│   Cache Check (Redis)               │
│   Key: "dashboard:summary"          │
└─────────────────────────────────────┘
         │ Encontrado      │ Não encontrado
         │                 │
         ▼                 ▼
    Return JSON      Database Query
    (10ms)           (100ms)
         │                 │
         │                 ▼
         │         ┌────────────────┐
         │         │ Calcular Dados │
         │         └────────────────┘
         │                 │
         │                 ▼
         │         ┌────────────────────────┐
         │         │ Cache em Redis (TTL)   │
         │         │ Válido por 5 minutos   │
         │         └────────────────────────┘
         │                 │
         └─────────┬───────┘
                   │
                   ▼
    ┌──────────────────────────────┐
    │  Return to Client            │
    │  {"status": "ok", "data"...} │
    └──────────────────────────────┘
```

---

*Arquitetura da Plataforma de Avaliação Prospectiva de Risco Climático*
*Última atualização: 20 de Maio de 2026*
