# Phase 1 Inspection and Planning Report

**Repository:** `k4rim93/3DE-ToolKit`
**Inspected:** 2026-11-13
**Branch:** `docs/project-handover-foundation`
**Purpose:** Phase 1 planning only. No implementation has been started.

## 1. Repository state and inventory

The repository is on `docs/project-handover-foundation`, tracking `origin/docs/project-handover-foundation`. Before this report, the working tree was clean. The configured remote is `origin` at `https://github.com/k4rim93/3DE-ToolKit.git` for fetch and push. Recent history contains the initial README and the handover/specification/onboarding documentation; `main` was not checked out or modified.

Tracked project files present before this report:

| Path | Purpose |
|---|---|
| `README.md` | Minimal project title and description. |
| `CODEX_START_HERE.md` | Repository onboarding and current-assignment instructions. |
| `docs/PROJECT_HANDOVER.md` | Goals, architecture principles, safety, protected work, and project context. |
| `docs/BUILD_SPEC_PHASE_1.md` | Phase 1 deliverables, inspector behavior, API scope, acceptance criteria, and test plan. |
| `docs/DEVELOPMENT_RULES.md` | Branch, API correctness, safety, quality, validation, and public-repository rules. |

There are no implementation scripts, tests, dependency manifests, or pre-existing API-reference files in the inspected project tree. The report itself is the only planned addition in this task. The Maya-to-3DE exporter/importer is explicitly protected and is not present in this repository inventory; it remains out of scope.

## 2. Phase 1 proposed architecture

Keep implementation small and read-only, with four clear responsibilities:

1. **Compatibility/capability layer:** detect the host using the documented `tde4.get3DEVersion()` and expose only capabilities whose exact signatures are verified for that release. Avoid relying on version-string parsing details until confirmed in-app.
2. **Collection layer:** gather camera, point-group, point, 2D tracking, calculated-3D, and survey data through verified getters. Isolate errors at camera/group/point scope and mark partial data explicitly.
3. **Formatting layer:** convert collected values to a stable structured result and readable report without touching scene state. Deep tracking observations remain opt-in due to scene-size cost.
4. **UI layer:** use native Custom Requester only after its callbacks, lifecycle, and layout behavior are verified in each supported release. Each tool gets an adjacent `!` help control that describes purpose, usage, inputs, output, and safety level.

Proposed dependency direction: UI → collector/capabilities → documented `tde4` getters; formatting consumes collected data and does not call `tde4`. No package or environment changes are proposed. Output should appear in the UI by default; writing a report to disk should require an explicit user-selected path and safe collision handling.

## 3. Official API verification matrix

The vendor's version-specific command summaries were opened and searched directly. Links below point to the official downloadable command summaries. The summaries label return shapes/types and argument placeholders; they do not always define precise Python classes, units, exception behavior, or semantic edge cases. Entries below are verified as documented names/signatures/summary return types, not as runtime-tested behavior.

| Release | Official source and evidence | Verified API subset relevant to the inspector | Still unverified / limitation |
|---|---|---|---|
| **R7.1** | [Official R7.1 Python command summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r7.1.txt) (document header identifies Release 7.1; `get3DEVersion()` at lines 79–80; camera getters at 558–583; point groups at 477–506; points and observations at 702–739). | `get3DEVersion()` → `<3de_version>`; `getCameraList(<selected_only>)` → list of camera IDs; `getCameraName(<camera_id>)` → `<name>`; `getCameraType(<camera_id>)` → `"SEQUENCE"\|"REF_FRAME"`; `getCameraNoFrames(<camera_id>)` → `<number_of_frames>`; `getCameraSequenceAttr(<camera_id>)` → `[<start>,<end>,<step>]`; `getCameraFPS(<camera_id>)` → `<double>`; `getCameraLens(<camera_id>)` → `<lens_id>`; `getPGroupList(<selected_only>)` → list of point-group IDs; `getPGroupType(<pgroup_id>)` → `"CAMERA"\|"OBJECT"\|"MOCAP"`; `getPGroupEnabledFlag(<pgroup_id>)` → `0|1`; `getPointList(<pgroup_id>,<selected_only>)` → list of point IDs; `getPointName(<pgroup_id>,<point_id>)` → `<name>`; `getPointPosition2D(<pgroup_id>,<point_id>,<camera_id>,<frame>)` → `<vector 2d>`; `isPointPos2DValid(<pgroup_id>,<point_id>,<camera_id>,<frame>)` → `0|1`; `getPointCalcPosition3D(<pgroup_id>,<point_id>)` and `getPointSurveyPosition3D(<pgroup_id>,<point_id>)` → `<vector 3d>`; `getPointSurveyMode(<pgroup_id>,<point_id>)` → `<survey mode>`. | The command summary verifies these names are in R7.1, but does not establish null/sentinel behavior, errors for unavailable calculated positions, units for all fields, sequence frame indexing semantics, or callback/UI lifecycle semantics. These require documentation detail review and/or in-app confirmation. |
| **R8.0** | [Official R8.0 Python command summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.0.txt) (document header identifies Release 8.0; version getter at lines 80–81; cameras at 588–613; point groups at 489–518; corresponding point APIs in the point section). | Same relevant getter names and summary signatures as R7.1 are present in this independent R8.0 summary: `get3DEVersion()`, camera list/name/type/frame count/sequence attributes/FPS/lens, point-group list/type/enabled flag, point list/name, 2D position/validity, calculated 3D position, survey position/mode. `getCameraList(<selected_only>)`, `getPGroupList(<selected_only>)`, and `getPointList(<pgroup_id>,<selected_only>)` return ID lists per the summary. | Same semantic/runtime gaps as R7.1. This report has not executed these calls in R8.0 and does not certify exact returned Python classes or exceptional cases. The version-specific command summary is the basis; a generic currently labeled R8.1 API page is not substituted for it. |
| **R8.1** | [Official R8.1 Python command summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.1.txt) (document header identifies Release 8.1; version getter at lines 82–83; cameras at 596–621; point groups at 497–526; corresponding point APIs in the point section). | Same relevant getter names and signatures are present in this independent R8.1 summary: `get3DEVersion()`, camera list/name/type/frame count/sequence attributes/FPS/lens, point-group list/type/enabled flag, point list/name, 2D position/validity, calculated 3D position, survey position/mode. | Same semantic/runtime gaps as R7.1/R8.0. No R8.1 application session was available for runtime or UI verification. |

### Verification interpretation and remaining API work

- The vendor's summaries expressly document the listed calls and signature shapes for all three releases. This supports planning a common read-only subset, subject to tests, rather than an assumption based only on one version.
- `getPointList`, `getPGroupList`, and `getCameraList` use a `<selected_only>` parameter in these summaries; implementation must deliberately pass the documented value meaning “all” only after its accepted values are confirmed from the docs/runtime. The summary shorthand alone does not define that value.
- The summaries list setters alongside getters. The inspector must not call setters, mutating functions, current-selection/current-frame setters, calculation commands, or file/project operations.
- The returned `<vector 3d>` for calculated/survey positions is documented, but when it is meaningful, how “not calculated” is represented, and whether a getter can error are **UNVERIFIED** here. Gate optional values with documented status/validity APIs only after their semantics are confirmed.
- The exact way to read camera lens metadata beyond assigned lens ID, lens naming, and fields/units desired for the first report needs focused verification before implementation.
- Deep tracking scale/performance, observations outside sequence bounds, malformed scene data behavior, exact exceptions, and UI event/lifecycle behavior are **UNVERIFIED** pending in-app runs.
- Although Custom Requester calls are listed in each summary (including `createCustomRequester`, `postCustomRequester`, and widget APIs), successful cross-version presentation, callback ordering, and cleanup behavior have not been verified at runtime. Do not build the UI around assumed callback semantics.
- No API name or signature has been invented for production use. If the focused review cannot resolve a needed item from the official documentation, mark it `UNVERIFIED` and exclude it from production behavior as required by the spec.

## 4. Proposed test strategy

| Test class | Planned checks | What it cannot claim |
|---|---|---|
| **Static** | Parse/compile source with an interpreter compatible with the particular target environment when available; inspect imports and calls to ensure only verified APIs/getters are used; review branch diff for prohibited setters, hidden file writes, dependencies, and unrelated files. | A host interpreter cannot prove that 3DE's embedded interpreter or `tde4` accepts the code. |
| **Mocked unit tests** | Test pure formatting/normalization against fabricated structured data; test partial-result handling and per-item error reporting with controlled mock collector outputs. Explicitly label fixtures as mocks. | Mocks cannot prove API existence, signatures, return semantics, UI behavior, scene read-only behavior, or performance in 3DE. |
| **In-application** | In each available exact release (R7.1, R8.0, R8.1), run version detection and read-only inspections on a disposable/test scene, including empty/minimal and representative scenes; exercise UI open/close/help; compare reported values to the UI; confirm no scene dirty-state or data changes; measure deep-mode behavior on larger scenes. Record exact version, interpreter, scene class (no client identifiers), steps, and outcomes. | No application installation/session is currently evidenced, so no in-app test is claimed by this report. |

## 5. Risks, conflicts, and owner decisions

### Risks and conflicts

- A camera may be a sequence or reference frame; sequence-only fields must be handled by camera type, and frame-domain assumptions must not be guessed.
- Optional or unavailable 3D/survey values may fail or have special sentinel behavior. A getter's presence alone is not enough to safely interpret a value.
- Deep per-frame observations can be expensive for large point/camera/frame counts; deep mode should be opt-in, and an eventual progress/cancel strategy itself needs verified UI support.
- The API summaries show deprecated camera fields such as zooming flag and timeshift in R7.1; avoid deprecated APIs unless a verified requirement arises.
- Public-repository hygiene still applies to all test fixtures, logs, and generated reports. Use synthetic scenes/data and do not commit client or production material.
- No repository conflict or protected-file collision was found during inspection. Existing project documentation says the protected Maya exporter/importer is outside this repository/task scope.

### Decisions needing owner approval before implementation

1. Confirm the minimum useful first-pass report fields: proposed default is scene/version summary, camera metadata, point-group summary, and aggregate point counts; per-point survey/calculated coordinates and all-frame 2D observations stay in opt-in deep detail.
2. Confirm default report destination: proposed default is display in a native requester, with file export only on explicit user action and an explicit path.
3. Decide whether lens output should show only assigned lens identity/name or include selected optical parameters; the latter requires verifying specific getters, units, and dynamic/static behavior.
4. Confirm which exact 3DE installations/scenes are available for R7.1/R8.0/R8.1 in-app validation before implementation is considered complete.

## 6. Scope completed and status

This is inspection, API research, architecture and test planning only. No implementation, dependencies, environment settings, scene data, or `main` branch were changed. No tests were run because no implementation exists. The report is ready for review; implementation must wait for the owner's explicit approval.

