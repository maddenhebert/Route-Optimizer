from pydantic import BaseModel
from typing import List

class Coordinate(BaseModel):
    lat: float
    lon: float

class RouteRequest(BaseModel):
    coordinates: List[Coordinate]

class RouteResponse(BaseModel):
    total_distance: float
    route: List[Coordinate]