from fastapi import FastAPI
from routing.service import compute_route
from routing.graph import load_graph
from app.schemas import RouteRequest, RouteResponse
import random

app = FastAPI()

@app.on_event("startup")
def startup():
    print(f"Loading graph for Chicago, Illinois...")
    app.state.graph = load_graph("Chicago, Illinois, USA")

@app.get("/health/live")
def live():
    return {"status": "alive"}

@app.get("/health/ready")
def ready():
    if not hasattr(app.state, "graph"):
        return {"status": "loading"}
    return {"status": "ready"}

@app.post("/route", response_model=RouteResponse)
def route(request: RouteRequest):

    G = app.state.graph

    stop_nodes = random.sample(list(G.nodes), request.num_stops)

    total_distance, route = compute_route(G, stop_nodes)

    return RouteResponse(
        total_distance=total_distance,
        route=route
    )