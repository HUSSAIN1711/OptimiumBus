from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.bus_stop import BusStop
from app.core.optimization import optimize_routes

router = APIRouter(prefix="/optimize", tags=["optimization"]) 


@router.post("/routes")
def optimize_routes_endpoint(num_buses: int, db: Session = Depends(get_db)) -> Dict[str, List[Dict]]:
    try:
        stops = db.query(BusStop).all()
        if not stops:
            raise HTTPException(status_code=400, detail="No bus stops available to optimize")
        if num_buses <= 0:
            raise HTTPException(status_code=400, detail="num_buses must be >= 1")
        routes = optimize_routes(stops, num_buses)
        return {"routes": routes, "num_buses": num_buses, "num_stops": len(stops)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")
