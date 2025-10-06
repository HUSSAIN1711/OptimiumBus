"""
Bus Stops API Router

This module provides RESTful API endpoints for managing bus stops,
including CRUD operations and geospatial functionality.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app.db.database import get_db
from app.models.bus_stop import (
    BusStop,
    BusStopCreate,
    BusStopUpdate,
    BusStopResponse,
    BusStopListResponse
)
from app.core.osmnx_utils import snap_coordinates_to_road_network, get_road_network_manager
from app.core.geospatial_utils import find_stops_within_radius, get_stop_density_analysis

# Create API router with prefix and tags
router = APIRouter(
    prefix="/stops",
    tags=["bus-stops"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=BusStopListResponse)
async def get_bus_stops(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """
    Get a paginated list of all bus stops
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        sort_by: Field to sort by (name, created_at, latitude, longitude, demand_weight)
        sort_order: Sort order (asc or desc)
        db: Database session
        
    Returns:
        BusStopListResponse: Paginated list of bus stops with metadata
    """
    try:
        # Validate sort_by field
        valid_sort_fields = ["name", "created_at", "latitude", "longitude", "demand_weight"]
        if sort_by not in valid_sort_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid sort field. Must be one of: {', '.join(valid_sort_fields)}"
            )
        
        # Get sort column
        sort_column = getattr(BusStop, sort_by)
        sort_func = desc if sort_order == "desc" else asc
        
        # Query bus stops with pagination and sorting
        query = db.query(BusStop).order_by(sort_func(sort_column))
        total = query.count()
        stops = query.offset(skip).limit(limit).all()
        
        # Calculate pagination info
        page = (skip // limit) + 1
        
        return BusStopListResponse(
            stops=stops,
            total=total,
            page=page,
            size=limit
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bus stops: {str(e)}")


@router.get("/{stop_id}", response_model=BusStopResponse)
async def get_bus_stop(stop_id: str, db: Session = Depends(get_db)):
    """
    Get a specific bus stop by ID
    
    Args:
        stop_id: UUID of the bus stop
        db: Database session
        
    Returns:
        BusStopResponse: The requested bus stop
        
    Raises:
        HTTPException: If bus stop is not found
    """
    try:
        stop = db.query(BusStop).filter(BusStop.id == stop_id).first()
        if not stop:
            raise HTTPException(status_code=404, detail="Bus stop not found")
        return stop
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bus stop: {str(e)}")


@router.post("/", response_model=BusStopResponse, status_code=201)
async def create_bus_stop(
    bus_stop: BusStopCreate,
    snap_to_road: bool = Query(True, description="Snap coordinates to nearest road intersection"),
    db: Session = Depends(get_db)
):
    """
    Create a new bus stop with optional coordinate snapping
    
    Args:
        bus_stop: Bus stop data to create
        snap_to_road: Whether to snap coordinates to nearest road intersection
        db: Database session
        
    Returns:
        BusStopResponse: The created bus stop
        
    Raises:
        HTTPException: If creation fails
    """
    try:
        # Get coordinates (snap to road if requested)
        final_latitude = bus_stop.latitude
        final_longitude = bus_stop.longitude
        
        if snap_to_road:
            try:
                snapped_lat, snapped_lng, node_id = snap_coordinates_to_road_network(
                    bus_stop.latitude, bus_stop.longitude
                )
                final_latitude = snapped_lat
                final_longitude = snapped_lng
                # Note: We could store the node_id in a future enhancement
            except Exception as e:
                # If snapping fails, use original coordinates
                print(f"Warning: Coordinate snapping failed: {e}. Using original coordinates.")
        
        # Create new bus stop instance
        db_bus_stop = BusStop(
            name=bus_stop.name,
            description=bus_stop.description,
            latitude=final_latitude,
            longitude=final_longitude,
            demand_weight=bus_stop.demand_weight
        )
        
        # Add to database
        db.add(db_bus_stop)
        db.commit()
        db.refresh(db_bus_stop)
        
        return db_bus_stop
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating bus stop: {str(e)}")


@router.put("/{stop_id}", response_model=BusStopResponse)
async def update_bus_stop(
    stop_id: str,
    bus_stop_update: BusStopUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing bus stop
    
    Args:
        stop_id: UUID of the bus stop to update
        bus_stop_update: Updated bus stop data
        db: Database session
        
    Returns:
        BusStopResponse: The updated bus stop
        
    Raises:
        HTTPException: If bus stop is not found or update fails
    """
    try:
        # Find existing bus stop
        db_bus_stop = db.query(BusStop).filter(BusStop.id == stop_id).first()
        if not db_bus_stop:
            raise HTTPException(status_code=404, detail="Bus stop not found")
        
        # Update fields that are provided
        update_data = bus_stop_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_bus_stop, field, value)
        
        # Save changes
        db.commit()
        db.refresh(db_bus_stop)
        
        return db_bus_stop
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating bus stop: {str(e)}")


@router.delete("/{stop_id}", status_code=204)
async def delete_bus_stop(stop_id: str, db: Session = Depends(get_db)):
    """
    Delete a bus stop
    
    Args:
        stop_id: UUID of the bus stop to delete
        db: Database session
        
    Raises:
        HTTPException: If bus stop is not found or deletion fails
    """
    try:
        # Find existing bus stop
        db_bus_stop = db.query(BusStop).filter(BusStop.id == stop_id).first()
        if not db_bus_stop:
            raise HTTPException(status_code=404, detail="Bus stop not found")
        
        # Delete the bus stop
        db.delete(db_bus_stop)
        db.commit()
        
        return None  # 204 No Content
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting bus stop: {str(e)}")


@router.get("/nearby/", response_model=List[BusStopResponse])
async def get_nearby_bus_stops(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude coordinate"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude coordinate"),
    radius_km: float = Query(1.0, ge=0.1, le=50.0, description="Search radius in kilometers"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Find bus stops near a given coordinate using PostGIS
    
    Uses PostGIS ST_DWithin for accurate geospatial queries with proper
    distance calculations on the Earth's surface.
    
    Args:
        latitude: Latitude coordinate to search from
        longitude: Longitude coordinate to search from
        radius_km: Search radius in kilometers
        limit: Maximum number of results to return
        db: Database session
        
    Returns:
        List[BusStopResponse]: List of nearby bus stops
    """
    try:
        # Convert kilometers to meters for PostGIS
        radius_meters = radius_km * 1000
        
        # Use PostGIS for accurate geospatial query
        stops = find_stops_within_radius(
            db=db,
            latitude=latitude,
            longitude=longitude,
            radius_meters=radius_meters,
            limit=limit
        )
        
        return stops
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding nearby bus stops: {str(e)}")


@router.get("/density-analysis/")
async def get_stop_density_analysis(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude coordinate"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude coordinate"),
    radius_km: float = Query(1.0, ge=0.1, le=10.0, description="Analysis radius in kilometers"),
    db: Session = Depends(get_db)
):
    """
    Analyze bus stop density in a given area
    
    Args:
        latitude: Latitude coordinate for analysis center
        longitude: Longitude coordinate for analysis center
        radius_km: Analysis radius in kilometers
        db: Database session
        
    Returns:
        dict: Density analysis results
    """
    try:
        # Convert kilometers to meters
        radius_meters = radius_km * 1000
        
        # Get density analysis
        analysis = get_stop_density_analysis(
            db=db,
            latitude=latitude,
            longitude=longitude,
            radius_meters=radius_meters
        )
        
        return {
            "status": "success",
            "analysis": analysis,
            "center_coordinates": {"latitude": latitude, "longitude": longitude},
            "radius_km": radius_km
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in density analysis: {str(e)}")


@router.get("/road-network/info")
async def get_road_network_info():
    """
    Get information about the current road network
    
    Returns:
        Dict containing road network statistics and information
    """
    try:
        network_manager = get_road_network_manager()
        stats = network_manager.get_network_stats()
        return {
            "status": "success",
            "road_network": stats,
            "message": "Road network information retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting road network info: {str(e)}")


@router.post("/road-network/refresh")
async def refresh_road_network():
    """
    Force refresh the road network data (re-download from OpenStreetMap)
    
    Returns:
        Dict containing updated road network information
    """
    try:
        network_manager = get_road_network_manager()
        # Force re-download
        network_manager.get_road_network(force_download=True)
        stats = network_manager.get_network_stats()
        return {
            "status": "success",
            "road_network": stats,
            "message": "Road network refreshed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing road network: {str(e)}")
