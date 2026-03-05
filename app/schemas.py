from pydantic import BaseModel, Field
from typing import List

class Coordinate(BaseModel):
    lat: float
    lon: float

class RouteRequest(BaseModel):
    coordinates: List[Coordinate] = Field(min_items=2, max_items=10)

class RouteResponse(BaseModel):
    total_distance: float
    route: List[Coordinate]