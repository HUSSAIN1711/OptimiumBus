"""
Development server runner for OptimumBus API

This script provides an easy way to run the FastAPI development server
with proper configuration for local development.
"""

import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
        access_log=True
    )
