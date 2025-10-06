"""
OptimumBus API - Main Application Entry Point

This is the main FastAPI application that serves as the backend for the
Bus Route Optimization system. It provides RESTful APIs for managing
bus stops and optimizing routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    description="API for Bus Route Optimization using geospatial data and machine learning",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc"  # ReDoc documentation
)

# Configure CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint - Simple health check and API information
    
    Returns:
        dict: Basic API information and status
    """
    return {
        "message": "Welcome to OptimumBus API!",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "description": "Bus Route Optimization API with geospatial intelligence"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers
    
    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "service": "optimumbus-api",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the application with uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,  # Auto-reload on code changes in development
        log_level="info"
    )
