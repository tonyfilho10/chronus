# CHRONUS — Prompt Engine AI

> Transforme ideias de aplicativos em Super Prompts técnicos completos, em segundos.

## Visão Geral

CHRONUS é uma plataforma SaaS com IA integrada (Claude API) que gera especificações técnicas detalhadas a partir de uma ideia descrita em linguagem natural. O output é um **Super Prompt** estruturado em 12 seções, pronto para ser consumido por Claude, Cursor, GPT-4 ou qualquer IA de desenvolvimento.

## Arquitetura

```
chronus/
├── config/           # Settings (base/dev/prod), URLs, Celery
├── apps/
│   ├── core/         # Base models (TimeStampedModel, SoftDeleteModel)
│   ├── accounts/     # Auth, User, UsageCounter, AuditLog
│   ├── prompts/      # Core: geração SSE, CRUD, refinamento
│   ├── community/    # Feed público, upvotes
│   ├── templates_library/  # Templates oficiais e da comunidade
│   ├── exports/      # MD, TXT, PDF
│   └── dashboard/    # Métricas e atividade
├── templates/        # Django Templates + Tailwind + Alpine.js + HTMX
├── docker/           # Dockerfile, NGINX
└── .github/workflows # CI/CD (lint → test → build → deploy)
```

**Stack:** Django 6 · DRF · PostgreSQL (Supabase) · Redis · Celery · Anthropic Claude API · Tailwind CSS · HTMX · Alpine.js · Docker

## Pré-requisitos

- Python 3.12+
- Docker + Docker Compose
- Conta Supabase (PostgreSQL)
- Chave de API Anthropic

## Setup local (< 5 comandos)

```bash
# 1. Clone e entre no diretório
git clone https://github.com/seu-usuario/chronus.git && cd chronus

# 2. Crie o virtual environment
python -m venv venv && venv/Scripts/activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Configure o .env
cp .env.example .env
# Edite .env com suas credenciais

# 4. Instale dependências e migre
make setup

# 5. Inicie o servidor
make run-local
```

Acesse: http://localhost:8000

## Variáveis de Ambiente

Veja [.env.example](.env.example) para a lista completa.

> ⚠️ **NUNCA** suba `.env`, credenciais ou API keys para o repositório.

## Comandos

```bash
make run        # Docker Compose (todos os serviços)
make run-local  # Django runserver local
make test       # pytest com cobertura mínima 80%
make lint       # ruff + black + isort
make lint-fix   # Corrige formatação automaticamente
make migrate    # makemigrations + migrate
make shell      # Django shell_plus
make logs       # Logs do container web
```

## Testes

```bash
make test
# ou diretamente:
pytest --cov=apps --cov-report=term-missing --cov-fail-under=80
```

## API Docs

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Schema OpenAPI: http://localhost:8000/api/schema/

## CI/CD

Pipeline GitHub Actions (`.github/workflows/ci.yml`):

| Job | Trigger | Ação |
|-----|---------|------|
| lint | push/PR | ruff + black + isort |
| security | push/PR | bandit + safety |
| test | push/PR | pytest 80% coverage |
| build | push | Docker build + push GHCR |
| deploy | push main | SSH deploy + migrate |

## Roadmap

- [ ] Integração Stripe (billing Pro/Team)
- [ ] Workspace compartilhado (plano Team)
- [ ] Suporte a múltiplos providers de LLM
- [ ] PWA / App mobile
- [ ] Exportação para Notion e Confluence

---

Construído com ❤️ usando Django + Claude API
