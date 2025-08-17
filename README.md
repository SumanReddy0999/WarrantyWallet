
# 🛡️ WarrantyWallet

WarrantyWallet is a full-stack monorepo designed for managing product warranties, customer interactions, and secure service workflows. It features a FastAPI-powered authentication service, a modern Vite-based web client, shared utility packages, and Docker-driven deployment infrastructure.

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18+ recommended)
- **pnpm** (v8+ recommended): [Install guide](https://pnpm.io/installation)
- **Python** (v3.10+ recommended, for ai-service)
- **Docker** (for running PostgreSQL)
- **Git**
- **Tesseract-OCR** : Required for local OCR capabilities in the AI service. Install guide. Make sure to add it
    to your system's PATH during installation.

- **Poppler**: A PDF rendering library required by the AI service for processing PDF files. Download for Windows.  
    For macOS/Linux, use Homebrew (brew install poppler) or your package manager.
### Setup Steps

1. **Clone the Repository**
   ```sh
   git clone <your-repo-url>
   cd warrantywallet-test
   ```
   ---

2. **Configure Environment**
   Create `.env` file in `services/auth-service/` with:
   ```sh
   DATABASE_URL="postgresql://postgres:warranty@localhost:5432/Warrant_wallet_v02"
   ```
   ---

3. **Start Database**
   ```sh
   docker-compose up -d
   ```
   ---

4. **Install Dependencies**
   ```sh
   pnpm install
   ```
   ---

5. **AI Service:** Create a file at services/ai-service/.env with your AI and database credentials. Update the 
   POPPLER_PATH and TESSERACT_PATH with the absolute paths to your local installations.
   ```
   # --- Generative AI Configuration ---
   GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

   # --- Database Configuration ---
   DATABASE_URL="postgresql://postgres:warranty@localhost:5432/Warrant_wallet_v02"

   # --- External Local Dependencies ---
   # Example for Windows: POPPLER_PATH="C:\\path\\to\\poppler-24.02.0\\Library\\bin"
   POPPLER_PATH="YOUR_ABSOLUTE_PATH_TO_POPPLER_BIN"

   # Example for Windows: TESSERACT_PATH="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
   TESSERACT_PATH="YOUR_ABSOLUTE_PATH_TO_TESSERACT_EXE"
   ```
   ---

6. **Set Up AI Service Python Environment**
   Create a virtual environment and install the required Python packages.

   ```
   # Navigate to the ai-service directory
   cd services/ai-service

   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

   # Install Python dependencies
   pip install -r requirements.txt

   # Navigate back to the root directory
   cd ../..
   ```

7. **Initialize Database**
   ```sh
   pnpm --filter=auth-service run db:push
   ```
   ---

8. **Build Shared Packages**
   ```sh
   pnpm --filter shared-types run build
   ```
   ---

9. **(Optional) Build All Packages**

   If you want to ensure all TypeScript is built (not just shared-types):

   ```sh
   pnpm build
   ```

---


10. **Start Development Servers**
   ```sh
   pnpm run dev
   ```

11. (If Needed) Run Services Individually

- **Auth Service** (port 5000):
  ```sh
  pnpm --filter auth-service run dev
  ```
- **AI Service** (port 8000, requires Python):
  ```sh
  cd services/ai-service
  pip install -r requirements.txt
  pnpm --filter ai-service run dev
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

## 📁 Project Structure
```sh
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
```

## 🔧 Components

### 🔐 Auth Service
- **Stack:** FastAPI, Drizzle ORM
- **Location:** services/auth-service
- **Port:** 5000
- **Environment:** .env file with JWT secret, database URL

### 🌐 Web Client
- **Stack:** Vite, React, Tailwind CSS
- **Location:** apps/web-client
- **Port:** 5173
- **Features:** Protected routes, service pages, toast notifications

### 🤖 AI RAG Service
- **Stack:** Python, FastAPI, LangChain
- **Location:** services/ai-service
- **Port:** 8000
- **Description:** Processes uploaded warranty documents (PDFs, images) using a hybrid local OCR and LLM-vision 
    approach. It extracts, validates, and categorizes warranty data, then populates the relational and vector database to be used by a RAG chatbot.
- **Key Dependencies:** Tesseract, Poppler, Google Generative AI

## 🛠️ Development Tools
- ESLint, Prettier for code formatting
- Depcheck, Knip for dependency management
- Jest for testing
- Git hooks via Husky (optional)
- Platform consistency via .gitattributes and scoped .gitignore

## ⚠️ Troubleshooting

- **Module not found:** If you see `Cannot find module 'shared-types/dist/index.js'`, rebuild shared-types
- **Database errors:** Ensure Docker is running and Postgres container is healthy
- **Python errors:** Verify correct Python version and dependencies
- **TypeScript errors:** Check for unused imports or missing types
- **Node.js types:** If process is not found in drizzle.config.ts, run:
  ```sh
  pnpm add -Dw @types/node
  ```

## 🛑 Stopping Services
- Stop Docker: `docker-compose down`
- Stop dev servers: `Ctrl+C` in terminal

## 📄 License & Governance
This project follows best practices for internal ownership. See .github/CODEOWNERS for maintainers.
