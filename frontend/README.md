# Frontend - Clima Risk Platform

Interface React/Next.js para Plataforma de Avaliação Prospectiva de Risco Climático

## Estrutura

```
frontend/
├── src/
│   ├── app/                         # Next.js App Router
│   │   ├── layout.tsx               # Layout raiz
│   │   ├── page.tsx                 # Dashboard principal
│   │   ├── manual-input/            # Inserção manual
│   │   │   └── page.tsx
│   │   ├── alerts/                  # Gerenciamento de alertas
│   │   │   └── page.tsx
│   │   ├── audit/                   # Log de auditoria
│   │   │   └── page.tsx
│   │   └── history/                 # Histórico
│   │       └── page.tsx
│   ├── components/                  # Componentes React
│   │   ├── Dashboard/
│   │   ├── RiskMatrix/
│   │   ├── Map/
│   │   ├── Charts/
│   │   ├── AlertSystem/
│   │   └── AuditLog/
│   ├── services/
│   │   └── api.ts                   # Cliente HTTP
│   ├── types/
│   │   └── index.ts                 # TypeScript types
│   └── styles/
│       └── globals.css              # Tailwind + custom styles
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
├── package.json
└── Dockerfile
```

## Instalação

### Com Docker

```bash
docker-compose up frontend
```

### Localmente

```bash
cd frontend
npm install
npm run dev
```

A aplicação estará disponível em `http://localhost:3000`

## Scripts

```bash
# Desenvolvimento
npm run dev

# Build para produção
npm run build

# Iniciar produção
npm start

# Verificar tipos TypeScript
npm run type-check

# Lint
npm run lint
```

## Páginas

### Dashboard (`/`)
- Visão geral do risco
- Situação meteorológica atual
- Distribuição de riscos
- Alertas ativos
- Quick actions

### Inserção Manual (`/manual-input`)
- Formulário para inserção de dados
- ENSO, Precipitação, Temperatura
- Impacto esperado
- Observações técnicas

### Alertas (`/alerts`)
- Lista de alertas ativos
- Níveis: atenção, alerta, alerta alto, extremo
- Informações de vigência

### Auditoria (`/audit`)
- Trilha completa de operações
- Parecer técnico dos meteorologistas
- Rastreabilidade decisória

### Histórico (`/history`)
- Eventos passados
- Análise comparativa
- Validação pós-evento

## Componentes Principais

### Dashboard Component
Exibe:
- Resumo de risco
- Gráficos temporais
- Mapa de situação
- Estatísticas

### RiskMatrix Component
- Visualização da matriz
- Cálculos exibidos
- Status colorido por nível

### AlertSystem Component
- Cards de alerta
- Ícones de severidade
- Informações de vigência

### Map Component
- Mapa interativo com Leaflet
- Sobreposição de geometrias
- Pontos de estação

## Estilização

### Tailwind CSS
- Cores personalizadas para risco
- Layout responsivo
- Dark mode ready (futuro)

### Cores de Risco
- **Baixo**: Verde (success)
- **Moderado**: Amarelo (warning)
- **Alto**: Laranja/Vermelho (danger)
- **Extremo**: Vermelho intenso
- **Crítico**: Vermelho muito intenso

## Variáveis de Ambiente

Criar `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## TypeScript

Tipos completos para:
- ENSO, Precipitação, Temperatura
- Matriz de Risco
- Alertas
- Logs de auditoria

## API Integration

Cliente HTTP com Axios:
- Endpoints tipados
- Error handling
- Request/response interceptors
- Timeout configurável

## Performance

- Next.js static generation quando aplicável
- Image optimization
- Code splitting automático
- Font optimization

## Acessibilidade

- Semântica HTML correta
- ARIA labels
- Contraste de cores
- Teclado navegável

## Development

### Hot Reload
```bash
npm run dev
```

Mudanças são refletidas instantaneamente.

### Type Checking
```bash
npm run type-check
```

### Lint
```bash
npm run lint
```

## Build para Produção

```bash
npm run build
npm start
```

## Docker

```bash
docker build -t clima-risk-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=<api-url> clima-risk-frontend
```

## Futuras Melhorias

- [ ] Gráficos interativos avançados
- [ ] Exportação de relatórios
- [ ] Dark mode
- [ ] Internacionalização (i18n)
- [ ] Progressive Web App (PWA)
- [ ] Real-time updates com WebSocket
- [ ] Mobile responsivo aprimorado

## License

MIT
