## create a .env file with following and make sure that have the same database, password , user in postgres .
-----------------------------------------------------------------------------------------------------------------------
# Application
DEBUG=True
APP_NAME="Warranty Wallet API"
API_V1_STR=/api/v1

# Security
SECRET_KEY=your-super-secret-key-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days

# Database
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_DB=warranty_wallet
DATABASE_URL=postgresql+psycopg://postgres:1234@localhost:5432/warranty_wallet

# CORS (comma-separated list of origins)
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:8000"]

# File Uploads
UPLOAD_FOLDER=./uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# External Services
OPENAI_API_KEY=

# Email (configure if email functionality is needed)
# SMTP_TLS=True
# SMTP_PORT=587
# SMTP_HOST=smtp.gmail.com
# SMTP_USER=your-email@gmail.com
# SMTP_PASSWORD=your-app-specific-password
# EMAILS_FROM_EMAIL=your-email@gmail.com
# EMAILS_FROM_NAME="Warranty Wallet"
# PGAdmin
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
------------------------------------------------------------------------------------------------
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
