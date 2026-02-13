# Minimal Provider Example

This is a tiny provider package that demonstrates the `renderflow` API with:
- two workflows under `minimal_provider.workflows`
- workflow params automatically discovered from `workflow.params`
- live step progress using `renderflow.progress.emit_progress` and `wrap_with_timing`

## Install

From this repo root:

```bash
uv venv --python 3.11 .venv
source .venv/bin/activate
uv pip install -e .
```

## Run

List providers:

```bash
renderflow list-providers
```

List example workflows:

```bash
renderflow list-workflows --provider minimal-provider
```

Show parameters:

```bash
renderflow show-params --provider minimal-provider --workflow greeting
```

Execute with terminal output:

```bash
renderflow execute \
  --provider minimal-provider \
  --workflow greeting \
  --param name=Ada \
  --param excited=true
```

Execute with combined report plus per-figure exports:

```bash
renderflow execute \
  --provider minimal-provider \
  --workflow series_plot \
  --param base_value=12 \
  --param points=8 \
  --html output/minimal_report.html \
  --save-figures-dir output/minimal_figures \
  --figure-format html \
  --figure-format json
```

Run Streamlit:

```bash
renderflow run --provider minimal-provider
```

Or run the included app entrypoint directly:

```bash
streamlit run app.py
```

## Streamlit Community Cloud

This provider can be deployed as a `.streamlit.app`.

Required files are included:
- `app.py` (Streamlit entrypoint)
- `minimal_provider/...` (provider package)
- `pyproject.toml` (runtime dependencies + entrypoint registration)

Deployment steps:
1. Push this repo to GitHub.
2. In Streamlit Community Cloud, create a new app from this repo.
3. Set main file path to `app.py`.
4. Deploy.

Notes:
- This example does not use `app_definition.py`.
- `pyproject.toml` pins `renderflow` from GitHub `main`.
- Image export formats (`png/jpg/svg/pdf`) require `kaleido` (already listed).

## API Summary

Provider package contract used here:
- `minimal_provider/renderflow.py`
  - `APP_NAME`
  - `WORKFLOWS_PACKAGE`
- `minimal_provider/workflows/*.py`
  - `workflow = Workflow(name=..., description=...)`
  - `workflow.params = {...}`
  - `run_workflow(...) -> workflow.build()`

No custom CLI or custom renderer is needed in the provider.

Progress helpers:
- `emit_progress(metadata, step, status, detail)` emits step events to the Streamlit status panel.
- `wrap_with_timing(fn, ...)` wraps a function, emits progress events, and appends timing metadata.
