"""Simple text/table workflow."""

from __future__ import annotations

import time

from renderflow import Workflow, emit_progress, wrap_with_timing


workflow = Workflow(
    name="Greeting",
    description="Minimal text + table output example.",
)

workflow.params = {
    "name": {
        "type": "text",
        "label": "Name",
        "default": "World",
    },
    "excited": {
        "type": "checkbox",
        "label": "Excited",
        "default": False,
        "help": "Add exclamation marks to the greeting.",
    },
    "repeat": {
        "type": "number",
        "label": "Repeat Count",
        "default": 2,
        "min": 1,
        "max": 10,
        "step": 1,
    },
}


def run_workflow(metadata=None, **kwargs):
    wf = workflow.clear()
    metadata = metadata or {}

    emit_progress(metadata, "Parse Inputs", "running", "Resolve workflow parameters")
    name = str(metadata.get("name", "World"))
    excited = bool(metadata.get("excited", False))
    repeat = int(metadata.get("repeat", 2))
    emit_progress(metadata, "Parse Inputs", "done", "Resolve workflow parameters")

    def _build_lines(inputs):
        time.sleep(0.12)
        n = inputs["name"]
        ex = inputs["excited"]
        rep = max(1, int(inputs["repeat"]))
        suffix = "!" if ex else "."
        return {"lines": [f"Hello, {n}{suffix}" for _ in range(rep)]}

    line_result = wrap_with_timing(
        _build_lines,
        label="Build Greeting Lines",
        description="Generate repeated greeting text",
        metadata=metadata,
    )({"name": name, "excited": excited, "repeat": repeat})
    lines = line_result["lines"]

    emit_progress(metadata, "Assemble Results", "running", "Add text and table outputs")
    wf.add_text(lines)
    wf.add_table(
        "Input Summary",
        {
            "key": ["name", "excited", "repeat"],
            "value": [name, excited, repeat],
        },
    )
    emit_progress(metadata, "Assemble Results", "done", "Add text and table outputs")
    return wf.build()
