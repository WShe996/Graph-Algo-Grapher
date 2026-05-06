// ------------------------------------------------------------
// Canvas + UI Elements
// ------------------------------------------------------------
const canvas = document.getElementById("graph-canvas");
const ctx = canvas.getContext("2d");

const algorithmSelect = document.getElementById("algorithm");
const startInput = document.getElementById("start-node");
const goalInput = document.getElementById("goal-node");
const runStepsBtn = document.getElementById("run-steps");

const stepForwardBtn = document.getElementById("step-forward");
const stepBackBtn = document.getElementById("step-back");
const playBtn = document.getElementById("play");
const pauseBtn = document.getElementById("pause");

// ------------------------------------------------------------
// Graph Model
// ------------------------------------------------------------
let graph = {
    nodes: [],   // [{ id, x, y }]
    edges: []    // [{ from, to, weight, capacity }]
};

let selectedNode = null;
let draggingNode = null;

// ------------------------------------------------------------
// Drawing
// ------------------------------------------------------------
function drawGraph(highlight = {}) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw edges
    graph.edges.forEach(e => {
        const from = graph.nodes.find(n => n.id === e.from);
        const to = graph.nodes.find(n => n.id === e.to);
        if (!from || !to) return;

        ctx.strokeStyle = "#555";
        ctx.lineWidth = 2;

        ctx.beginPath();
        ctx.moveTo(from.x, from.y);
        ctx.lineTo(to.x, to.y);
        ctx.stroke();

        // Draw weight/capacity label
        if (e.weight != null || e.capacity != null) {
            const label = e.weight != null ? e.weight : e.capacity;
            const mx = (from.x + to.x) / 2;
            const my = (from.y + to.y) / 2;
            ctx.fillStyle = "black";
            ctx.fillText(label, mx, my);
        }
    });

    // Draw nodes
    graph.nodes.forEach(n => {
        const radius = 18;
        const isVisited = highlight.visited?.has(n.id);
        const isCurrent = highlight.current === n.id;

        ctx.beginPath();
        ctx.arc(n.x, n.y, radius, 0, 2 * Math.PI);
        ctx.fillStyle = isCurrent ? "orange" : (isVisited ? "#88c" : "#ccc");
        ctx.fill();
        ctx.strokeStyle = "#333";
        ctx.stroke();

        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(n.id, n.x, n.y);
    });
}

// ------------------------------------------------------------
// Node Creation + Dragging
// ------------------------------------------------------------
canvas.addEventListener("dblclick", e => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const id = prompt("Node id:");
    if (!id) return;

    graph.nodes.push({ id: String(id), x, y });
    drawGraph();
});

canvas.addEventListener("mousedown", e => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    draggingNode = graph.nodes.find(n => {
        const dx = n.x - x;
        const dy = n.y - y;
        return dx * dx + dy * dy <= 18 * 18;
    });
});

canvas.addEventListener("mousemove", e => {
    if (!draggingNode) return;

    const rect = canvas.getBoundingClientRect();
    draggingNode.x = e.clientX - rect.left;
    draggingNode.y = e.clientY - rect.top;

    drawGraph();
});

canvas.addEventListener("mouseup", () => {
    draggingNode = null;
});

// ------------------------------------------------------------
// Edge Creation
// ------------------------------------------------------------
canvas.addEventListener("click", e => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const node = graph.nodes.find(n => {
        const dx = n.x - x;
        const dy = n.y - y;
        return dx * dx + dy * dy <= 18 * 18;
    });

    if (!node) return;

    if (!selectedNode) {
        selectedNode = node;
        return;
    }

    if (selectedNode.id !== node.id) {
        let weight = null;
        let capacity = null;

        const algo = algorithmSelect.value;

        if (algo === "dijkstra" || algo === "astar") {
            weight = Number(prompt("Edge weight:", "1")) || 1;
        } else if (algo === "flow") {
            capacity = Number(prompt("Edge capacity:", "1")) || 1;
        }

        graph.edges.push({
            from: String(selectedNode.id),
            to: String(node.id),
            weight: weight ?? null,
            capacity: capacity ?? null
        });
    }

    selectedNode = null;
    drawGraph();
});

// ------------------------------------------------------------
// Step System
// ------------------------------------------------------------
let steps = [];
let currentStep = 0;
let playing = false;
let playInterval = null;

function renderStep() {
    if (!steps.length) return;

    const step = steps[currentStep];
    const visited = new Set(step.visited || []);
    const current = step.current || null;

    drawGraph({ visited, current });
}

function stepForward() {
    if (currentStep < steps.length - 1) {
        currentStep++;
        renderStep();
    }
}

function stepBack() {
    if (currentStep > 0) {
        currentStep--;
        renderStep();
    }
}

function play() {
    if (playing) return;
    playing = true;

    playInterval = setInterval(() => {
        if (currentStep >= steps.length - 1) {
            pause();
            return;
        }
        stepForward();
    }, 600);
}

function pause() {
    playing = false;
    clearInterval(playInterval);
}

// ------------------------------------------------------------
// Run Algorithm
// ------------------------------------------------------------
runStepsBtn.addEventListener("click", async () => {
    pause();

    const algorithm = algorithmSelect.value;
    const start = startInput.value || null;
    const goal = goalInput.value || null;

    const payloadGraph = {
        nodes: graph.nodes.map(n => n.id),
        edges: graph.edges.map(e => ({
            from: e.from,
            to: e.to,
            weight: e.weight,
            capacity: e.capacity
        }))
    };

    console.log("Payload graph:", payloadGraph);

    const result = await fetchSteps(algorithm, payloadGraph, start, goal);

    steps = result.steps || [];
    currentStep = 0;

    console.log("Steps returned:", steps);

    renderStep();
});

// ------------------------------------------------------------
// Default Graph
// ------------------------------------------------------------
graph = {
    nodes: [
        { id: "A", x: 150, y: 150 },
        { id: "B", x: 350, y: 100 },
        { id: "C", x: 350, y: 250 },
        { id: "D", x: 550, y: 150 },
        { id: "E", x: 550, y: 300 },
        { id: "F", x: 750, y: 200 },
        { id: "G", x: 800, y: 150 }
    ],

    edges: [
        // A branching start
        { from: "A", to: "B", weight: 4 },
        { from: "A", to: "C", weight: 2 },

        // B branch
        { from: "B", to: "D", weight: 7 },
        { from: "B", to: "C", weight: 1 },   // cheap back-edge

        // C branch
        { from: "C", to: "D", weight: 3 },
        { from: "C", to: "E", weight: 10 },  // misleading expensive path

        // D branch
        { from: "D", to: "E", weight: 2 },
        { from: "D", to: "F", weight: 8 },

        // E branch
        { from: "E", to: "F", weight: 2 },

        // F to goal
        { from: "F", to: "G", weight: 1 },

        // A cycle to test correctness
        { from: "E", to: "B", weight: 6 }
    ]
};




drawGraph();

// ------------------------------------------------------------
// Button Wiring
// ------------------------------------------------------------
stepForwardBtn.addEventListener("click", () => { pause(); stepForward(); });
stepBackBtn.addEventListener("click", () => { pause(); stepBack(); });
playBtn.addEventListener("click", () => play());
pauseBtn.addEventListener("click", () => pause());
