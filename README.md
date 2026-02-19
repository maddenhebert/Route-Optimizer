# WGUPS Routing Program

A Python-based package delivery routing system implementing a greedy nearest-neighbor algorithm.

## Features
- A-Star Algorithm with MST Heuristics* – Optimized pathfinding with admissible heuristics for guaranteed optimality
- Real-World Network Integration – Actual road topology from OpenStreetMap with realistic distance/time calculations
- Route Visualization - Most efficient route visualized on a plot using matplotlib

## Project Structure
- logistics/ – Core routing algorithms (A*, distance matrix computation, heuristic functions)
- objects/ – Stop object for nodes

## How to Run
python main.py