
# 🛡️ WarrantyWallet

WarrantyWallet is a full-stack monorepo designed for managing product warranties, customer interactions, and secure service workflows. It features a FastAPI-powered authentication service, a modern Vite-based web client, shared utility packages, and Docker-driven deployment infrastructure.

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v18+ recommended)
- **pnpm** (v8+ recommended): [Install guide](https://pnpm.io/installation)
- **Python** (v3.11+ recommended, for ai-service)
  - The project uses Python 3.13.5 (specified in `.python-version`)
  - Virtual environment is configured in `services/ai-service/venv/`
- **Docker** (for running PostgreSQL)
- **Git**
- **Tesseract-OCR**: Required for local OCR capabilities in the AI service. Install guide. Make sure to add it
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
   docker compose up -d
   ```
   ---

4. **Vector Extension** Open query tool for the database in pgadmin4 and run the command
   ```sh
   CREATE EXTENSION vector;

   ---

5. **Initialize Database**
   ```sh
   pnpm --filter=auth-service run db:push
   ```
   ---

6. **Install Dependencies**
   ```sh
   pnpm install
   ```
   ---

7. **Verify External Dependencies** Run these commands from your terminal to ensure Tesseract and Poppler are correctly installed and accessible.

Verify Tesseract:

```

tesseract --version
```
✅ Success: You'll see a version number (e.g., tesseract 5.3.3).

❌ Failure: You'll see an error like 'tesseract' is not recognized.... If this happens, you must add your Tesseract installation folder to your system's PATH environment variable.

Verify Poppler:

```

# The 'pdftoppm' command is part of the Poppler suite
pdftoppm -v
```
✅ Success: You'll see version information (e.g., pdftoppm version 24.02.0).

❌ Failure: You'll see a command not found error. If this happens, add the bin folder of your Poppler installation to your system's PATH.

8. **AI Service:** Create a file at services/ai-service/.env with your AI and database credentials. Update the 
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

9. **Set Up AI Service Python Environment**
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

   **IDE Configuration**: The project includes VS Code/Cursor configuration files (`.vscode/settings.json`, `.vscode/launch.json`) that automatically configure the Python interpreter to use the AI service virtual environment. This ensures proper IntelliSense and debugging capabilities.
   ---

10. **Build Shared Packages**
   ```sh
   pnpm --filter shared-types run build
   ```
   ---

11. **Start Development Servers**
   ```sh
   pnpm run dev
   ```

12. (If Needed) Run Services Individually

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
- **Description:** Provides two main functionalities:
 1) A RAG ingestion pipeline that processes uploaded documents and populates a vector store. 
 2) A RAG chat pipeline that answers questions based on the ingested documents.
- **Key Dependencies:** Tesseract, Poppler, Google Generative AI

## 🛠️ Development Tools
- ESLint, Prettier for code formatting
- Depcheck, Knip for dependency management
- Jest for testing
- Git hooks via Husky (optional)
- Platform consistency via .gitattributes and scoped .gitignore
- **Python Development**: Pyright for type checking, configured in `services/ai-service/pyrightconfig.json`
- **IDE Configuration**: VS Code/Cursor settings for seamless Python and TypeScript development

## ⚠️ Troubleshooting

- **Module not found:** If you see Cannot find module 'shared-types/dist/index.js', run pnpm --filter shared-types run build.
- **Database errors:** Ensure your Docker container is running and that you have run the db:push command.
-**AI-service errors:** If you encounter errors related to Tesseract or Poppler, double-check that they are installed and that their paths are correctly set in both your System PATH and the ai-service/.env file. Run the verification commands from Step 5 of the setup guide to confirm.
- **Python import errors in VS Code:** Ensure your IDE is using the correct Python interpreter from services/ai-service/venv/.
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
