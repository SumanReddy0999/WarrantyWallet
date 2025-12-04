# Warranty Wallet

A comprehensive solution for managing product warranties and purchases.

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 13+
- pgAdmin (optional)

## Backend Setup

1. **Environment Variables**
   Create a `.env` file in the `backend` directory with the following content:

   ```env
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
   OPENAI_API_KEY=your-openai-api-key
   ```

2. **Database Setup**
   - Install PostgreSQL
   - Create a new database named `warranty_wallet`
   - Update the database credentials in `.env` if different

3. **Install Dependencies**
   ```bash
   cd backend
  uvicorn app.main:app --reload
   ```

4. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the Backend Server**
   ```bash
   uvicorn app.main:app --reload
   ```

## Frontend Setup

1. **Install Dependencies**
   ```bash
   cd web-client
   npm install
   ```

2. **Start the Development Server**
   ```bash
   npm run dev
   ```

## PGAdmin Setup

1. Install PGAdmin 4
2. Add a new server with the following details:
   - Host: localhost
   - Port: 5432
   - Maintenance database: postgres
   - Username: postgres
   - Password: 1234

## Default Admin Credentials

- **PGAdmin**
  - Email: admin@example.com
  - Password: admin

## API Documentation

Once the backend server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Backend
- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Shadcn/ui

## License

MIT
