import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- API Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please add it.")

# --- Database Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file.")

# --- Embedding Model Configuration ---
EMBEDDING_MODEL_NAME = "models/embedding-001"
EMBEDDING_DIMENSION = 768

# --- Text Splitting Configuration ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# --- File Handling ---
TEMP_UPLOAD_DIR = "temp_uploads"

# --- External Dependencies Configuration ---
# Paths required for local document processing with 'unstructured'
POPPLER_PATH = os.getenv("POPPLER_PATH")
TESSERACT_PATH = os.getenv("TESSERACT_PATH")