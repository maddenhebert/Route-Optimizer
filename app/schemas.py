from pydantic import BaseModel
from typing import List

class RouteRequest(BaseModel):
    city: str
    num_stops: int

class RouteResponse(BaseModel):
    total_distance: float
    route: List[int]