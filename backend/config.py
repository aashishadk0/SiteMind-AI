from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

STRUCTURED_DATA_DIR = DATA_DIR / "structured"

CHROMA_DIR = DATA_DIR / "chroma"

UPLOAD_DIR = DATA_DIR / "uploads"

DATABASE_PATH = DATA_DIR / "app.db"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLAMA_PARSE_KEY = os.getenv("LLAMA_PARSE_KEY")

OLLAMA_URL = "http://localhost:11434"