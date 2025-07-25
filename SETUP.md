# 🛠️ WarrantyWallet Local Setup Guide

## 1. Prerequisites

- **Node.js** (v18+ recommended)
- **pnpm** (v8+ recommended): [Install guide](https://pnpm.io/installation)
- **Python** (v3.10+ recommended, for ai-service)
- **Docker** (for running PostgreSQL)
- **Git**

---

## 2. Clone the Repository

```sh
git clone <your-repo-url>
cd warrantywallet-test
```

---

## 3. Create .env file in services/auth-service/ folder and paste the below content

```sh
DATABASE_URL="postgresql://postgres:warranty@localhost:5432/Warrant_wallet_v02"
```

---

## 4. Start the Database (PostgreSQL)

The project uses Docker Compose to run a local Postgres instance on port 5432.

```sh
docker-compose up -d
```

- This will create a database named `Warrant_wallet_v02` with user `postgres` and password `warranty`.
- You can check the status with `docker ps`.

---

## 5. Install Node.js Dependencies

From the project root:

```sh
pnpm install
```

- This will install all dependencies for every workspace package (apps, services, packages).

---

## 6. Push Database Schema (Drizzle ORM)

After starting the database and installing dependencies, push the latest schema to Postgres:

```sh
pnpm --filter=auth-service run db:push
```

- This will create all necessary tables in your local Postgres instance.

---

## 7. Build Shared Types

The `shared-types` package must be built before running any TypeScript services:

```sh
pnpm --filter shared-types run build
```

---

## 8. (Optional) Build All Packages

If you want to ensure all TypeScript is built (not just shared-types):

```sh
pnpm build
```

---

## 9. Run Services

You can run all services in development mode using Turborepo:

```sh
pnpm run dev
```

This will:
- Start the **web-client** (React app) on port 5173.
- Start the **auth-service** (Node/Express) on port 5000.
- Start the **ai-service** (FastAPI) on port 8000 (if Python and dependencies are installed).

> **Note:** If you see errors about missing shared-types, make sure you ran the build step above.

---

## 10. (If Needed) Run Services Individually

- **Auth Service** (port 5000):
  ```sh
  pnpm --filter auth-service run dev
  ```
- **AI Service** (port 8000, requires Python):
  ```sh
  cd services/ai-service
  pip install -r requirements.txt
  pnpm run dev
  ```
- **Web Client** (port 5173):
  ```sh
  pnpm --filter web-client run dev
  ```
  from root folder to run only ai-service run this command.
  ```sh
  pnpm --filter ai-service run dev
  ```
---

## 11. Access the Apps

- **Web Client:** http://localhost:5173
- **Auth Service API:** http://localhost:5000
- **AI Service API:** http://localhost:8000
- **Postgres:** localhost:5432 (use a DB client with the credentials from `docker-compose.yml`)

---

## 12. Troubleshooting

- If you see `Cannot find module 'shared-types/dist/index.js'`, ensure you ran the build for shared-types and that `"noEmit": false` in `tsconfig.base.json`.
- If you get database connection errors, ensure Docker is running and the Postgres container is healthy.
- For Python errors, ensure you have the correct Python version and all dependencies installed.

---

## 13. Stopping Services

- To stop all Docker containers:
  ```sh
  docker-compose down
  ```
- To stop dev servers, use `Ctrl+C` in the terminal.

---

## 14. Additional Notes

- The **API Gateway** service is currently a placeholder and does not run by default.
- You may need to create `.env` files for local secrets (see service READMEs if present).
- For Windows users, ensure Python and Docker are in your PATH. 
