import osmnx

# loads graph for given city 
def load_graph(city: str):
    return osmnx.graph_from_place(city, network_type="drive")