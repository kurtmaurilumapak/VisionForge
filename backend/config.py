import os

# Configuration settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
RELOAD = os.getenv("RELOAD", "true").lower() == "true"

# CORS settings
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Alternative dev server
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000"
]

# API settings
API_TITLE = "VisionForge API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Backend API for VisionForge image processing application"



