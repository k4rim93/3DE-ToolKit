# 3DE-ToolKit
Professional multi-version Python toolkit for 3DEqualizer matchmove workflows

## Phase 1 status

The read-only Scene Inspector foundation is under implementation on the feature branch. It reports camera metadata, point-group states, and point counts. Deep point and current-frame observation details are enabled only in R8.1, where the official structured API contract documents how to request all points. R7.1 and R8.0 deep enumeration remains disabled until the accepted selector semantics are independently verified for those releases.

## Supported releases

- 3DEqualizer R7.1
- 3DEqualizer R8.0
- 3DEqualizer R8.1

The common overview calls are documented in the vendor command summary for each version. Actual behavior has not yet been smoke-tested inside these applications. See [version compatibility](docs/VERSION_COMPATIBILITY.md) and the [API reference](docs/API_REFERENCE.md) for exact coverage and unresolved details.

## Install and use

Copy `scripts/scene_inspector.py` and `scripts/kikz_toolkit.py` together into an existing 3DE custom Python scripts folder, then use the **Kikz Toolkit** menu. The scripts add Scene Inspector, Quick Inspection, Deep Inspection, API Reference, and a neighboring `!` help entry for each tool.

The report appears in a native requester. This version does not write report files. Deep Inspection is opt-in and checks point values and 2D observations at each camera's current frame; it does not move the current frame.

## Safety and limits

- The inspector uses getters and UI presentation calls only. It does not change scene data, selection, camera, frame, lenses, points, or project state.
- No third-party packages are required.
- Individual unavailable APIs or item errors are shown as partial-result diagnostics.
- R7.1/R8.0 deep point enumeration is disabled rather than using an undocumented selector value.
- The exact version-string format, UI appearance, and in-application behavior still need validation in each supported release.
- Never use production or client scene data as public test fixtures.

## Validation

No static syntax checks, mocked tests, or in-application tests have been run for the current implementation. Do not treat this toolkit as validated in any 3DE version until the exact smoke tests and results are recorded.

## Documentation

- [Phase 1 inspection report](docs/PHASE1_INSPECTION_REPORT.md)
- [API reference](docs/API_REFERENCE.md)
- [Version compatibility](docs/VERSION_COMPATIBILITY.md)
- [API examples](docs/API_EXAMPLES.md)
- [Changelog](CHANGELOG.md)
