# OptimumBus - Code Structure Documentation

## Overview

OptimumBus is a full-stack web application for optimizing bus routes using geospatial data, machine learning algorithms, and real-time mapping. The system consists of a FastAPI backend with PostgreSQL/PostGIS database and a React TypeScript frontend with Google Maps integration.

## Project Architecture

```
OptimumBus/
├── backend/                 # FastAPI Python backend
├── frontend/                # React TypeScript frontend  
├── tests/                   # Test suite
├── road_networks/           # Shared road network data
├── .env.local              # Environment configuration
├── README.md               # Project documentation
├── pytest.ini             # Test configuration
└── context.md              # Project context
```

---

## Backend Structure (`/backend/`)

### Core Application (`/backend/app/`)

#### **Configuration (`/backend/app/core/`)**

**`config.py`** - Application Settings Management
- **Purpose**: Centralized configuration using Pydantic Settings
- **Key Features**:
  - Loads environment variables from `.env.local`
  - Database connection settings (PostgreSQL with PostGIS)
  - CORS configuration for frontend communication
  - Application metadata (name, version, debug mode)
- **Environment Variables**:
  - `DATABASE_URL`: PostgreSQL connection string
  - `ALLOWED_ORIGINS`: CORS allowed origins for frontend
  - `DEBUG`: Development mode flag
- **Usage**: Imported throughout the application for consistent configuration

**`database.py`** - Database Connection Management
- **Purpose**: SQLAlchemy database engine and session management
- **Key Components**:
  - `engine`: SQLAlchemy engine with connection pooling
  - `SessionLocal`: Database session factory
  - `Base`: Declarative base for SQLAlchemy models
  - `get_db()`: Dependency injection for FastAPI endpoints
- **Features**:
  - Connection pooling with health checks
  - Automatic session cleanup
  - Support for PostgreSQL with PostGIS extensions

**`optimization.py`** - Route Optimization Algorithms
- **Purpose**: Core optimization logic for bus route planning
- **Key Functions**:
  - `cluster_stops_kmeans()`: Groups bus stops using K-Means clustering
  - `order_stops_nearest_neighbor()`: Orders stops within clusters using nearest-neighbor heuristic
  - `optimize_routes()`: Main optimization function that coordinates the process
  - `haversine_meters()`: Calculates distance between geographic coordinates
- **Algorithm Flow**:
  1. Cluster bus stops into N groups (where N = number of buses)
  2. For each cluster, order stops using nearest-neighbor algorithm
  3. Return optimized routes with stop sequences and coordinates
- **Fallback Strategy**: Uses haversine distance when road network data is unavailable

**`osmnx_utils.py`** - OpenStreetMap Road Network Integration
- **Purpose**: Downloads and manages OpenStreetMap road network data
- **Key Classes**:
  - `RoadNetworkManager`: Manages road network data for specific geographic areas
- **Key Functions**:
  - `get_road_network()`: Downloads and caches road network data
  - `snap_coordinates_to_road_network()`: Snaps coordinates to nearest road intersections
  - `get_road_network_manager()`: Singleton pattern for network manager
- **Caching**: Stores downloaded networks as pickle files in `road_networks/` directory
- **Geographic Focus**: Defaults to Irvine, California, USA

**`geospatial_utils.py`** - PostGIS Geospatial Operations
- **Purpose**: Advanced geospatial queries using PostGIS
- **Key Functions**:
  - `find_stops_within_radius()`: Finds bus stops within specified radius
  - `get_stop_density_analysis()`: Analyzes stop density in geographic areas
- **Features**: Uses PostGIS ST_DWithin for accurate distance calculations

**`graph_utils.py`** - NetworkX Graph Utilities
- **Purpose**: Pure graph algorithms without external dependencies
- **Key Functions**:
  - `snap_to_nearest_node()`: Finds nearest node in NetworkX graph using haversine distance
- **Usage**: Fallback for road network operations when OSMnx is unavailable

#### **Database Models (`/backend/app/models/`)**

**`bus_stop.py`** - Bus Stop Data Models
- **SQLAlchemy Model**: `BusStop` class representing database table
  - **Fields**:
    - `id`: UUID primary key
    - `name`: Stop name (required, indexed)
    - `description`: Optional description
    - `latitude`/`longitude`: Geographic coordinates (indexed)
    - `geometry`: PostGIS POINT geometry (SRID 4326)
    - `demand_weight`: Passenger demand weight (0.0-1.0)
    - `created_at`/`updated_at`: Timestamps
- **Pydantic Schemas**:
  - `BusStopBase`: Common fields for all operations
  - `BusStopCreate`: Schema for creating new stops
  - `BusStopUpdate`: Schema for updating existing stops
  - `BusStopResponse`: Schema for API responses
  - `BusStopListResponse`: Schema for paginated stop lists
- **Validation**: Coordinate range validation, field length limits

#### **API Endpoints (`/backend/app/api/`)**

**`bus_stops.py`** - Bus Stop CRUD API
- **Purpose**: RESTful API for bus stop management
- **Endpoints**:
  - `GET /stops/`: List all stops with pagination and sorting
  - `GET /stops/{stop_id}`: Get specific stop by ID
  - `POST /stops/`: Create new stop with optional coordinate snapping
  - `PUT /stops/{stop_id}`: Update existing stop
  - `DELETE /stops/{stop_id}`: Delete stop
  - `GET /stops/nearby/`: Find stops within radius using PostGIS
  - `GET /stops/density-analysis/`: Analyze stop density in area
  - `GET /stops/road-network/info`: Get road network statistics
  - `POST /stops/road-network/refresh`: Force refresh road network data
- **Features**:
  - Automatic coordinate snapping to road intersections
  - PostGIS geospatial queries
  - Comprehensive error handling
  - Input validation using Pydantic

**`optimization.py`** - Route Optimization API
- **Purpose**: API endpoint for route optimization
- **Endpoints**:
  - `POST /optimize/routes`: Optimize routes for specified number of buses
- **Parameters**:
  - `num_buses`: Number of buses for optimization (query parameter)
- **Response**: Returns optimized routes with stop sequences and coordinates
- **Error Handling**: Comprehensive error handling with detailed logging

#### **Database Layer (`/backend/app/db/`)**

**`database.py`** - Database Connection and Session Management
- **Purpose**: Centralized database configuration and session management
- **Key Components**:
  - SQLAlchemy engine configuration
  - Session factory setup
  - Dependency injection for FastAPI
  - Database initialization functions
- **Features**:
  - Connection pooling
  - Health checks
  - Automatic session cleanup

### **Application Entry Points**

**`main.py`** - FastAPI Application Entry Point
- **Purpose**: Main FastAPI application configuration
- **Key Features**:
  - CORS middleware configuration
  - API router registration
  - Health check endpoints
  - Automatic API documentation (Swagger/ReDoc)
- **Endpoints**:
  - `GET /`: Root endpoint with API information
  - `GET /health`: Health check for monitoring
- **Documentation**: Auto-generated at `/docs` and `/redoc`

**`run.py`** - Development Server Runner
- **Purpose**: Development server configuration
- **Features**:
  - Uvicorn server with hot reload
  - Debug mode configuration
  - Logging configuration

**`init_db.py`** - Database Initialization
- **Purpose**: Initialize database tables and PostGIS extensions
- **Usage**: Run once to set up the database schema
- **Features**:
  - Creates all tables
  - Enables PostGIS extension
  - Sets up spatial indexes

### **Dependencies and Configuration**

**`requirements.txt`** - Python Dependencies
- **Core Framework**: FastAPI, Uvicorn
- **Database**: SQLAlchemy, PostgreSQL driver, PostGIS support
- **Geospatial**: OSMnx, NetworkX, GeoPy, scikit-learn
- **Validation**: Pydantic, Pydantic Settings
- **Environment**: python-dotenv

**`env.example`** - Environment Configuration Template
- **Purpose**: Template for environment variables
- **Variables**: Database credentials, API keys, CORS settings

### **Data and Cache Files**

**`/backend/cache/`** - Application Cache
- **Purpose**: Stores cached data for performance
- **Files**: JSON cache files for various operations

**`/backend/road_networks/`** - Road Network Data
- **Purpose**: Cached OpenStreetMap road network data
- **Files**: 
  - `Irvine_California_USA.pkl`: Pickled NetworkX graph of Irvine road network
- **Format**: Python pickle files containing NetworkX MultiDiGraph objects
- **Creation**: Generated by OSMnx when downloading road network data
- **Usage**: Loaded by `RoadNetworkManager` for coordinate snapping and route optimization

**`/backend/venv/`** - Python Virtual Environment
- **Purpose**: Isolated Python environment for the project
- **Contents**: Python interpreter, installed packages, activation scripts
- **Usage**: Provides isolated dependency management

---

## Frontend Structure (`/frontend/`)

### **Source Code (`/frontend/src/`)**

#### **Main Application**

**`App.tsx`** - Main React Application Component
- **Purpose**: Root component managing application state and user interactions
- **Key Features**:
  - State management for bus stops, routes, and UI state
  - API integration for CRUD operations
  - Form handling for bus stop creation/editing
  - Route optimization integration
  - Error handling and loading states
- **State Management**:
  - `busStops`: Array of bus stop objects
  - `routes`: Array of optimized route objects
  - `showForm`: Modal form visibility
  - `editingStop`: Currently editing stop
  - `isLoading`: Loading state indicator
- **Key Functions**:
  - `loadBusStops()`: Fetches all bus stops from API
  - `handleFormSubmit()`: Handles bus stop creation/updates
  - `handleDeleteStop()`: Handles bus stop deletion
  - `handleOptimize()`: Triggers route optimization

#### **Components (`/frontend/src/components/`)**

**`MapComponent.tsx`** - Google Maps Integration
- **Purpose**: Interactive map component with Google Maps API
- **Key Features**:
  - Google Maps initialization and configuration
  - Bus stop markers with click handlers
  - Route polylines with different colors
  - Map click handling for adding new stops
  - Marker management and cleanup
- **Dependencies**: Google Maps JavaScript API, @googlemaps/js-api-loader
- **Props**: busStops, routes, onMapClick, onStopClick
- **Features**:
  - Automatic marker updates when stops change
  - Route visualization with colored polylines
  - Click-to-add functionality

**`BusStopForm.tsx`** - Bus Stop Creation/Editing Form
- **Purpose**: Modal form for creating and editing bus stops
- **Key Features**:
  - Form validation and error handling
  - Coordinate pre-filling from map clicks
  - Demand weight input with range validation
  - Create/Update mode switching
- **Props**: onSubmit, onCancel, initialData
- **Form Fields**:
  - Name (required)
  - Description (optional)
  - Latitude/Longitude (required, numeric)
  - Demand Weight (0.0-1.0, default 0.5)

**`BusStopList.tsx`** - Bus Stop Management List
- **Purpose**: Displays list of all bus stops with management options
- **Key Features**:
  - Stop information display (name, coordinates, demand)
  - Edit and delete buttons for each stop
  - Empty state handling
  - Responsive design
- **Props**: busStops, onEdit, onDelete
- **Features**:
  - Coordinate formatting
  - Demand weight display
  - Action button integration

**`OptimizationControls.tsx`** - Route Optimization Interface
- **Purpose**: Controls for triggering route optimization
- **Key Features**:
  - Number of buses input
  - Optimization trigger button
  - Loading state handling
  - Validation for minimum stops
- **Props**: onOptimize, isLoading, numStops
- **Features**:
  - Input validation
  - Disabled state when insufficient stops
  - Loading indicator

#### **Services (`/frontend/src/services/`)**

**`api.ts`** - API Client Service
- **Purpose**: Centralized API communication layer
- **Key Features**:
  - Axios HTTP client configuration
  - Bus stop CRUD operations
  - Route optimization API calls
  - Error handling and response processing
- **API Endpoints**:
  - `busStopAPI.getAll()`: Fetch all bus stops
  - `busStopAPI.create()`: Create new bus stop
  - `busStopAPI.update()`: Update existing bus stop
  - `busStopAPI.delete()`: Delete bus stop
  - `busStopAPI.getNearby()`: Find nearby stops
  - `optimizationAPI.optimizeRoutes()`: Optimize routes
- **Configuration**: Base URL, headers, error handling

#### **Types (`/frontend/src/types/`)**

**`index.ts`** - TypeScript Type Definitions
- **Purpose**: Centralized type definitions for the application
- **Key Interfaces**:
  - `BusStop`: Bus stop data structure
  - `Route`: Optimized route structure
  - `OptimizationResponse`: API response for optimization
- **Features**:
  - Type safety across the application
  - API contract definition
  - IntelliSense support

#### **Styling and Assets**

**`App.css`** - Main Application Styles
- **Purpose**: Global styles and component styling
- **Features**:
  - Responsive design
  - Modal styling
  - Loading states
  - Form styling

**`index.css`** - Global Styles
- **Purpose**: Base styles and CSS resets
- **Features**:
  - CSS normalization
  - Global typography
  - Base component styles

### **Build and Distribution**

**`/frontend/build/`** - Production Build Output
- **Purpose**: Compiled and optimized production build
- **Contents**:
  - `index.html`: Main HTML file
  - `static/css/`: Compiled CSS files
  - `static/js/`: Compiled JavaScript bundles
  - `asset-manifest.json`: Build manifest
- **Files**:
  - `main.a6fe5e48.js`: Main application bundle
  - `453.d7446e4a.chunk.js`: Code splitting chunk
  - `main.bdb7fbd9.css`: Compiled stylesheet
- **Generation**: Created by `npm run build` command
- **Usage**: Served by web server for production deployment

### **Configuration and Dependencies**

**`package.json`** - Node.js Dependencies and Scripts
- **Dependencies**:
  - React 19.2.0 with TypeScript support
  - Google Maps integration (@googlemaps/js-api-loader)
  - HTTP client (axios)
  - Testing libraries (@testing-library/*)
- **Scripts**:
  - `start`: Development server
  - `build`: Production build
  - `test`: Test runner
- **Configuration**: ESLint, Browserslist

**`tsconfig.json`** - TypeScript Configuration
- **Purpose**: TypeScript compiler configuration
- **Features**: Strict type checking, modern JavaScript target

**`env.example`** - Environment Configuration Template
- **Purpose**: Template for frontend environment variables
- **Variables**: Google Maps API key

---

## Test Suite (`/tests/`)

### **Test Configuration**

**`conftest.py`** - Test Configuration and Fixtures
- **Purpose**: Centralized test setup and configuration
- **Key Features**:
  - Separate test database setup
  - SQLAlchemy session fixtures
  - FastAPI TestClient configuration
  - Database isolation between tests
- **Fixtures**:
  - `setup_test_database()`: Creates/drops test tables
  - `db_session()`: Test database session
  - `client()`: FastAPI test client with database override
- **Database**: Uses separate test database (`optimumbus_db_test`)

**`pytest.ini`** - Test Runner Configuration
- **Purpose**: Pytest configuration and options
- **Features**:
  - Python path configuration
  - Warning filters
  - Test discovery settings

### **Test Files**

**`test_api_stops.py`** - API Endpoint Tests
- **Purpose**: Tests for bus stop CRUD API endpoints
- **Test Cases**:
  - `test_create_bus_stop_success()`: Validates successful stop creation
  - `test_create_bus_stop_invalid_data()`: Validates error handling for invalid data
- **Features**:
  - Uses test database isolation
  - Validates HTTP status codes and response data
  - Tests both success and error scenarios

**`test_optimization_logic.py`** - Optimization Algorithm Tests
- **Purpose**: Unit tests for optimization algorithms
- **Test Cases**:
  - Tests nearest-neighbor algorithm
  - Tests graph-based coordinate snapping
- **Features**:
  - Pure unit tests (no database/API dependencies)
  - Fast execution
  - Algorithm validation

---

## Binary Files and Generated Content

### **Road Network Data (`/backend/road_networks/Irvine_California_USA.pkl`)**
- **Type**: Python pickle file
- **Content**: NetworkX MultiDiGraph object containing OpenStreetMap road network data
- **Creation**: Generated by OSMnx when downloading road network for Irvine, California
- **Size**: Contains nodes (intersections) and edges (road segments) with attributes
- **Usage**: Loaded by `RoadNetworkManager` for coordinate snapping and route optimization
- **Format**: Binary pickle format for efficient storage and loading

### **Frontend Build Artifacts (`/frontend/build/`)**
- **Type**: Compiled JavaScript and CSS bundles
- **Content**: Minified and optimized production code
- **Files**:
  - `main.a6fe5e48.js`: Main application bundle (compiled React components)
  - `453.d7446e4a.chunk.js`: Code-split chunk for optimization
  - `main.bdb7fbd9.css`: Compiled and minified stylesheet
  - `asset-manifest.json`: Build manifest with file mappings
- **Generation**: Created by `react-scripts build` command
- **Purpose**: Production-ready static files for web server deployment

### **Python Virtual Environment (`/backend/venv/`)**
- **Type**: Python virtual environment directory
- **Content**: Isolated Python environment with installed packages
- **Structure**:
  - `bin/`: Python interpreter and executable scripts
  - `lib/python3.13/site-packages/`: Installed Python packages
  - `pyvenv.cfg`: Virtual environment configuration
- **Purpose**: Dependency isolation and version management
- **Usage**: Activated with `source venv/bin/activate` before running the application

### **Cache Files (`/backend/cache/`)**
- **Type**: JSON cache files
- **Content**: Cached data for various operations
- **Files**: Hash-named JSON files containing cached results
- **Purpose**: Performance optimization by avoiding repeated computations
- **Usage**: Automatically managed by the application

---

## Environment Configuration

### **`.env.local`** - Unified Environment Configuration
- **Purpose**: Single configuration file for both backend and frontend
- **Backend Variables**:
  - `DATABASE_URL`: PostgreSQL connection string
  - `POSTGRES_*`: Database credentials
  - `ALLOWED_ORIGINS`: CORS configuration
- **Frontend Variables**:
  - `REACT_APP_GOOGLE_MAPS_API_KEY`: Google Maps API key
- **Usage**: Loaded by both backend (Pydantic Settings) and frontend (React environment)

---

## Development Workflow

### **Backend Development**
1. **Setup**: Create virtual environment and install dependencies
2. **Database**: Set up PostgreSQL with PostGIS extension
3. **Configuration**: Configure `.env.local` with database credentials
4. **Initialization**: Run `python init_db.py` to create tables
5. **Development**: Run `python run.py` for development server
6. **Testing**: Run `pytest` for test suite

### **Frontend Development**
1. **Setup**: Install Node.js dependencies with `npm install`
2. **Configuration**: Set Google Maps API key in `.env.local`
3. **Development**: Run `npm start` for development server
4. **Building**: Run `npm run build` for production build
5. **Testing**: Run `npm test` for test suite

### **Integration**
- **CORS**: Backend configured to allow frontend origins
- **API**: Frontend communicates with backend via REST API
- **Data Flow**: Frontend → API → Database → Optimization → Response

---

## Key Technologies and Libraries

### **Backend Stack**
- **FastAPI**: Modern Python web framework with automatic API documentation
- **SQLAlchemy**: Python SQL toolkit and ORM
- **PostgreSQL + PostGIS**: Robust database with geospatial capabilities
- **Pydantic**: Data validation and serialization
- **OSMnx**: OpenStreetMap data processing
- **NetworkX**: Graph algorithms and analysis
- **scikit-learn**: Machine learning algorithms (K-Means clustering)

### **Frontend Stack**
- **React 19**: Modern JavaScript library for building user interfaces
- **TypeScript**: Type-safe JavaScript development
- **Google Maps API**: Interactive mapping and geolocation
- **Axios**: HTTP client for API communication
- **CSS3**: Modern styling with responsive design

### **Testing Stack**
- **pytest**: Python testing framework
- **FastAPI TestClient**: API testing utilities
- **React Testing Library**: React component testing
- **Jest**: JavaScript testing framework

---

## Performance Considerations

### **Backend Optimizations**
- **Database Indexing**: Spatial indexes on geometry columns
- **Connection Pooling**: SQLAlchemy connection pool management
- **Caching**: Road network data caching in pickle files
- **Geospatial Queries**: PostGIS for efficient spatial operations

### **Frontend Optimizations**
- **Code Splitting**: Separate chunks for different features
- **Bundle Optimization**: Minified and compressed production builds
- **Lazy Loading**: Components loaded on demand
- **Caching**: Browser caching for static assets

### **Scalability Features**
- **Database**: PostgreSQL with PostGIS for large-scale geospatial data
- **API**: RESTful design for easy integration
- **Caching**: Multiple levels of caching for performance
- **Modularity**: Clean separation of concerns for maintainability

---

This documentation provides a comprehensive overview of the OptimumBus codebase structure, explaining the purpose and functionality of each component, file, and directory in the system.
