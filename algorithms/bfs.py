from collections import deque

def run(graph, start, goal=None):
    """
    Standard BFS that returns final visited order and path.
    """
    # Build adjacency list
    adj = {n: [] for n in graph["nodes"]}
    for e in graph["edges"]:
        adj[e["from"]].append(e["to"])

    visited = []
    queue = deque([start])
    parent = {start: None}

    while queue:
        node = queue.popleft()
        visited.append(node)

        if node == goal:
            break

        for neighbor in adj[node]:
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)

    # Reconstruct path if goal exists
    path = []
    if goal and goal in parent:
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()

    return {
        "visited": visited,
        "path": path
    }


def run_steps(graph, start, goal=None):
    """
    BFS generator that yields step-by-step states for animation.
    """
    # Build adjacency list
    adj = {n: [] for n in graph["nodes"]}
    for e in graph["edges"]:
        adj[e["from"]].append(e["to"])

    visited = set()
    queue = deque([start])
    parent = {start: None}

    while queue:
        node = queue.popleft()
        visited.add(node)

        # Yield the current BFS state
        yield {
            "current": node,
            "visited": list(visited),
            "queue": list(queue),
            "parent": parent.copy()
        }

        if node == goal:
            break

        for neighbor in adj[node]:
            if neighbor not in parent:
                parent[neighbor] = node
                queue.append(neighbor)
