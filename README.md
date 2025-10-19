# OptimumBus - Bus Route Optimization System

A full-stack web application for optimizing bus routes using geospatial data, machine learning algorithms, and real-time mapping. Users can define bus stops on an interactive map and receive optimized multi-bus routes based on travel time and passenger demand.

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** with pip
- **PostgreSQL 17+** with PostGIS extension
- **Node.js 18+** with npm
- **Google Maps API Key** (for frontend mapping)
- **Git** (for version control)

### Installation

#### 1. Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   
   # Verify Python version (should be 3.13+)
   python --version
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # The .env.local file is already created in the main directory
   # Backend automatically loads from ../.env.local
   # Edit .env.local with your database credentials and API keys
   nano .env.local  # or use your preferred editor
   ```

5. **Set up PostgreSQL database:**
   ```sql
   -- Connect to PostgreSQL and create database
   CREATE DATABASE optimumbus_db;
   
   -- Connect to the new database and enable PostGIS
   \c optimumbus_db;
   CREATE EXTENSION postgis;
   ```

6. **Initialize the database:**
   ```bash
   python init_db.py
   ```

7. **Start the backend server:**
   ```bash
   python run.py
   ```

#### 2. Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   # The .env.local file is already created in the main directory
   # A symlink has been created in frontend/ to use the same file
   # Edit .env.local with your Google Maps API key
   nano .env.local  # or use your preferred editor
   ```

4. **Start the development server:**
   ```bash
   npm start
   ```

### 🎯 Application URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
OptimumBus/
├── .env.local                    # Unified environment configuration
├── backend/
│   ├── app/
│   │   ├── api/                 # API route handlers
│   │   ├── core/                # Core configuration and settings
│   │   ├── db/                  # Database connection and session management
│   │   └── models/              # SQLAlchemy models and Pydantic schemas
│   ├── main.py                  # FastAPI application entry point
│   ├── run.py                   # Development server runner
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── services/            # API client
│   │   └── types/               # TypeScript interfaces
│   ├── package.json             # Node.js dependencies
│   └── .env.local -> ../.env.local  # Symlink to main .env.local
└── README.md                    # This file
```

## 🔑 Required API Keys & Environment Variables

### Single Environment File Setup

**All environment variables are managed in one file: `.env.local` (in the main OptimumBus directory)**

### Google Maps API Key (Required for Frontend)

1. **Get a Google Maps API Key:**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - **Important**: Restrict your API key to prevent unauthorized usage

2. **Enable Required APIs:**
   - Maps JavaScript API
   - Places API (optional, for enhanced location features)

### Environment Configuration

**Edit `.env.local` in the main directory:**
```env
# =============================================================================
# BACKEND CONFIGURATION
# =============================================================================

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

# CORS Configuration (for frontend communication)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# =============================================================================
# FRONTEND CONFIGURATION
# =============================================================================

# Google Maps API Key
REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### Environment Setup Checklist

- [ ] Google Maps API key obtained and restricted
- [ ] `.env.local` file edited with your credentials
- [ ] PostgreSQL database created with PostGIS extension
- [ ] Database connection tested

## 🚌 How to Use OptimumBus

### 1. Adding Bus Stops
- Click anywhere on the map to add a new bus stop
- Fill in the stop details (name, description, demand weight)
- Stops are automatically snapped to the nearest road intersection

### 2. Optimizing Routes
- Enter the number of available buses
- Click "Optimize Routes" to generate optimized routes
- View colored polylines showing each bus route
- Routes are optimized using K-Means clustering and nearest-neighbor algorithms

### 3. Managing Stops
- View all stops in the sidebar
- Edit or delete existing stops
- Stops are stored in PostgreSQL with PostGIS for geospatial operations

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

---

## 🔧 Phase 1 Setup Instructions

**Complete setup guide to get Phase 1 running:**

### **Step 1: Python Environment Setup**

1. **Navigate to backend directory:**
   ```bash
   cd /Users/hmahuvaw/Coding/OptimumBus/OptimiumBus/backend
   ```

2. **Create Python virtual environment:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   
   # Verify activation (should show (venv) in terminal prompt)
   which python  # Should point to venv/bin/python
   ```

3. **Install Python dependencies:**
   ```bash
   # Upgrade pip first
   pip install --upgrade pip
   
   # Install all required packages
   pip install -r requirements.txt
   
   # Verify installation
   pip list | grep fastapi  # Should show FastAPI installed
   ```

### **Step 2: PostgreSQL & PostGIS Setup**

1. **Install PostgreSQL (if not already installed):**
   ```bash
   # On macOS with Homebrew
   brew install postgresql@17
   brew services start postgresql@17
   
   # On Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   
   # On Windows: Download from https://www.postgresql.org/download/windows/
   ```

2. **Create database and user:**
   ```bash
   # Connect to PostgreSQL as superuser
   sudo -u postgres psql  # On Linux
   # or
   psql postgres  # On macOS/Windows
   ```

3. **Run these SQL commands:**
   ```sql
   -- Create database
   CREATE DATABASE optimumbus_db;
   
   -- Create user (optional, or use existing user)
   CREATE USER optimumbus_user WITH PASSWORD 'your_secure_password';
   
   -- Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE optimumbus_db TO optimumbus_user;
   
   -- Connect to the new database
   \c optimumbus_db;
   
   -- Install PostGIS extension
   CREATE EXTENSION postgis;
   
   -- Verify PostGIS installation
   SELECT PostGIS_Version();
   
   -- Exit PostgreSQL
   \q
   ```

### **Step 3: Environment Configuration**

1. **Create environment file:**
   ```bash
   # Copy the example file
   cp env.example .env
   ```

2. **Edit .env file with your database credentials:**
   ```bash
   # Open .env file in your editor
   nano .env  # or use your preferred editor
   ```

3. **Update these variables in .env:**
   ```env
   # Database Configuration - UPDATE THESE VALUES
   DATABASE_URL=postgresql://optimumbus_user:your_secure_password@localhost:5432/optimumbus_db
   POSTGRES_USER=optimumbus_user
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_DB=optimumbus_db
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   
   # Application Configuration
   APP_NAME=OptimumBus API
   DEBUG=True
   API_V1_STR=/api/v1
   
   # CORS Configuration (for future frontend)
   ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   ```

### **Step 4: Test Phase 1 Setup**

1. **Start the FastAPI server:**
   ```bash
   # Make sure virtual environment is activated
   source venv/bin/activate  # If not already active
   
   # Start the server
   python run.py
   ```

2. **Verify everything is working:**
   - ✅ Server should start without errors
   - ✅ Should show: "Uvicorn running on http://0.0.0.0:8000"
   - ✅ Visit http://localhost:8000 - should show welcome message
   - ✅ Visit http://localhost:8000/docs - should show Swagger UI
   - ✅ Visit http://localhost:8000/health - should show health status

3. **Test database connection:**
   ```bash
   # In another terminal, test database connection
   python -c "
   from app.db.database import engine
   from sqlalchemy import text
   with engine.connect() as conn:
       result = conn.execute(text('SELECT version()'))
       print('Database connected:', result.fetchone()[0])
   "
   ```

### **Troubleshooting Common Issues:**

**Database Connection Error:**
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql  # On macOS
sudo systemctl status postgresql     # On Linux

# Check if database exists
psql -l | grep optimumbus_db
```

**Python Import Errors:**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

**Port Already in Use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # On macOS/Linux
```

### **Phase 1 Verification Checklist:**
- [ ] Python virtual environment created and activated
- [ ] All dependencies installed successfully
- [ ] PostgreSQL running and accessible
- [ ] Database `optimumbus_db` created
- [ ] PostGIS extension installed
- [ ] `.env` file configured with correct credentials
- [ ] FastAPI server starts without errors
- [ ] API documentation loads at http://localhost:8000/docs
- [ ] Database connection test passes


## 🔧 Phase 2 Setup Instructions (Geospatial & Road Network)

1) Ensure DB and PostGIS are ready (if not already):
```bash
psql -U postgres -c "CREATE DATABASE optimumbus_db;"
psql -U postgres -d optimumbus_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

2) Initialize tables and spatial indexes:
```bash
cd /Users/hmahuvaw/Coding/OptimumBus/OptimiumBus/backend
python init_db.py
```

3) Run the backend API:
```bash
python run.py
# Swagger: http://localhost:8000/docs
```

4) Optional: Warm up OSMnx cache (Irvine default):
```bash
curl -X GET http://localhost:8000/api/v1/stops/road-network/info
```

5) Create a bus stop (snapping on by default; you can disable via snap_to_road=false):
```bash
curl -X POST "http://localhost:8000/api/v1/stops/?snap_to_road=true" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Demo Stop",
    "description": "Test",
    "latitude": 33.6846,
    "longitude": -117.8265,
    "demand_weight": 0.5
  }'
```

---

## 🔧 Phase 3 Setup Instructions (Optimization API)

1) Start the backend (if not running):
```bash
cd /Users/hmahuvaw/Coding/OptimumBus/OptimiumBus/backend
python run.py
```

2) Add several bus stops (see Phase 2 step 5) so clusters can form.

3) Run optimization for N buses (example: 2):
```bash
curl -X POST "http://localhost:8000/api/v1/optimize/routes?num_buses=2"
```

4) Response schema highlights:
- routes: array of { bus_index, stop_ids[], coordinates[] }

---

## 🔧 Phase 4 Setup Instructions (React Frontend)

1) Install and run the frontend:
```bash
cd /Users/hmahuvaw/Coding/OptimumBus/OptimiumBus/frontend
npm install
cp env.example .env  # add your Google Maps API key
npm start
```

2) Ensure backend CORS allows http://localhost:3000 (configured in backend settings).

3) Use the UI:
- Click on the map to add stops, then fill details in the form
- Use the optimization panel to enter number of buses and submit
- View colored polylines for each route

---

## 🧪 Testing Foundation (Phase 1) – Setup & Configuration ✅

**What We Added:**
- ✅ `tests/` directory with `__init__.py`
- ✅ `pytest.ini` at project root (pythonpath set to `OptimiumBus/backend`)
- ✅ `tests/conftest.py` with fixtures:
  - Session-scoped setup/teardown that creates and drops tables in a separate test DB
  - `db_session` fixture providing a SQLAlchemy session bound to the test DB
  - `client` fixture providing a FastAPI `TestClient` that overrides `get_db` to use the test session

**Environment:**
- Set `TEST_DATABASE_URL` (optional). Defaults to development URL with db name replaced by `optimumbus_db_test`.
  - Example: `TEST_DATABASE_URL=postgresql://user:pass@localhost:5432/optimumbus_db_test`

**Commands:**
```bash
cd /Users/hmahuvaw/Coding/OptimumBus/OptimiumBus
pip install pytest

# Ensure the test database exists and PostGIS is enabled
psql -U postgres -c "CREATE DATABASE optimumbus_db_test;"
psql -U postgres -d optimumbus_db_test -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# Run tests
pytest
```

**Why This Setup:**
- Separate test database avoids polluting development data
- Fixtures in `conftest.py` centralize setup/teardown and dependency override
- `TestClient` runs real HTTP requests against the app using the test session

Next Testing Steps:
- Phase 2: Add API tests for `/stops/` (happy and sad paths)
- Phase 3: Add pure unit tests for optimization utilities (no DB/API)

---

## 🧪 Testing (Phase 2) – API Endpoint Tests ✅

**What We Added:**
- ✅ `tests/test_api_stops.py` with two tests for `/stops/`:
  - `test_create_bus_stop_success` – verifies 201 Created and response fields
  - `test_create_bus_stop_invalid_data` – verifies 422 on validation error
- Tests pass `snap_to_road=False` to avoid external OSMnx calls for determinism

**Run Tests:**
```bash
cd /Users/hmahuvaw/Coding/OptimumBus/OptimiumBus
pytest -q tests/test_api_stops.py
```

**Why:**
- Ensures CRUD create endpoint is correct for both happy/sad paths
- Keeps tests fast and reliable by avoiding network-bound snapping

---

## 🧪 Testing (Phase 3) – Core Logic Unit Tests ✅

**What We Added:**
- ✅ `app/core/graph_utils.py` with a pure `snap_to_nearest_node(graph, lat, lng)` using haversine distance
- ✅ `tests/test_optimization_logic.py` unit test that builds a tiny NetworkX graph and asserts the nearest node ID

**Run Tests:**
```bash
cd /Users/hmahuvaw/Coding/OptimumBus/OptimiumBus
pytest -q tests/test_optimization_logic.py
```

**Why:**
- Tests algorithmic logic in isolation (no API, no DB, no network)
- Fast, deterministic verification of nearest-node snapping