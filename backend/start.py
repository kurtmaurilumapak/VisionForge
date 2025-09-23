#!/usr/bin/env python3
"""
Startup script for VisionForge backend
"""
import uvicorn
# Force inclusion of key deps when freezing with PyInstaller
try:  # noqa: F401
    import fastapi  # type: ignore
    import starlette  # type: ignore
    import pydantic  # type: ignore
except Exception:
    # If running in a normal python env, this import is fine; if missing, the app will fail later anyway.
    pass
import os
try:
    from dotenv import load_dotenv
except Exception:  # allow running without python-dotenv when frozen
    def load_dotenv():
        return None

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    # Honor Electron override to prevent orphan processes
    reload_env = os.getenv("RELOAD", "true")
    is_electron = os.getenv("ELECTRON") == "1"
    reload = False if is_electron else reload_env.lower() == "true"
    
    print(f"Starting VisionForge API server on {host}:{port}")
    print(f"Reload mode: {reload}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )



