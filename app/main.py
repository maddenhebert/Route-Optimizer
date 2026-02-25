from fastapi import FastAPI
from routing.service import compute_route
from routing.graph import load_graph
from app.schemas import RouteRequest, RouteResponse
import random

def get_graph(city: str):
    cache = app.state.graph_cache

    if city not in cache:
        print(f"Loading graph for {city}...")
        cache[city] = load_graph(city)

    return cache[city]

app = FastAPI()

@app.on_event("startup")
def startup():
    app.state.graph_cache = {}

@app.post("/route", response_model=RouteResponse)
def route(request: RouteRequest):

    G = get_graph(request.city)

    stop_nodes = random.sample(list(G.nodes), request.num_stops)

    total_distance, route = compute_route(G, stop_nodes)

    return RouteResponse(
        total_distance=total_distance,
        route=route
    )