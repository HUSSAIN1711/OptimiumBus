"""
Geospatial utility functions for PostGIS operations

This module provides utility functions for performing geospatial queries
using PostGIS, including distance calculations, spatial indexing, and
geometric operations.
"""

from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from app.models.bus_stop import BusStop
import logging

logger = logging.getLogger(__name__)


def find_stops_within_radius(
    db: Session,
    latitude: float,
    longitude: float,
    radius_meters: float,
    limit: int = 100
) -> List[BusStop]:
    """
    Find bus stops within a specified radius using PostGIS
    
    Args:
        db: Database session
        latitude: Center latitude
        longitude: Center longitude
        radius_meters: Search radius in meters
        limit: Maximum number of results
        
    Returns:
        List[BusStop]: Bus stops within the radius
    """
    try:
        # Create a point geometry for the search center
        point_wkt = f"POINT({longitude} {latitude})"
        
        # Use PostGIS ST_DWithin for efficient spatial query
        query = text("""
            SELECT * FROM bus_stops 
            WHERE ST_DWithin(
                geometry,
                ST_SetSRID(ST_GeomFromText(:point_wkt), 4326),
                :radius_meters
            )
            ORDER BY ST_Distance(
                geometry,
                ST_SetSRID(ST_GeomFromText(:point_wkt), 4326)
            )
            LIMIT :limit
        """)
        
        result = db.execute(query, {
            'point_wkt': point_wkt,
            'radius_meters': radius_meters,
            'limit': limit
        })
        
        # Convert result to BusStop objects
        stops = []
        for row in result:
            stop = BusStop(
                id=row.id,
                name=row.name,
                description=row.description,
                latitude=row.latitude,
                longitude=row.longitude,
                demand_weight=row.demand_weight,
                created_at=row.created_at,
                updated_at=row.updated_at
            )
            stops.append(stop)
        
        return stops
        
    except Exception as e:
        logger.error(f"Error finding stops within radius: {e}")
        raise


def calculate_distance_between_stops(
    db: Session,
    stop1_id: str,
    stop2_id: str
) -> Optional[float]:
    """
    Calculate the distance between two bus stops using PostGIS
    
    Args:
        db: Database session
        stop1_id: ID of first bus stop
        stop2_id: ID of second bus stop
        
    Returns:
        float: Distance in meters, or None if stops not found
    """
    try:
        query = text("""
            SELECT ST_Distance(
                s1.geometry,
                s2.geometry
            ) as distance
            FROM bus_stops s1, bus_stops s2
            WHERE s1.id = :stop1_id AND s2.id = :stop2_id
        """)
        
        result = db.execute(query, {
            'stop1_id': stop1_id,
            'stop2_id': stop2_id
        }).fetchone()
        
        if result:
            return float(result.distance)
        return None
        
    except Exception as e:
        logger.error(f"Error calculating distance between stops: {e}")
        return None


def find_stops_in_bounding_box(
    db: Session,
    min_lat: float,
    min_lng: float,
    max_lat: float,
    max_lng: float,
    limit: int = 1000
) -> List[BusStop]:
    """
    Find bus stops within a bounding box using PostGIS
    
    Args:
        db: Database session
        min_lat: Minimum latitude
        min_lng: Minimum longitude
        max_lat: Maximum latitude
        max_lng: Maximum longitude
        limit: Maximum number of results
        
    Returns:
        List[BusStop]: Bus stops within the bounding box
    """
    try:
        # Create bounding box geometry
        bbox_wkt = f"POLYGON(({min_lng} {min_lat}, {max_lng} {min_lat}, {max_lng} {max_lat}, {min_lng} {max_lat}, {min_lng} {min_lat}))"
        
        query = text("""
            SELECT * FROM bus_stops 
            WHERE ST_Within(
                geometry,
                ST_SetSRID(ST_GeomFromText(:bbox_wkt), 4326)
            )
            LIMIT :limit
        """)
        
        result = db.execute(query, {
            'bbox_wkt': bbox_wkt,
            'limit': limit
        })
        
        # Convert result to BusStop objects
        stops = []
        for row in result:
            stop = BusStop(
                id=row.id,
                name=row.name,
                description=row.description,
                latitude=row.latitude,
                longitude=row.longitude,
                demand_weight=row.demand_weight,
                created_at=row.created_at,
                updated_at=row.updated_at
            )
            stops.append(stop)
        
        return stops
        
    except Exception as e:
        logger.error(f"Error finding stops in bounding box: {e}")
        raise


def get_stop_density_analysis(
    db: Session,
    latitude: float,
    longitude: float,
    radius_meters: float = 1000
) -> dict:
    """
    Analyze bus stop density in a given area
    
    Args:
        db: Database session
        latitude: Center latitude
        longitude: Center longitude
        radius_meters: Analysis radius in meters
        
    Returns:
        dict: Density analysis results
    """
    try:
        point_wkt = f"POINT({longitude} {latitude})"
        
        query = text("""
            SELECT 
                COUNT(*) as stop_count,
                AVG(demand_weight) as avg_demand,
                MIN(ST_Distance(geometry, ST_SetSRID(ST_GeomFromText(:point_wkt), 4326))) as min_distance,
                MAX(ST_Distance(geometry, ST_SetSRID(ST_GeomFromText(:point_wkt), 4326))) as max_distance
            FROM bus_stops 
            WHERE ST_DWithin(
                geometry,
                ST_SetSRID(ST_GeomFromText(:point_wkt), 4326),
                :radius_meters
            )
        """)
        
        result = db.execute(query, {
            'point_wkt': point_wkt,
            'radius_meters': radius_meters
        }).fetchone()
        
        if result:
            return {
                'stop_count': result.stop_count,
                'avg_demand_weight': float(result.avg_demand) if result.avg_demand else 0.0,
                'min_distance_meters': float(result.min_distance) if result.min_distance else 0.0,
                'max_distance_meters': float(result.max_distance) if result.max_distance else 0.0,
                'density_per_sq_km': result.stop_count / (3.14159 * (radius_meters / 1000) ** 2)
            }
        
        return {
            'stop_count': 0,
            'avg_demand_weight': 0.0,
            'min_distance_meters': 0.0,
            'max_distance_meters': 0.0,
            'density_per_sq_km': 0.0
        }
        
    except Exception as e:
        logger.error(f"Error in density analysis: {e}")
        return {
            'stop_count': 0,
            'avg_demand_weight': 0.0,
            'min_distance_meters': 0.0,
            'max_distance_meters': 0.0,
            'density_per_sq_km': 0.0,
            'error': str(e)
        }


def update_geometry_from_coordinates(db: Session, stop_id: str) -> bool:
    """
    Update the PostGIS geometry column from latitude/longitude coordinates
    
    Args:
        db: Database session
        stop_id: ID of the bus stop to update
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        query = text("""
            UPDATE bus_stops 
            SET geometry = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
            WHERE id = :stop_id
        """)
        
        result = db.execute(query, {'stop_id': stop_id})
        db.commit()
        
        return result.rowcount > 0
        
    except Exception as e:
        logger.error(f"Error updating geometry: {e}")
        db.rollback()
        return False


def create_spatial_indexes(db: Session) -> bool:
    """
    Create spatial indexes on the geometry column for better performance
    
    Args:
        db: Database session
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create GIST index on geometry column
        query = text("""
            CREATE INDEX IF NOT EXISTS idx_bus_stops_geometry_gist 
            ON bus_stops USING GIST (geometry)
        """)
        
        db.execute(query)
        db.commit()
        
        logger.info("Spatial indexes created successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error creating spatial indexes: {e}")
        db.rollback()
        return False
