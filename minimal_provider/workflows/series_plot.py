"""Simple plot workflow."""

from __future__ import annotations

import time

import plotly.graph_objects as go

from renderflow import Workflow, emit_progress, wrap_with_timing

workflow = Workflow(
    name="Series Plot",
    description="Minimal workflow that returns text, table, and one plot.",
)

workflow.params = {
    "base_value": {
        "type": "number",
        "label": "Base Value",
        "default": 10,
        "min": -1000,
        "max": 1000,
        "step": 1,
    },
    "points": {
        "type": "number",
        "label": "Number of Points",
        "default": 6,
        "min": 2,
        "max": 30,
        "step": 1,
    },
    "scale": {
        "type": "number",
        "label": "Scale",
        "default": 1.5,
        "min": 0.1,
        "max": 10.0,
        "step": 0.1,
    },
}


def run_workflow(metadata=None, **kwargs):
    wf = workflow.clear()
    metadata = metadata or {}

    emit_progress(metadata, "Parse Inputs", "running", "Read numeric parameters")
    points = int(metadata.get("points", 6))
    scale = float(metadata.get("scale", 1.5))
    base_value = float(metadata.get("base_value", 10))
    emit_progress(metadata, "Parse Inputs", "done", "Read numeric parameters")

    def _compute_series(inputs):
        time.sleep(0.2)
        pts = max(2, int(inputs["points"]))
        x = list(range(pts))
        y = [float(inputs["base_value"]) + (idx * float(inputs["scale"])) for idx in x]
        return {"x_vals": x, "y_vals": y}

    series = wrap_with_timing(
        _compute_series,
        label="Compute Series",
        description="Generate x/y values for plotting",
        metadata=metadata,
    )({"points": points, "scale": scale, "base_value": base_value})
    x_vals = series["x_vals"]
    y_vals = series["y_vals"]

    emit_progress(metadata, "Build Plot", "running", "Create Plotly figure")
    fig = go.Figure(data=[go.Scatter(x=x_vals, y=y_vals, mode="lines+markers", name="series")])
    fig.update_layout(title="Sample Series", xaxis_title="Index", yaxis_title="Value")
    emit_progress(metadata, "Build Plot", "done", "Create Plotly figure")

    emit_progress(metadata, "Assemble Results", "running", "Add text, table, and plot outputs")
    wf.add_text(f"Generated {points} points with base={base_value} and scale={scale}.")
    wf.add_table(
        "Series Data",
        {
            "x": x_vals,
            "y": y_vals,
        },
    )
    wf.add_plot(fig)
    emit_progress(metadata, "Assemble Results", "done", "Add text, table, and plot outputs")
    return wf.build()
