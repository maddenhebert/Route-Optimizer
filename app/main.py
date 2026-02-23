from fastapi import FastAPI
from routing.service import compute_route
from app.schemas import RouteRequest, RouteResponse