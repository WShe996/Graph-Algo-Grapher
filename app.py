from flask import Flask, render_template, request, jsonify
from algorithms import bfs, dfs, dijkstra, astar, flows

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_algorithm():
    data = request.json
    graph = data["graph"]
    start = data.get("start")
    goal = data.get("goal")
    algo = data["algorithm"]

    if algo == "bfs":
        result = bfs.run(graph, start, goal)
    elif algo == "dfs":
        result = dfs.run(graph, start, goal)
    elif algo == "dijkstra":
        result = dijkstra.run(graph, start, goal)
    elif algo == "astar":
        result = astar.run(graph, start, goal)
    elif algo == "flow":
        result = flows.run(graph)
    else:
        return jsonify({"error": "Unknown algorithm"}), 400

    return jsonify(result)

@app.route("/run_steps", methods=["POST"])
def run_algorithm_steps():
    data = request.json
    graph = data["graph"]
    start = data.get("start")
    goal = data.get("goal")
    algo = data["algorithm"]

    if algo == "bfs":
        steps = list(bfs.run_steps(graph, start, goal))
    elif algo == "dfs":
        steps = list(dfs.run_steps(graph, start, goal))
    elif algo == "dijkstra":
        steps = list(dijkstra.run_steps(graph, start, goal))
    elif algo == "astar":
        steps = list(astar.run_steps(graph, start, goal))
    elif algo == "flow":
        steps = list(flows.run_steps(graph))
    else:
        return jsonify({"error": "Unknown algorithm"}), 400

    return jsonify({"steps": steps})

if __name__ == "__main__":
    app.run(debug=True)
