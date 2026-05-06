import heapq
import sys

def run(graph, start, goal):
    """
    Standard Dijkstra's that returns final shortest distances from the start node.
    """
    # Build adjacency list
    adj = {n: [] for n in graph["nodes"]}
    for e in graph["edges"]:
        adj[e["from"]].append((e["to"], e["weight"]))

    V = lein(adj)
    pq = []
    parent = {start: None}
    visited = []

    dist = {n: sys.maxsize for n in graph["nodes"]}

    dist[start] = 0
    heapq.heappush(pq, (0,start))

    while pq:
        d, u = heapq.heappop(pq)

        if u in visited:
            continue
        visited.append(u)

        if d > dist[u]:
            continue

        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    # Reconstruct Path if goal exists
    path = []
    if goal and goal in parent:
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()

    return {
        "distances": dist,
        "visited": visited,
        "path": path
    }

def run_steps(graph, start, goal=None):
    """
    step by step Dijkstra generator for animation.
    Yields snapshots after each node is popped from the priority queue.
    """

    # Build adjacency list with weights
    adj = {n: [] for n in graph["nodes"]}
    for e in graph["edges"]:
        adj[e["from"]].append((e["to"], e["weight"]))

    dist = {n: sys.maxsize for n in graph["nodes"]}
    parent = {start: None}
    visited = []

    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)

        if u in visited:
            continue
        visited.append(u)

        yield {
            "current": u,
            "visited": list(visited),
            "queue": list(pq),
            "dist": dist.copy(),
            "parent": parent.copy()
        }

        if goal and u == goal:
            break

        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

