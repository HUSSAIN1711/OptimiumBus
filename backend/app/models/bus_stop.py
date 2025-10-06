"""
Bus Stop data models

This module defines both the SQLAlchemy database model and Pydantic schemas
for bus stops. The SQLAlchemy model represents the database table structure,
while Pydantic schemas handle data validation and serialization for the API.
"""

from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func as sql_func
from pydantic import BaseModel, Field, validator
from app.db.database import Base
import uuid


class BusStop(Base):
    """
    SQLAlchemy model for bus stops table
    
    This model represents the database table structure for storing bus stop
    information including geospatial coordinates and passenger demand data.
    """
    __tablename__ = "bus_stops"
    
    # Primary key - using UUID for better scalability and security
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Basic information
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    
    # Geospatial coordinates (latitude and longitude)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    
    # Passenger demand weight (0.0 to 1.0, where 1.0 is highest demand)
    # This will be used in the optimization algorithm to prioritize stops
    demand_weight = Column(Float, nullable=False, default=0.5)
    
    # Timestamps for tracking
    created_at = Column(DateTime(timezone=True), server_default=sql_func.now())
    updated_at = Column(DateTime(timezone=True), server_default=sql_func.now(), onupdate=sql_func.now())
    
    def __repr__(self):
        return f"<BusStop(id={self.id}, name='{self.name}', lat={self.latitude}, lng={self.longitude})>"


# Pydantic schemas for API validation and serialization

class BusStopBase(BaseModel):
    """
    Base Pydantic schema for bus stop data
    
    This contains the common fields that are shared between
    create, update, and response schemas.
    """
    name: str = Field(..., min_length=1, max_length=255, description="Name of the bus stop")
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the bus stop")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate (-180 to 180)")
    demand_weight: float = Field(0.5, ge=0.0, le=1.0, description="Passenger demand weight (0.0 to 1.0)")
    
    @validator('latitude', 'longitude')
    def validate_coordinates(cls, v):
        """
        Validate coordinate values are within valid ranges
        
        Args:
            v: The coordinate value to validate
            
        Returns:
            float: The validated coordinate value
            
        Raises:
            ValueError: If coordinate is outside valid range
        """
        if isinstance(v, (int, float)):
            return float(v)
        raise ValueError('Coordinates must be numeric values')


class BusStopCreate(BusStopBase):
    """
    Pydantic schema for creating a new bus stop
    
    This schema is used when receiving data from the API to create
    a new bus stop. It inherits all fields from BusStopBase.
    """
    pass


class BusStopUpdate(BaseModel):
    """
    Pydantic schema for updating an existing bus stop
    
    All fields are optional since we might only want to update
    specific fields of an existing bus stop.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    demand_weight: Optional[float] = Field(None, ge=0.0, le=1.0)


class BusStopResponse(BusStopBase):
    """
    Pydantic schema for API responses containing bus stop data
    
    This schema includes all the base fields plus the database-generated
    fields like id and timestamps. It's used when returning bus stop
    data to the client.
    """
    id: uuid.UUID = Field(..., description="Unique identifier for the bus stop")
    created_at: datetime = Field(..., description="Timestamp when the bus stop was created")
    updated_at: datetime = Field(..., description="Timestamp when the bus stop was last updated")
    
    class Config:
        """
        Pydantic configuration for the response schema
        
        orm_mode: Allows the schema to work with SQLAlchemy ORM objects
        """
        from_attributes = True  # This replaces the deprecated orm_mode=True


class BusStopListResponse(BaseModel):
    """
    Pydantic schema for API responses containing a list of bus stops
    
    This schema is used when returning multiple bus stops, such as
    in the GET /stops/ endpoint.
    """
    stops: list[BusStopResponse] = Field(..., description="List of bus stops")
    total: int = Field(..., description="Total number of bus stops")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of items per page")
