# OptimumBus Project Context & AI Workspace Guide

## 🎯 Project Overview
**OptimumBus** is a full-stack web application for bus route optimization. Users can define bus stops on an interactive map, specify the number of available buses, and receive optimized routes based on travel time and passenger demand using advanced clustering and pathfinding algorithms.

## 🏗️ Tech Stack & Architecture
- **Frontend**: React 19.2.0 + TypeScript with Google Maps JavaScript API
- **Backend**: Python 3.13 + FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL 17+ with PostGIS extension for geospatial operations
- **GIS/Data Processing**: OSMnx, NetworkX, Pandas, GeoPy for road network analysis
- **Optimization**: K-Means clustering, nearest-neighbor heuristics, VRP algorithms
- **API Integration**: Google Maps JavaScript API v3 (weekly release)
- **Development**: pytest for testing, Alembic for migrations

## 🤖 AI Workspace Context

### Current Project Status
- **Development Phase**: Production-ready MVP with full-stack implementation
- **Backend**: Complete FastAPI application with geospatial capabilities
- **Frontend**: React application with Google Maps integration
- **Database**: PostgreSQL with PostGIS for spatial operations
- **Testing**: Comprehensive test suite with pytest
- **Documentation**: Developer-focused README and AI-focused context

### Key Technical Decisions Made
1. **Google Maps API**: Using `@googlemaps/js-api-loader` v2.0.1+ with `setOptions()` and `importLibrary()` pattern
2. **Database**: PostgreSQL with PostGIS for advanced geospatial queries and coordinate snapping
3. **Backend Architecture**: Modular FastAPI structure with separate concerns (api/, core/, models/, db/)
4. **Frontend Architecture**: Component-based React with TypeScript for type safety
5. **Optimization Algorithm**: K-Means clustering + nearest-neighbor heuristic for route optimization

### Environment Variables Required
- **Single File**: All environment variables are managed in `.env.local` (main directory)
- **Frontend**: `REACT_APP_GOOGLE_MAPS_API_KEY` (Google Maps JavaScript API)
- **Backend**: Database connection variables (DATABASE_URL, POSTGRES_*, etc.)
- **Location**: `/Users/hmahuvaw/Coding/OptimumBus/OptimiumBus/.env.local`

### Common AI Tasks in This Workspace
1. **Adding new API endpoints**: Follow the pattern in `backend/app/api/`
2. **Database model changes**: Update SQLAlchemy models in `backend/app/models/`
3. **Frontend component updates**: Modify React components in `frontend/src/components/`
4. **Testing**: Add tests in `tests/` directory following existing patterns
5. **Documentation**: Update both README.md (developer) and context.md (AI) as needed

## ✅ COMPLETED PHASES

### Phase 1: Backend Setup & API Foundation ✅ COMPLETE

**What We Accomplished:**
- ✅ Created modular FastAPI project structure (`app/api/`, `app/core/`, `app/models/`, `app/db/`)
- ✅ Set up comprehensive dependencies in `requirements.txt` (FastAPI, SQLAlchemy, PostgreSQL, geospatial libraries)
- ✅ Implemented secure configuration management with Pydantic Settings and environment variables
- ✅ Created robust database connection system with SQLAlchemy and PostgreSQL support
- ✅ Built comprehensive BusStop data models:
  - SQLAlchemy model with UUID primary key, geospatial fields (lat/lng), demand weighting
  - Pydantic schemas for API validation (Create, Update, Response, ListResponse)
- ✅ Set up CORS middleware for frontend communication
- ✅ Created development server runner and comprehensive documentation

**Key Files Created:**
```
OptimiumBus/
├── backend/
│   ├── app/
│   │   ├── api/__init__.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py          # Environment configuration
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   └── database.py        # Database connection & session management
│   │   └── models/
│   │       ├── __init__.py
│   │       └── bus_stop.py        # BusStop SQLAlchemy & Pydantic models
│   ├── main.py                    # FastAPI application entry point
│   ├── run.py                     # Development server runner
│   ├── requirements.txt           # Python dependencies
│   ├── env.example               # Environment variables template
│   └── README.md                 # Comprehensive setup documentation
└── context.md                    # This progress tracker
```

**Current Status:** Backend foundation is complete and ready for testing. The API can be started with `python run.py` and will be available at http://localhost:8000 with interactive docs at http://localhost:8000/docs.

---

## 🚧 UPCOMING PHASES

### Phase 2: Geospatial Data & Road Network ✅ COMPLETE

**What We Accomplished:**
- ✅ Created comprehensive bus stops API router with full CRUD operations
- ✅ Implemented database session dependency injection with proper error handling
- ✅ Built OSMnx integration for downloading and caching road network data
- ✅ Added coordinate snapping functionality (lat/lng → nearest road intersection)
- ✅ Enhanced BusStop model with PostGIS geometry columns
- ✅ Created advanced geospatial query utilities using PostGIS
- ✅ Added road network management endpoints
- ✅ Implemented density analysis and nearby stops functionality

**Key Files Created:**
```
OptimiumBus/backend/
├── app/
│   ├── api/
│   │   └── bus_stops.py          # Complete CRUD API with geospatial features
│   ├── core/
│   │   ├── osmnx_utils.py        # OSMnx road network integration
│   │   └── geospatial_utils.py   # PostGIS geospatial operations
│   └── models/
│       └── bus_stop.py           # Enhanced with PostGIS geometry column
├── init_db.py                    # Database initialization script
└── main.py                       # Updated with API router integration
```

**API Endpoints Available:**
- `GET /api/v1/stops/` - List all bus stops with pagination and sorting
- `POST /api/v1/stops/` - Create new bus stop with coordinate snapping
- `GET /api/v1/stops/{id}` - Get specific bus stop
- `PUT /api/v1/stops/{id}` - Update bus stop
- `DELETE /api/v1/stops/{id}` - Delete bus stop
- `GET /api/v1/stops/nearby/` - Find nearby stops using PostGIS
- `GET /api/v1/stops/density-analysis/` - Analyze stop density
- `GET /api/v1/stops/road-network/info` - Get road network information
- `POST /api/v1/stops/road-network/refresh` - Refresh road network data

**Current Status:** Phase 2 is complete and ready for testing. The API provides full bus stop management with real-world road network integration and advanced geospatial capabilities.

### Phase 3: Core Optimization Algorithm ✅ COMPLETE

**What We Accomplished:**
- ✅ Implemented KMeans clustering to group bus stops by number of buses
- ✅ Added nearest-neighbor heuristic for intra-cluster route ordering
- ✅ Implemented road-network-aware travel-time estimates using OSMnx/NetworkX, with robust fallbacks
- ✅ Created `/api/v1/optimize/routes` endpoint to run end-to-end optimization
- ✅ Standardized response shape with ordered stop IDs and coordinates for each bus/cluster

**Key Files Created:**
```
OptimiumBus/backend/app/
├── core/
│   └── optimization.py          # Clustering + route ordering utilities
└── api/
    └── optimization.py          # /optimize/routes endpoint
```

**API Endpoints Available (Phase 3):**
- `POST /api/v1/optimize/routes?num_buses=N` – Returns `routes` array, each with:
  - `bus_index`: index of the bus/cluster
  - `stop_ids`: ordered list of stop UUIDs
  - `coordinates`: ordered list of `{ lat, lng }`

**Current Status:** Phase 3 is complete. We can now compute optimized routes from real stops using clustering and a TSP heuristic.

### Phase 4: Frontend Development with React & Google Maps ✅ COMPLETE

**What We Accomplished:**
- ✅ Created React TypeScript application with Google Maps integration
- ✅ Built interactive map component with click-to-add functionality
- ✅ Implemented bus stop management (create, edit, delete)
- ✅ Added route visualization with colored polylines
- ✅ Created optimization controls UI for multi-bus routing
- ✅ Integrated with backend API for real-time data

**Key Files Created:**
```
OptimiumBus/frontend/
├── src/
│   ├── components/
│   │   ├── MapComponent.tsx          # Google Maps with click handlers
│   │   ├── BusStopForm.tsx          # Add/edit bus stop form
│   │   ├── BusStopList.tsx          # List and manage stops
│   │   └── OptimizationControls.tsx # Route optimization UI
│   ├── services/
│   │   └── api.ts                   # Backend API client
│   ├── types/
│   │   └── index.ts                 # TypeScript interfaces
│   ├── App.tsx                      # Main application
│   └── App.css                      # Responsive styling
├── env.example                      # Google Maps API key template
└── README.md                        # Setup and usage guide
```

**Features Available:**
- 🗺️ **Interactive Map**: Click to add bus stops with coordinate snapping
- 🚌 **Stop Management**: Full CRUD operations for bus stops
- 🎯 **Route Optimization**: Multi-bus route optimization with clustering
- 📍 **Real-time Visualization**: Colored polylines showing optimized routes
- 📱 **Responsive Design**: Works on desktop and mobile devices

**Current Status:** Phase 4 is complete. The full-stack application is ready for use with a modern React frontend and comprehensive backend API.