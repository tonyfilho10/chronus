PYTHON = venv/Scripts/python.exe
PIP = venv/Scripts/pip.exe
MANAGE = $(PYTHON) manage.py
DC = docker-compose

.PHONY: setup run test lint shell logs migrate static help

setup:
	$(PIP) install -r requirements/development.txt
	cp -n .env.example .env || true
	$(MANAGE) migrate
	$(MANAGE) createsuperuser --noinput || true

run:
	$(DC) up

run-local:
	$(MANAGE) runserver

worker:
	venv/Scripts/celery.exe -A config worker --loglevel=info

test:
	venv/Scripts/pytest.exe --cov=apps --cov-report=term-missing --cov-fail-under=80

lint:
	venv/Scripts/ruff.exe check .
	venv/Scripts/black.exe --check .
	venv/Scripts/isort.exe --check-only .

lint-fix:
	venv/Scripts/ruff.exe check . --fix
	venv/Scripts/black.exe .
	venv/Scripts/isort.exe .

shell:
	$(MANAGE) shell_plus

logs:
	$(DC) logs -f web

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

static:
	$(MANAGE) collectstatic --noinput

stop:
	$(DC) down

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup      - Instala dependências, configura .env e roda migrations"
	@echo "  make run        - Inicia Docker Compose"
	@echo "  make run-local  - Inicia servidor Django local"
	@echo "  make test       - Roda testes com cobertura"
	@echo "  make lint       - Verifica formatação do código"
	@echo "  make lint-fix   - Corrige formatação automaticamente"
	@echo "  make shell      - Abre Django shell_plus"
	@echo "  make logs       - Exibe logs do container web"
	@echo "  make migrate    - Cria e aplica migrations"
	@echo "  make static     - Coleta arquivos estáticos"
