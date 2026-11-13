# Prototype Code Audit — 3DEqualizer R7.1 Only

**Date:** 2026-11-13
**Branch:** `docs/project-handover-foundation`
**Scope:** Read-only audit of `scripts/scene_inspector.py` and `scripts/kikz_toolkit.py` against official R7.1 documentation.
**Implementation status:** No code was modified. No script was run inside 3DE. No runtime validation is claimed.

## Executive summary

The prototype's overview collector uses camera and point-group getters whose names and argument shapes are documented in the R7.1 command summary. Its deep collector has three material R7.1 blockers: it is gated to version text containing `8.1`, it reads calculated 3D coordinates without first checking the documented calculated-status API, and it passes `0` to the `selected_only` argument of `getPointList` even though the R7.1 summary does not define what that value means. The source is not designed to perform deep inspection for the active R7.1 target; the exact runtime outcome of the version-string condition is untested.

The Custom Requester functions and argument shapes used for display are present in the R7.1 summary. This verifies signatures only; the summary does not establish the exact menu-label dispatch, blocking behavior, layout dimensions, text-area rendering, or lifecycle behavior. Those claims need an R7.1 in-application smoke test, which was not performed.

**Readiness:** Prototype is not ready for approval as an R7.1 implementation. The findings below are evidence for a future, separately approved code task; no fixes are included here.

## Scope and method

The audit read the repository instructions and current project documentation, inspected the working branch/tree, and reviewed both prototype files without changing them. API names and signatures were checked against the official [3DEqualizer4 Release 7.1 Python Interface Command Summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r7.1.txt) only. No R8.0/R8.1 documentation was used as evidence. R8.1-specific branches or labels found in the prototype are assessed as out of scope, not validated against another release.

In this report, **VERIFIED** means the R7.1 summary lists that function and its signature/return placeholder. It does not mean the call was executed in R7.1. **UNVERIFIED** means the documentation does not establish the semantic/runtime claim being made. Script line numbers below refer to the checked-in files at this audit commit.

## R7.1 API inventory

| API used by prototype | R7.1 documentation evidence | Status and audit note |
|---|---|---|
| `get3DEVersion()` | `get3DEVersion() → <3de_version>`; lines 79–80 | **VERIFIED** signature. Exact returned text format/parsing behavior is not specified in the summary. |
| `getNoCameras()`; `getFirstCamera()`; `getNextCamera(camera_id)` | `getNoCameras() → <number_of_cameras>`; `getFirstCamera() → <camera_id>`; `getNextCamera(<camera_id>) → <camera_id>`; lines 561–565 | **VERIFIED** signatures/results. End-of-iteration value is not specified. The code's count-bounded traversal avoids relying on a final sentinel; it additionally treats `None` before the count as an early-stop diagnostic. |
| `getCameraName(camera_id)`; `getCameraType(camera_id)`; `getCameraNoFrames(camera_id)`; `getCameraSequenceAttr(camera_id)`; `getCameraFPS(camera_id)`; `getCameraLens(camera_id)` | `getCameraName(<camera_id>) → <name>`; `getCameraType(<camera_id>) → "SEQUENCE"|"REF_FRAME"`; `getCameraNoFrames(<camera_id>) → <number_of_frames>`; `getCameraSequenceAttr(<camera_id>) → [<start>,<end>,<step>]`; `getCameraFPS(<camera_id>) → <double>`; `getCameraLens(<camera_id>) → <lens_id>`; lines 560, 573–582 | **VERIFIED** signatures/results. Detailed range/units and type-specific availability are not specified. |
| `getLensName(lens_id)` | `getLensName(<lens_id>) → <name>`; lines 848–849 | **VERIFIED** signature/result. Behavior when the camera has no usable assigned lens is **UNVERIFIED**. |
| `getNoPGroups()`; `getFirstPGroup()`; `getNextPGroup(pgroup_id)`; `getPGroupName(pgroup_id)`; `getPGroupType(pgroup_id)`; `getPGroupEnabledFlag(pgroup_id)` | `getNoPGroups() → <number_of_pgroups>`; `getFirstPGroup() → <pgroup_id>`; `getNextPGroup(<pgroup_id>) → <pgroup_id>`; `getPGroupName(<pgroup_id>) → <name>`; `getPGroupType(<pgroup_id>) → "CAMERA"|"OBJECT"|"MOCAP"`; `getPGroupEnabledFlag(<pgroup_id>) → 0|1`; lines 481, 483–494 | **VERIFIED** signatures/results; next-item sentinel semantics are not stated. |
| `getCurrentFrame(camera_id)` | `getCurrentFrame(<camera_id>) → <frame>`; line 264 | **VERIFIED** signature/result placeholder. Its use is not reached by the current R7.1 deep path because of the release gate. The summary does not spell out behavior for all camera types. |
| `getPointList(pgroup_id, selected_only)` | `getPointList(<pgroup_id>, <selected_only>) → [<point_id>, ...]`; lines 704–712 | **VERIFIED** function signature and list return shape. The summary does **not** define accepted selector values or whether `0` means all points. Therefore the exact call `getPointList(group_id, 0)` is not semantically verified for R7.1. |
| `getPointName(pgroup_id, point_id)`; `getPointSurveyPosition3D(pgroup_id, point_id)`; `getPointCalcPosition3D(pgroup_id, point_id)`; `getPointSurveyMode(pgroup_id, point_id)` | `getPointName(<pgroup_id>,<point_id>) → <name>`; survey/calc getters → `<vector 3d>`; survey-mode getter → `<survey mode>`; lines 712, 716–724 | **VERIFIED** signatures/result placeholders. Missing/unavailable value behavior, units, and survey meaningfulness are not specified. |
| `getPointCalculated3DStatus(pgroup_id, point_id)` | `getPointCalculated3DStatus(<pgroup_id>, <point_id>) → <point_3d_status>`; enum at line 71; getter at line 813 | **VERIFIED**, but not called by the prototype. Enum values: `NOT_CALCULATED`, `CALCULATED`, `TRIANGULATED`. |
| `isPointPos2DValid(pgroup_id, point_id, camera_id, frame)`; `getPointPosition2D(pgroup_id, point_id, camera_id, frame)` | Validity getter → `0|1`; position getter → `<vector 2d>`; lines 730–736 | **VERIFIED** signatures/results. Frame bounds, invalid-ID behavior, and coordinate conventions are not specified. |
| `createCustomRequester()`; `deleteCustomRequester(requester_id)`; `postCustomRequester(requester_id, title, width, height, label0, ...)` | `createCustomRequester() → <requester id>`; `deleteCustomRequester(<requester id>)` (no result stated); `postCustomRequester(<requester id>, <window title>, <width>, <height>, <label 0>, ...) → <int>`; lines 147–152 | **VERIFIED** signatures. The summary does not define the button mapping or explicitly describe blocking behavior. |
| `addTextAreaWidget(requester_id, widget_name, label, height, editable)`; `appendTextAreaWidgetString(requester_id, widget_name, string)` | Exact argument order shown in lines 210–211; no result stated | **VERIFIED** signatures. Rendering, sizing units, and visual behavior are **UNVERIFIED** without an R7.1 application check. |
| `getLastScriptMenuLabel()` | `getLastScriptMenuLabel() → <menu_label>`; lines 273–275 | **VERIFIED** signature/result placeholder. Whether it returns the exact `name`/`addlabel` value for every menu item invocation is not demonstrated by the summary. |

No lens distortion-model or parameter API is called by these prototype files. The lens behavior presently implemented is limited to reading the assigned lens ID and, if non-`None`, reading its name.

## Findings

### High — calculated 3D position is read without status check

`scripts/scene_inspector.py:150–160` requests `getPointCalcPosition3D` directly for every enumerated point. The official R7.1 summary documents `getPointCalculated3DStatus` and the three status values (`NOT_CALCULATED`, `CALCULATED`, `TRIANGULATED`), but the collector never calls it. A caught exception from the position getter is not a substitute for checking the documented status; a returned vector is currently displayed as calculated data with no status context.

R7.1 evidence: official summary lines 71 and 813 for status; lines 716–719 for survey/calculated position getters. The summary does not explicitly guarantee getter behavior in every status, so even a future status guard should keep item-level error handling and avoid claiming a sentinel contract.

### High — R7.1 deep inspection is disabled by an R8.1 gate

`_version_is_r81()` at `scripts/scene_inspector.py:26–27` checks whether the version string contains `8.1`. `collect_scene()` at lines 207–215 calls deep collection only when that condition is true; otherwise it appends a message that deep inspection is disabled outside R8.1. The exact R7.1 version string is not specified in the command summary, so the behavior inside the application is not runtime-proven. This is explicitly an R8.1-only gate and the deep branch is not designed to run for the newly declared R7.1-only target.

The `Deep Inspection` menu item at `scripts/kikz_toolkit.py:99–100` routes to a call that returns only the overview plus a diagnostic whenever the version string does not contain `8.1`. Its help text says point-level deep details remain disabled for R7.1 (`kikz_toolkit.py:40–46`) while also promising a “detailed” report (`:47`). The action exists and explains a limitation, but it is not designed as a functioning deep inspection for R7.1. Whether the R7.1 application version string meets the condition is an unverified runtime fact.

### High — `getPointList(..., 0)` selector meaning is unverified in R7.1

The R7.1 command summary lists `getPointList(<pgroup_id>, <selected_only>)` returning a point-ID list (lines 708–709) but does not define selector values. The deep collector passes literal `0` at `scripts/scene_inspector.py:144`. No R7.1-only official evidence reviewed here establishes that this returns all points. Since the release gate prevents this call in normal R7.1 flow, the call is currently dormant for the active target; it must not be enabled for R7.1 based on the current documentation alone.

R7.1 also documents `getFirstPoint(pgroup_id)` and `getNextPoint(pgroup_id, point_id, use_gui_order)` (lines 704–706), but the summary does not explain the `use_gui_order` values or termination behavior. These signatures alone do not establish a safe all-points iteration replacement.

### Medium — `getPointCalculated3DStatus` should be reported, not just used as a gate

The documented status distinguishes not-calculated, calculated, and triangulated points. The current report omits that status entirely. In future approved work, the status should be preserved in the result/report; a `NOT_CALCULATED` point should not be presented as having an available calculated coordinate. `CALCULATED`/`TRIANGULATED` should still be guarded by exception handling because the R7.1 summary does not specify absent-data errors or sentinels.

### Medium — 2D validity ordering is correct, but scope is only current-frame

In the deep collector (`scene_inspector.py:136–138, 168–187`), the code reads `getCurrentFrame(camera_id)`, calls `isPointPos2DValid(...)`, and calls `getPointPosition2D(...)` only when `valid == 1`. This ordering matches the R7.1 documented validity and position APIs (summary lines 730–736) and does not change the frame. Coverage is only the current frame for each camera, not a full tracking-curve scan; help text correctly says “at each camera's current frame.” Out-of-range semantics and returned coordinate conventions remain undocumented.

### Low — overview API calls match documented R7.1 signatures

Camera collection at `scene_inspector.py:36–82` uses the R7.1 count/first/next/name/type/frame/sequence/FPS/lens APIs. Point-group collection at `:88–126` uses the documented count/first/next/name/type/enabled/point-count APIs. Iteration is bounded by the count, and API exceptions are recorded per field/item through `_call` rather than aborting the whole report. One caveat: a wrong count or a non-`None` unexpected ID can still produce a partial or misleading result; the summary does not specify identifier validation behavior.

### Medium — the requester call shapes are documented, but UI assumptions are not

`show_report()` (`scene_inspector.py:286–309`) uses R7.1-documented create/delete, text-area, append, and post calls with matching argument counts/order. The returned integer from `postCustomRequester` is intentionally ignored, avoiding an undocumented button-index interpretation. Cleanup is attempted in `finally` after requester creation.

The following remain **UNVERIFIED** against R7.1 application behavior: whether `postCustomRequester` blocks until close; whether width/height and text-area height values are pixels or otherwise; whether `editable=0` presents the desired read-only widget; whether the report text fits/scrolls; and whether deleting the requester after every early-return/error path behaves as expected. The function names/signatures alone cannot confirm these UI outcomes. Consequently the help text's claims of a native requester as expected output (`kikz_toolkit.py:24–30`) and compact native report (`:32–38`) are source descriptions, not verified R7.1 behavior.

### Medium — menu/help entries exist in source, dispatch needs R7.1 validation

The R7.1 scripting summary documents `3DE4.script.name`, `3DE4.script.addlabel`, and GUI tags (lines 15–23). Source defines a script name plus additional menu labels in `kikz_toolkit.py:1–8`; each listed tool has a `!` help label. `_HELP` has entries for Scene Inspector, Quick Inspection, Deep Inspection, and API Reference (`:23–59`), and `main()` routes labels ending in ` !` to their help text (`:76–85`). Static inspection therefore finds real help text/actions for every declared menu item, rather than empty placeholder callbacks.

However, the exact label returned by `getLastScriptMenuLabel`, association of `script.name` with the main action, addlabel ordering/adjacency, and the live R7.1 menu dispatch are not proven by the command summary and were not tested in-app. The `API Reference` action displays content, but its text at `kikz_toolkit.py:86–95` advertises R8.0/R8.1 and R8.1-only details, contradicting the active R7.1-only project scope. Unknown non-help labels fall through to the default full overview (`:80–84, :99–102`), so exact dispatch matters. The Deep Inspection help also overstates the output as detailed for R7.1 when the branch is gated off.

`kikz_toolkit.py` imports `scene_inspector` by module name (`:17–20`), and its help says both files must be installed together (`:72–74`). Whether the R7.1 embedded script loader makes the sibling module importable from that location is not established in the command summary and was not checked in-app. If this import fails, `main()` exits before any menu action runs.

### Low — read-only safety is supported by static inspection

The reviewed scripts contain getter calls, formatting/printing, imports, and Custom Requester presentation calls. No setter, calculation command, scene selection/frame setter, file write, dependency install, PATH/environment change, or network call was found. `getCurrentFrame` is a getter; no `setCurrentFrame` is used. Thus the code is **statically consistent with read-only intent**. This is not runtime proof that the host's UI presentation has no side effects, and it is not a 3DE execution test.

### Medium — error isolation is useful but not complete

`_call()` catches API exceptions and reports missing functions; count conversion is guarded; camera/group iteration is count-bounded; requester cleanup is in `finally`. These are positive safeguards. Unhandled non-API data-shape cases remain: for example, a non-iterable `point_ids` return or a malformed container can escape `_collect_deep_r81`; a zero/negative or unexpected count can silently yield incomplete output. R7.1 docs do not define such malformed return behavior. There is no outer boundary around `collect_scene()` in `run_inspection()` to convert arbitrary Python-side errors into a partial report.

### Low — API Reference action and repository copy are stale for active scope

The toolkit's API Reference menu action still says the tool verifies R7.1, R8.0 and R8.1 and discusses R8.1 selector semantics. The top-level README and historical API/compatibility docs also retain multi-version messaging. The current task explicitly scopes implementation/audit to R7.1 only. These stale messages are report findings only; this audit does not edit code or other documents.

## R7.1 readiness checklist

| Area | Audit result |
|---|---|
| Overview camera APIs | Signatures VERIFIED in R7.1 documentation; no in-app test. |
| Overview point-group APIs | Signatures VERIFIED in R7.1 documentation; no in-app test. |
| Lens assignment/name | Signatures VERIFIED; missing-lens behavior UNVERIFIED; no distortion-model inspection implemented. |
| Point enumeration for deep mode | R7.1 signature exists, but `selected_only=0` meaning UNVERIFIED; do not rely on it. Iteration alternative's argument semantics also need evidence. |
| Calculated 3D | Status getter documented but not used; current direct coordinate read is not safe to rely on. |
| Survey data | Getter signatures documented; meaningfulness/units/absent-value behavior UNVERIFIED. |
| 2D tracking | Validity-before-position sequence is correct for one current frame; full-frame tracking not implemented. |
| Custom Requester | R7.1 signatures match; visual/lifecycle/blocking behavior UNVERIFIED. |
| Menus/help | Static source routes each declared label and has nonempty help; exact R7.1 menu dispatch untested; some displayed claims are stale. |
| Read-only safety | No scene mutation/file/network API found in static review; not runtime validated. |

## Remaining blockers before code approval

1. Define a R7.1-supported point enumeration method with documented selector/iteration semantics. The R7.1 command summary alone does not resolve `getPointList(..., 0)` or `getNextPoint(..., use_gui_order)` semantics.
2. Require calculated-status handling before reading/displaying calculated coordinates; preserve the status in output and continue to report getter failures.
3. Make the Deep Inspection R7.1 behavior truthful: either it performs verified deep inspection or the UI clearly presents it as unavailable/diagnostic until that is resolved.
4. Remove or scope out the R8.0/R8.1 claims and R8.1-only gate from user-facing active-target messaging in a future approved code/documentation task.
5. Run static syntax validation with the already-installed R7.1-compatible interpreter if available, then perform a read-only smoke test in 3DEqualizer R7.1. Neither was run as part of this audit.
6. Validate the requester appearance, sizing, text overflow/scroll behavior, close behavior, and menu/help dispatch in R7.1 before treating the UI as complete.
7. Confirm the R7.1 custom-script module search path resolves `scene_inspector.py` when `kikz_toolkit.py` imports it.

## Validation and changes

- R7.1 official documentation reviewed: the single vendor command summary linked above. Key evidence lines: scripting tags 15–23; version getter 79–80; camera API 560–582; point-group APIs 481–494; point enumeration/position/status APIs 704–736 and 813; lens APIs 838–899; requester APIs 147–152 and text area APIs 210–211; current-frame/menu-label getters 264 and 273–275.
- Static API inventory performed by reading source and searching call sites. No scripts were executed.
- No mocked tests or in-application R7.1 tests were run.
- Only this report is intended to change in this task. Implementation scripts remain untouched. No dependencies, Python environment, PATH, scenes, or `main` were changed.
- **Approval gate:** stop here and wait for the owner to approve a specific implementation task.
