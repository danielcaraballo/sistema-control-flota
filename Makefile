.PHONY: help dev-backend dev-frontend dev test-backend test-frontend test lint format migrate shell setup clean

help:
	@echo "SCF — Sistema de Control de Flota"
	@echo ""
	@echo "Uso: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  dev-backend     Iniciar servidor Django"
	@echo "  dev-frontend    Iniciar servidor Vite"
	@echo "  dev             Ambos servidores en paralelo"
	@echo "  test-backend    Tests de Django"
	@echo "  test            Tests de Django + lint de frontend"
	@echo "  lint            Ruff (backend) + ESLint (frontend)"
	@echo "  format          Ruff format (backend) + Prettier (frontend)"
	@echo "  migrate         makemigrations + migrate"
	@echo "  shell           Django shell"
	@echo "  setup           uv sync + npm install + migrate"
	@echo "  clean           Eliminar __pycache__, .venv, node_modules"

dev-backend:
	cd backend && uv run python manage.py runserver

dev-frontend:
	cd frontend && npm run dev

dev:
	@echo "Iniciando backend y frontend..."
	cd backend && uv run python manage.py runserver &
	cd frontend && npm run dev

test-backend:
	cd backend && uv run python manage.py test

test:
	cd backend && uv run python manage.py test
	cd frontend && npx eslint .

lint:
	cd backend && uv run ruff check .
	cd frontend && npx eslint .

format:
	cd backend && uv run ruff format .
	cd frontend && npx prettier --write .

migrate:
	cd backend && uv run python manage.py makemigrations
	cd backend && uv run python manage.py migrate

shell:
	cd backend && uv run python manage.py shell

setup:
	cd backend && uv sync
	cd frontend && npm install
	cd backend && uv run python manage.py migrate

clean:
	rm -rf backend/**/__pycache__ backend/.venv frontend/node_modules
	rm -rf backend/.ruff_cache