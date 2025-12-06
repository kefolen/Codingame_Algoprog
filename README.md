# Moon Tubes Optimizer (Codingame Fall 2024)

## Short solution description

To search the space of tube layouts, the code uses a Simulated Annealing strategy seeded by a greedy heuristic:
- Start from a fast greedy baseline that connects near, high-value pairs while respecting constraints.
- Iteratively apply local moves (add/remove/swap a tube, reroute small neighborhoods), accepting better moves and occasionally accepting worse ones according to a cooling schedule.
- Keep the best-so-far solution and restart when stuck to escape local optima.

This combination gives a good tradeoff between solution quality and runtime under contest constraints.

## Project structure
- `Greed.py` — fast greedy initializer and utility routines for geometry/intersections.
- `DSU.py` — disjoint-set (union-find) helpers to keep components connected and avoid cycles where needed.
- `Proper dist.py` — distance and pathfinding utilities (e.g., Dijkstra variants) used in scoring and neighbor generation.
- `Test_snippets.py` — playground with alternative heuristics, geometric primitives, and I/O parsing helpers.
- `debug_inp.py` — local input helpers for quick testing.

## Provenance
- This `README.md` was AI-generated.
- All other source files in this repository are hand-written.