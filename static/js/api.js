async function fetchSteps(algorithm, graph, start, goal) {
    const res = await fetch("/run_steps", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ algorithm, graph, start, goal })
    });
    return res.json();
}
