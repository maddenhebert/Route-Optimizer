from fastapi import FastAPI, HTTPException, Request
from routing.service import compute_route
from routing.graph import load_graph
from app.schemas import RouteRequest, RouteResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import osmnx as ox

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

def is_within_bounds(lat, lon):
    return (
        41.60 <= lat <= 42.05 and
        -87.95 <= lon <= -87.50
    )

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

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/route", response_model=RouteResponse)
def route(request: RouteRequest):

    G = app.state.graph

    stop_nodes = []

    for coord in request.coordinates:
        if not is_within_bounds(coord.lat, coord.lon):
            raise HTTPException(status_code=400, detail="Coordinate outside Chicago bounds")

    for coord in request.coordinates:
        node = ox.nearest_nodes(G, X=coord.lon, Y=coord.lat)
        stop_nodes.append(node)

    total_distance, full_path = compute_route(G, stop_nodes)

    route_coords = [
    {"lat": G.nodes[n]["y"], "lon": G.nodes[n]["x"]}
    for n in full_path
    ]

    return RouteResponse(
        total_distance=total_distance,
        route=route_coords
    )