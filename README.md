# SCF - Sistema de Control de Flota

Sistema corporativo para la gestión integral de flota vehicular.

## Stack

- **Backend:** Django Ninja (Python 3.11+)
- **Frontend:** Vue.js 3 + Pinia + Vue Router (PWA)
- **Base de datos:** PostgreSQL
- **Infraestructura:** Docker (próximamente)

## Requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (opcional, fallback a SQLite en dev)

## Inicio rápido

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver

# Frontend
cd frontend
npm install
npm run dev
```
