# Graph Algorithm Visualizer (Flask)

A lightweight, interactive **graph algorithm visualizer** built with **Flask**, **HTML5 Canvas**, and **vanilla JavaScript**.  
It supports graph editing, weighted edges, step-by-step algorithm playback, and flow network visualization.

This project is designed to be simple, hackable, and educational — perfect for learning or demonstrating BFS, DFS, Dijkstra, A*, and Max-Flow algorithms.

---

## 🚀 Features

### ✅ Graph Editing
- Double‑click canvas to add nodes  
- Click‑drag nodes to reposition  
- Click two nodes to create an edge  
- Automatic prompts for:
  - **Weights** (Dijkstra, A*)  
  - **Capacities** (Flow networks)

### ✅ Algorithm Support
- **BFS** (with step-by-step queue visualization)
- **DFS**
- **Dijkstra’s Algorithm**
- **A\*** (heuristic-ready)
- **Edmonds–Karp Max Flow**

### ✅ Step-by-Step Playback Controls
- ▶ **Play**
- ⏸ **Pause**
- ◀ **Step Back**
- ▶ **Step Forward**
- Automatic highlighting of:
  - Current node
  - Visited nodes

### ✅ Flask Backend
- `/run` — full algorithm result  
- `/run_steps` — detailed step-by-step states  
- Clean separation of algorithm logic in `algorithms/` directory

---

## 📁 Project Structure

graph-visualizer/
│
├── app.py
├── algorithms/
│   ├── bfs.py
│   ├── dfs.py
│   ├── dijkstra.py
│   ├── astar.py
│   └── flows.py
│
├── templates/
│   └── index.html
│
└── static/
├── js/
│   ├── api.js
│   └── graph.js
└── css/
└── styles.css

---

## 🛠 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourname/graph-visualizer.git
cd graph-visualizer