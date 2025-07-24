
# 🛡️ WarrantyWallet

WarrantyWallet is a full-stack monorepo designed for managing product warranties, customer interactions, and secure service workflows. It features a FastAPI-powered authentication service, a modern Vite-based web client, shared utility packages, and Docker-driven deployment infrastructure.

---

## 📁 Project Structure

WarrantyWallet/
├── apps/
│   └── web-client/         # Frontend (Vite + React + Tailwind)
├── services/
│   ├── auth-service/       # FastAPI Auth backend with Drizzle ORM
│   └── ai-service/         # Optional Python microservice
├── packages/
│   ├── shared-types/       # Shared type definitions
│   └── ui-core/            # UI design system components
├── infra/
│   └── terraform/          # Infrastructure automation
├── docs/                   # ADRs, Runbooks
├── docker-compose.yml
└── turbo.json              # Turborepo config


🔐 Auth Service
Stack: FastAPI, Drizzle ORM

Location: services/auth-service

Environment: .env file with JWT secret, database URL

🌐 Web Client
Stack: Vite, React, Tailwind CSS

Location: apps/web-client

Features: Protected routes, service pages, toast notifications

🧪 Development Tools
ESLint, Prettier, Depcheck, Knip, Jest

Git hooks via Husky (optional)

.gitattributes and scoped .gitignore for platform consistency

📄 License & Governance
This project follows best practices for internal ownership. See .github/CODEOWNERS for maintainers.
