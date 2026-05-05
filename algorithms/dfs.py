def run(graph, start, goal=None):
    """
    Standard DFS that returns final visited order and path
    """
    # Build adjacency list
    adj = {n: [] for n in graph["nodes"]}
    for e in graph["edges"]:
        adj[e["from"]].append(e["to"])

    visited = []
    stack = [start]
    parent = {start: None}

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.append(node)

            if node == goal:
                break

        for v in reversed(adj[node]):
            if v not in visited:
                parent[v] = node
                stack.append(v)

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
    DFS generator that yields step-by-step states for animation
    """
    #build adjacency list
    adj = {n: [] for n in graph["nodes"]}
    for e in graph["edges"]:
        adj[e["from"]].append(e["to"])

    visited = set()
    stack = [start]
    parent = {start: None}

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)

            yield {
                "current": node,
                "visited": list(visited),
                "stack": list(stack),
                "parent": parent.copy()
            }

            if node == goal:
                break

            for v in reversed(adj[node]):
                if v not in visited:
                    parent[v] = node
                    stack.append(v)
    
