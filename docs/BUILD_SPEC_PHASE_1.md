# Phase 1 — Foundation and Read-Only Scene Inspector

## Status
Implementation is authorized and in progress on `docs/project-handover-foundation`. The code remains read-only and must follow the verification limits documented in `docs/API_REFERENCE.md` and `docs/VERSION_COMPATIBILITY.md`.

## Deliverables

### A. Verified API reference
Create:
- `docs/API_REFERENCE.md`
- `docs/VERSION_COMPATIBILITY.md`
- `docs/API_EXAMPLES.md`

Research each supported version independently: R7.1, R8.0, and R8.1.

For every API entry used by the implementation, record:
- Exact documented function name and signature.
- Argument meanings and accepted types, where documented.
- Return type / return-value meaning, where documented.
- Version availability.
- Relevant caveats, deprecation status, and error behavior, if documented.
- Official documentation source and version.

Cover only what is needed for the first inspector, then expand carefully: version detection, cameras, frame/sequence metadata, lenses, point groups, points, 2D observations, calculated 3D positions, and survey data where supported.

**Verification rule:** never infer or invent a `tde4` function, signature, argument, or return value. If official documentation is unavailable or ambiguous for a version, mark the item `UNVERIFIED` and do not rely on it in production code.

### B. Scene Inspector
Proposed file: `scripts/scene_inspector.py`

Required behavior:
1. Detect the running 3DE version using a documented API.
2. Inspect cameras and report available camera metadata, frame count / sequence attributes, FPS, and lens assignment where documented.
3. Inspect point groups, their types, enabled states, and point counts where supported.
4. Inspect point names and relevant calculated 3D / survey information where supported.
5. Offer optional deep tracking inspection based on documented 2D observation validity and position APIs.
6. Produce a readable report in the UI and/or a user-selected output location. Do not silently write files.
7. Handle unavailable APIs and individual item errors gracefully; report partial results.
8. Never modify scene data.

### C. Toolkit UI foundation
Proposed file: `scripts/kikz_toolkit.py`

Initial menu:
- Scene Inspector
- Quick Inspection
- Deep Inspection
- API Reference

Use native 3DE Custom Requester UI initially, after verifying the exact requester API for each supported release. Keep UI code version-aware. If a UI capability differs by version, document and gracefully adapt rather than guessing.

Every listed tool has a neighboring `!` help control following the help contract in `PROJECT_HANDOVER.md`.

### D. Documentation and maintenance
Create:
- `README.md` (update only on the feature branch; preserve useful existing content)
- `CHANGELOG.md`
- The API documentation files listed above.

README must explain supported versions, installation/use instructions, safety model, limitations, and which tests were actually run.

## Suggested internal design
- Keep version detection and capability checks separate from inspection logic.
- Build a small compatibility layer around verified APIs only.
- Keep data collection separate from formatting / UI.
- Return structured inspection results before rendering them.
- Isolate per-camera / per-group / per-point errors so one bad item does not abort the report.
- Make deep inspection opt-in because it may take longer on large scenes.

This is a design direction, not permission to invent wrapper behavior or APIs.

## Test plan
- Static syntax validation with an available interpreter compatible with the target 3DE environment.
- Unit tests for pure formatting / normalization helpers using mocked data; do not pretend mocks are in-app tests.
- Compatibility review against the official R7.1, R8.0, and R8.1 docs.
- In-application smoke tests in each version only when those installations are actually available.
- Record exact interpreter, 3DE version, test command, result, and limitations.
- Clearly distinguish static checks, mocked tests, and tests performed inside 3DE.

## Phase 1 acceptance criteria
- All used APIs have verified documentation for the relevant version, or a documented safe fallback.
- R7.1 / R8.0 / R8.1 compatibility behavior is explicit rather than assumed.
- Inspector is read-only and has no hidden scene or environment side effects.
- Missing functions and per-item errors are handled gracefully.
- UI help is available for every tool.
- Tests and untested environments are reported honestly.
- Protected exporter/importer code and unrelated projects remain unchanged.

## Stop conditions
Stop and report instead of proceeding if:
- A required official API signature cannot be verified.
- A requested feature would require undocumented behavior.
- A file/path conflicts with existing project content.
- A change would touch protected exporter/importer scripts or another project.
- A dependency, PATH change, environment modification, or production-scene mutation appears necessary.
