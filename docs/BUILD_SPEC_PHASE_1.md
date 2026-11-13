# Phase 1 — R7.1 Foundation and Read-Only Scene Inspector

## Current scope and authorization
**Target 3DEqualizer version: R7.1 only.** R8.0 and R8.1 are explicitly out of scope for this phase. Existing comparison tables may remain as historical research, but they must not drive implementation or acceptance criteria.

The immediate task is a READ-ONLY audit of the existing prototype scripts against the official R7.1 API documentation. Do not write or modify implementation code until the owner explicitly approves the audit outcome and a specific implementation task.

## R7.1 API requirements
Maintain:
- `docs/API_REFERENCE.md`
- `docs/API_EXAMPLES.md`
- `docs/VERSION_COMPATIBILITY.md` (simplify active acceptance criteria to R7.1; clearly label R8.x material as historical/out of scope).

For every API used by the R7.1 implementation, record the exact documented function name/signature, arguments, documented return, source location, and any semantic gaps. Never invent APIs or rely on R8.x-only documentation for R7.1.

Focus on version detection, cameras, frame/sequence metadata, lenses, point groups, points, 2D observations, calculated 3D positions, survey data, and native Custom Requester UI where documented for R7.1.

## Existing prototype audit
Audit these existing files without changing them:
- `scripts/scene_inspector.py`
- `scripts/kikz_toolkit.py`

Check every API call against R7.1 documentation, calculated-3D status handling, read-only safety, exception handling, R7.1 UI behavior assumptions, and whether each UI action/help control is functional or merely a placeholder.

Write findings to `docs/CODE_AUDIT_REPORT.md`. This is a report-only task.

## Intended Scene Inspector behavior (future implementation; not yet authorized)
1. Detect the running R7.1 version using a documented API.
2. Inspect cameras and documented metadata: frame count, sequence attributes, FPS, and lens assignment.
3. Inspect point groups, their types, enabled states, and point counts.
4. Inspect point names and calculated 3D / survey information only when safely available.
5. Offer optional deep tracking inspection using documented 2D observation validity and position APIs.
6. Produce a readable report in the native UI and/or an explicitly selected output location. Never silently write files.
7. Handle unavailable APIs and individual item errors gracefully.
8. Never modify scene data.

## UI direction (future implementation; not yet authorized)
Use native 3DE R7.1 Custom Requester UI after checking its exact R7.1 signatures. Initial entries: Scene Inspector, Quick Inspection, Deep Inspection, API Reference. Every entry must have a nearby `!` help control explaining What / When / How / Inputs / Output / Safety. Do not ship placeholder controls.

## Test and acceptance plan
- Static syntax validation using an interpreter compatible with the installed R7.1 Python environment, without changing that environment.
- Mocked tests for pure helpers where useful; label them as mocked.
- In-application read-only smoke tests inside **3DEqualizer R7.1 only** when available.
- Record exact interpreter, application version, commands, results, and limitations.
- Never claim in-app testing unless it actually ran inside R7.1.

## Stop conditions
Stop and report if an API signature cannot be verified for R7.1, if behavior would require undocumented assumptions, if a file/path conflict appears, or if a change would touch protected exporter/importer code, another project, dependencies, PATH, the Python environment, or a production scene.
