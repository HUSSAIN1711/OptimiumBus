# OptimumBus Backend API

A FastAPI-based backend for bus route optimization using geospatial data and machine learning algorithms.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+ with PostGIS extension
- pip (Python package manager)

### Installation

1. **Clone and navigate to the backend directory:**
   ```bash
   cd /Users/hmahuvaw/Coding/OptimumBus/backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

5. **Set up PostgreSQL database:**
   ```sql
   -- Connect to PostgreSQL and create database
   CREATE DATABASE optimumbus_db;
   
   -- Connect to the new database and enable PostGIS
   \c optimumbus_db;
   CREATE EXTENSION postgis;
   ```

6. **Run the application:**
   ```bash
   python run.py
   # or
   uvicorn main:app --reload
   ```

The API will be available at:
- **API Base URL:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/           # API route handlers
│   ├── core/          # Core configuration and settings
│   ├── db/            # Database connection and session management
│   └── models/        # SQLAlchemy models and Pydantic schemas
├── main.py            # FastAPI application entry point
├── run.py             # Development server runner
├── requirements.txt   # Python dependencies
└── env.example        # Environment variables template
```

## 🔧 Configuration

The application uses environment variables for configuration. Copy `env.example` to `.env` and modify the values:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/optimumbus_db
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=optimumbus_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Application Configuration
APP_NAME=OptimumBus API
DEBUG=True
API_V1_STR=/api/v1

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 🗄️ Database Models

### BusStop Model

The `BusStop` model represents bus stops with the following fields:

- **id**: UUID primary key
- **name**: Stop name (required)
- **description**: Optional description
- **latitude**: Latitude coordinate (-90 to 90)
- **longitude**: Longitude coordinate (-180 to 180)
- **demand_weight**: Passenger demand weight (0.0 to 1.0)
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

## 🛠️ Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Migrations

For production deployments, use Alembic for database migrations:

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔍 Key Features

- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **PostgreSQL + PostGIS**: Robust database with geospatial capabilities
- **Pydantic Validation**: Automatic request/response validation and serialization
- **CORS Support**: Ready for frontend integration
- **Environment Configuration**: Secure configuration management
- **Type Hints**: Full type safety throughout the codebase

## 🚧 Next Steps

This completes Phase 1 of the OptimumBus project. The next phases will add:

- **Phase 2**: Geospatial data integration with OSMnx
- **Phase 3**: Route optimization algorithms
- **Phase 4**: React frontend with Google Maps

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error:**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env`
   - Verify PostGIS extension is installed

2. **Import Errors:**
   - Ensure virtual environment is activated
   - Check all dependencies are installed: `pip install -r requirements.txt`

3. **Port Already in Use:**
   - Change the port in `run.py` or kill the process using port 8000

### Getting Help

- Check the FastAPI documentation: https://fastapi.tiangolo.com/
- Review the interactive API docs at http://localhost:8000/docs
- Check the application logs for detailed error messages
