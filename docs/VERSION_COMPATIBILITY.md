# Version Compatibility

**Priority:** R7.1 is the owner's primary production version. Verification and in-application validation should target R7.1 first; R8.0 and R8.1 are secondary.

## Official references

- [R7.1 Python Interface Command Summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r7.1.txt)
- [R8.0 Python Interface Command Summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.0.txt)
- [R8.1 Python Interface Command Summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.1.txt)
- [R8.1 structured Python API reference](https://www.3dequalizer.com/user_daten/sections/tech_docs/py_doc/tde4_with_examples.wtrl.core.rfc-2119.json) (R8.1 only)

`VERIFIED` below means the exact API signature/return placeholder is in that version's official command summary; it does not mean the call was run in that version. `VERSION-SPECIFIC` means release coverage differs. `UNVERIFIED` means the required detail is not established by official documentation or runtime evidence.

## Compatibility matrix

| Area | R7.1 (primary) | R8.0 | R8.1 | Cross-version conclusion |
|---|---|---|---|---|
| Camera-to-lens assignment | `getCameraLens(camera_id) → lens_id`: VERIFIED (summary line 582) | VERIFIED (around line 610) | VERIFIED (around line 618) | Shared signature. Handling of an absent lens handle is UNVERIFIED. |
| Lens distortion model | `getLensLDModel(lens_id) → model`: VERIFIED (line 888) | VERIFIED (line 944) | VERIFIED (line 952) | Shared. Dynamic mode and generic regular/adjustable parameter getters are also documented in all three. Units and model-specific parameter semantics are UNVERIFIED. |
| Model catalogue | `getLensLDModelList`: UNVERIFIED / not listed in the lens summary | VERSION-SPECIFIC (line 943) | VERSION-SPECIFIC (line 951) | Do not depend on this list to build the R7.1 UI. `getLDModelNoParameters`/`getLDModelParameterName` are shared alternatives for a known model. |
| Calculated 3D status | `getPointCalculated3DStatus` + enum values: VERIFIED (lines 71, 813) | VERIFIED (lines 71, 857) | VERIFIED (lines 73, 865) | Shared status values `NOT_CALCULATED`, `CALCULATED`, `TRIANGULATED`; use status before requesting calculated coordinates. Guarantee of getter behavior remains UNVERIFIED. |
| Calculated 3D coordinate | `getPointCalcPosition3D(pgroup, point) → vector 3d`: VERIFIED (lines 716–719) | VERIFIED (around lines 760–763) | VERIFIED (around lines 768–771) | Shared signature; absent-value/error behavior and units UNVERIFIED. |
| Survey coordinate and mode | `getPointSurveyPosition3D`, `getPointSurveyMode`: VERIFIED (lines 716–724) | VERIFIED (around 760–768) | VERIFIED (around 768–776) | Shared; meaningfulness conditions and units UNVERIFIED. |
| Mocap per-frame survey/calculated position | `getPointMoCapSurveyPosition3D` and `getPointMoCapCalcPosition3D`: VERIFIED (lines 720–723) | VERIFIED (764–767) | VERIFIED (772–775) | Shared functions include camera and frame arguments; value availability and units are UNVERIFIED. |
| Mocap per-camera survey/calculated position lists | UNVERIFIED (list variants not found in R7.1 summary) | VERSION-SPECIFIC (lines 871–872) | VERSION-SPECIFIC (lines 879–880) | Do not call list variants as an R7.1 common path; ordering/correspondence is UNVERIFIED. |
| 2D observation validity and position | `isPointPos2DValid` and `getPointPosition2D`: VERIFIED (lines 730–736) | VERIFIED (774–780) | VERIFIED (782–788) | Shared exact signatures. Check validity before position. Frame bounds/errors and coordinate conventions UNVERIFIED. |
| Custom Requester lifecycle | `createCustomRequester`, `deleteCustomRequester`, `postCustomRequester`: VERIFIED (lines 147–152) | VERIFIED (152–157) | VERIFIED (155–160) | Shared signatures. Blocking/modal behavior, runtime layout and button-result semantics are UNVERIFIED. |
| Text report widget | `addTextAreaWidget`, `appendTextAreaWidgetString`: VERIFIED (lines 210–211) | VERIFIED (215–216) | VERIFIED (219–220) | Shared signature, including `editable` argument. Runtime presentation unverified. |
| Script menu label routing | `getLastScriptMenuLabel`: VERIFIED in each summary (near line 275) | VERIFIED | VERIFIED | Shared getter signature; actual dispatch with project addlabels untested. |
| Attribute editor position tag | Not documented | Not documented | VERSION-SPECIFIC (`3DE4.script.gui.attribute_editor_pos`, line 34) | Not required by the modal requester strategy. |

## Recommended shared strategy

For the initial UI, use the shared Custom Requester call shape: create the requester, add a text area, append report text, post it with one Close label, then delete it after the call returns. The exact signatures are present independently in R7.1, R8.0 and R8.1. The summaries do not specify whether this call blocks, so modal behavior must be checked in-app. Avoid `postCustomRequesterAndContinue` and callback-dependent layouts in the first shared UI because the requester's detailed callback lifecycle has not been verified in the target installations. The common path still needs an in-application smoke check for sizing, widget rendering, close/delete lifecycle and script menu routing.

For point data, call `getPointCalculated3DStatus` before `getPointCalcPosition3D`; report `NOT_CALCULATED` as unavailable and preserve the distinction between calculated and triangulated states. Treat any getter failure as an item-level diagnostic. Keep survey coordinates separate and report `getPointSurveyMode`. Do not infer numeric units or missing-vector conventions.

For tracking, query `isPointPos2DValid` for each explicit point/group/camera/frame tuple and call `getPointPosition2D` only when the result is 1. Stay within a frame domain independently established for that camera. Do not infer behavior for invalid IDs or out-of-range frame values.

## Verification limitations and status

- Exact shared signatures for the listed core API calls are independently documented in all three command summaries.
- The R8.1 structured reference gives detailed Python annotations/examples for some calls such as `getPointPosition2D`, `isPointPos2DValid`, and `getLensLDModel`. It does not establish those detailed annotation contracts for earlier releases.
- No 3DE application was run during this research. There is no runtime certification for R7.1, R8.0, or R8.1.
- Refer to [API_REFERENCE.md](API_REFERENCE.md) for per-function classifications and remaining semantic gaps.

## IMPLEMENTATION READINESS

**Scene Inspector implementation should not be considered ready to proceed or ship yet.** Documentation now verifies the signatures needed for a conservative shared read-only foundation, with R7.1 as the primary target. Remaining blockers before implementation is declared safe/complete:

1. The repository already contains prototype scripts (`scripts/scene_inspector.py` and `scripts/kikz_toolkit.py`) from earlier work. They were not modified in this documentation task; their current behavior must be reconciled with these findings before any further implementation or release claim. In particular, the prototype's unconditional calculated-position getter needs a status guard before it can be relied on.
2. Official summaries do not specify absent calculated/survey values, exceptions, coordinate units, invalid IDs, or out-of-range frame behavior. Code must surface diagnostics and must not depend on undocumented sentinels.
3. Mocap per-camera position-list ordering/correspondence semantics are unclear; exclude that feature until verified. Do not use R8.x-only helpers in the R7.1 path.
4. The R7.1 custom requester, widget presentation, menu-label routing, dialog cleanup, and target Python/runtime behavior have not been checked inside the owner's installed 3DE R7.1. Perform a read-only smoke test in R7.1 first; then validate R8.0/R8.1 if they remain supported targets.
5. Model-specific lens parameter names, units, and interpretation are not established generically. Keep the first inspector to model identity and documented metadata unless individual model details are verified.

No code was changed as part of this verification task. Explicit owner approval is still required before implementation work resumes.
