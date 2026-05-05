from collections import deque
import copy

def run(graph):
    # expects: graph["nodes"], graph["edges"], graph["source"], graph["sink"]
    source = graph["source"]
    sink = graph["sink"]

    capacity = {}
    for e in graph["edges"]:
        u, v, c = e["from"], e["to"], e["capacity"]
        capacity[(u, v)] = capacity.get((u, v), 0) + c
        capacity.setdefault((v, u), 0)

    flow = {edge: 0 for edge in capacity}
    max_flow = 0

    while True:
        parent = {source: None}
        q = deque([source])

        while q and sink not in parent:
            u = q.popleft()
            for v in graph["nodes"]:
                if (u, v) in capacity and v not in parent and capacity[(u, v)] - flow[(u, v)] > 0:
                    parent[v] = u
                    q.append(v)

        if sink not in parent:
            break

        # bottleneck
        increment = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            increment = min(increment, capacity[(u, v)] - flow[(u, v)])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            flow[(u, v)] += increment
            flow[(v, u)] -= increment
            v = u

        max_flow += increment

    return {"max_flow": max_flow, "flow": {str(k): v for k, v in flow.items()}}

def run_steps(graph):
    source = graph["source"]
    sink = graph["sink"]

    capacity = {}
    for e in graph["edges"]:
        u, v, c = e["from"], e["to"], e["capacity"]
        capacity[(u, v)] = capacity.get((u, v), 0) + c
        capacity.setdefault((v, u), 0)

    flow = {edge: 0 for edge in capacity}
    max_flow = 0

    while True:
        parent = {source: None}
        q = deque([source])

        while q and sink not in parent:
            u = q.popleft()
            for v in graph["nodes"]:
                if (u, v) in capacity and v not in parent and capacity[(u, v)] - flow[(u, v)] > 0:
                    parent[v] = u
                    q.append(v)

        if sink not in parent:
            break

        path = []
        v = sink
        while v is not None:
            path.append(v)
            v = parent[v]
        path.reverse()

        increment = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            increment = min(increment, capacity[(u, v)] - flow[(u, v)])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            flow[(u, v)] += increment
            flow[(v, u)] -= increment
            v = u

        max_flow += increment

        yield {
            "augmenting_path": path,
            "increment": increment,
            "max_flow": max_flow,
            "flow": {str(k): v for k, v in flow.items()}
        }
