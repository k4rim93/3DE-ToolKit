# R7.1 Experimental Build — User Test Plan

**Status:** Experimental; owner validation required.
**Target:** 3DEqualizer R7.1 only.
**Branch:** `feature/r71-inspector-experimental`

## Files to install together

- `scripts/kikz_toolkit.py`
- `scripts/scene_inspector.py`

Keep both files in the same 3DE custom Python scripts directory. Do not rename either file. Refresh/reload the script menu using the normal 3DE workflow.

## First test: safe overview

1. Open a copy of a non-critical R7.1 project (do not use a live production scene for the first test).
2. Run **Scene Inspector**.
3. Confirm the report identifies R7.1 and lists camera and point-group counts.
4. Run **Quick Inspection** and confirm it returns the compact overview.
5. Open each `!` help entry and confirm it shows the matching help text.
6. Open **API Reference** and confirm it describes R7.1 only.

## Second test: Deep Inspection

1. Use a non-critical scene containing several point groups and points.
2. Run **Deep Inspection**.
3. Confirm the report includes each point group's count and the point-level results.
4. Check that each point has a calculated-3D status. For `NOT_CALCULATED`, the report must say so and must not show a fetched calculated coordinate.
5. Confirm valid 2D observations show positions only when the validity getter returns `1`.
6. If a point group is skipped because `getPointList(..., 0)` count does not match `getNoPoints`, keep the diagnostic text; do not bypass the guard or alter the scene.

## Safety checks

- No point, camera, lens, frame, group, or scene values should change.
- No calculation should start.
- No files should be written by the toolkit.
- No package installation or environment changes are required.

## Send back

Please report:
- Exact 3DE version string shown in the report.
- Whether both scripts appear in the menu and each menu/help item opens.
- Whether the requester opens, displays the full report, scrolls, and closes normally.
- Whether overview counts match the scene.
- Whether Deep Inspection lists points, calculated-3D statuses, and current-frame 2D observations.
- Any console traceback or diagnostic message (copy/paste text is better than screenshots).

## Known unverified behavior

The official R7.1 command summary documents the `getPointList(pgroup_id, selected_only)` signature but does not spell out selector value semantics. The experimental build passes `0` as the conventional false value for `selected_only` and cross-checks the returned list length against `getNoPoints`. A mismatch causes that group to be skipped with a diagnostic. This is a guarded experiment, not a claim that the selector contract is fully specified by the summary.

No in-application R7.1 test has been performed by the developer. Requester layout, scrolling, module import resolution, and menu dispatch still require this owner test.
