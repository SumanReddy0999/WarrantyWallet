# Backend (FastAPI)

## Setup

1. Create a virtual environment (recommended)
   - Windows PowerShell:
     - `python -m venv .venv`
     - `.venv\\Scripts\\Activate.ps1`
2. Install dependencies
   - `pip install -r requirements.txt`
3. Run the server
   - `uvicorn app.main:app --reload --port 5000`

The API will be available at `http://localhost:5000/`.

## Endpoints

- `GET /health` — health check
- `POST /auth/signup` — create account
- `POST /auth/login` — get JWT
- `POST /ai/chat` — basic AI echo, uses OpenAI if `OPENAI_API_KEY` is set

## Environment variables

- `SECRET_KEY` — JWT signing secret
- `DATABASE_URL` — SQLAlchemy URL (default Postgres `postgresql+psycopg://postgres:postgres@localhost:5432/warranty_wallet`)
- `FRONTEND_ORIGIN` — CORS allowed origin (default `http://localhost:5173`)
- `OPENAI_API_KEY` — optional, enables OpenAI-backed responses


