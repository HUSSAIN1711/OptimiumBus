from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.bus_stop import BusStop
from app.core.optimization import optimize_routes

router = APIRouter(prefix="/optimize", tags=["optimization"]) 


@router.post("/routes")
def optimize_routes_endpoint(
    num_buses: int = Query(..., description="Number of buses for optimization"),
    db: Session = Depends(get_db)
):
    try:
        print(f"API endpoint called with num_buses={num_buses}")
        stops = db.query(BusStop).all()
        print(f"Found {len(stops)} stops in database")
        
        if not stops:
            raise HTTPException(status_code=400, detail="No bus stops available to optimize")
        if num_buses <= 0:
            raise HTTPException(status_code=400, detail="num_buses must be >= 1")
        
        print(f"Starting optimization with {len(stops)} stops and {num_buses} buses")
        routes = optimize_routes(stops, num_buses)
        print(f"Optimization completed, generated {len(routes)} routes")
        return {"routes": routes, "num_buses": num_buses, "num_stops": len(stops)}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Optimization error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")
