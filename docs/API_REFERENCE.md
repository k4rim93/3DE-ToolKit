# Phase 1 API Reference

This reference records APIs used by the read-only Scene Inspector. Function names and summary signatures were checked independently against the vendor command summaries for R7.1, R8.0, and R8.1. Detailed selector contracts are available in the official R8.1 structured documentation only; older-release use is restricted where those semantics matter.

## Official documentation

- [3DE4 R7.1 Python command summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r7.1.txt)
- [3DE4 R8.0 Python command summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.0.txt)
- [3DE4 R8.1 Python command summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.1.txt)
- [3DE4 R8.1 structured Python API documentation](https://www.3dequalizer.com/user_daten/sections/tech_docs/py_doc/tde4_with_examples.wtrl.core.rfc-2119.json)

The command summaries give return placeholders such as `<camera_id>`, `[<start>,<end>,<step>]`, and `<vector 3d>`. Unless a source explicitly provides a concrete Python type or semantic contract, these are documented shapes rather than claims about a precise runtime class or units.

## APIs used by the standard report

| API | Documented signature / result | Use and compatibility |
|---|---|---|
| `get3DEVersion()` | `get3DEVersion()` → `<3de_version>` | Runtime version string; listed in all three release summaries. Its exact text format is not specified. |
| `getNoCameras()` | `getNoCameras()` → `<number_of_cameras>` | Camera iteration bound; all three releases. |
| `getFirstCamera()` | `getFirstCamera()` → `<camera_id>` | Begins camera iteration; all three releases. |
| `getNextCamera(camera_id)` | `getNextCamera(<camera_id>)` → `<camera_id>` | Advances camera iteration; all three releases. The summaries do not spell out end-of-list sentinel behavior. |
| `getCameraName(camera_id)` | `getCameraName(<camera_id>)` → `<name>` | Camera display name; all three releases. |
| `getCameraType(camera_id)` | `getCameraType(<camera_id>)` → `"SEQUENCE"` or `"REF_FRAME"` | Camera kind; all three releases. |
| `getCameraNoFrames(camera_id)` | `getCameraNoFrames(<camera_id>)` → `<number_of_frames>` | Frame count; all three releases. |
| `getCameraSequenceAttr(camera_id)` | `getCameraSequenceAttr(<camera_id>)` → `[<start>,<end>,<step>]` | Sequence attributes; all three releases. Units/frame-number interpretation is not elaborated by the summary. |
| `getCameraFPS(camera_id)` | `getCameraFPS(<camera_id>)` → `<double>` | Camera frame rate; all three releases. |
| `getCameraLens(camera_id)` | `getCameraLens(<camera_id>)` → `<lens_id>` | Assigned lens handle; all three releases. |
| `getLensName(lens_id)` | `getLensName(<lens_id>)` → `<name>` | Lens name; all three releases. |
| `getNoPGroups()` | `getNoPGroups()` → `<number_of_pgroups>` | Point-group iteration bound; all three releases. |
| `getFirstPGroup()` | `getFirstPGroup()` → `<pgroup_id>` | Begins point-group iteration; all three releases. |
| `getNextPGroup(pgroup_id)` | `getNextPGroup(<pgroup_id>)` → `<pgroup_id>` | Advances point-group iteration; all three releases. End sentinel behavior is not specified in the summaries. |
| `getPGroupName(pgroup_id)` | `getPGroupName(<pgroup_id>)` → `<name>` | Point-group name; all three releases. |
| `getPGroupType(pgroup_id)` | `getPGroupType(<pgroup_id>)` → `"CAMERA"`, `"OBJECT"`, or `"MOCAP"` | Point-group kind; all three releases. |
| `getPGroupEnabledFlag(pgroup_id)` | `getPGroupEnabledFlag(<pgroup_id>)` → `0` or `1` | Read-only enabled state; all three releases. |
| `getNoPoints(pgroup_id)` | `getNoPoints(<pgroup_id>)` → `<number_of_points>` | Point count; all three releases. |

## R8.1 deep-inspection APIs

These APIs are called for deep inspection only when the detected version string contains `8.1`. The older summaries confirm several names/signatures, but do not provide the detailed selector contract used to enumerate all points; deep point enumeration therefore remains disabled on R7.1 and R8.0.

| API | Documented signature / result | Use and caveat |
|---|---|---|
| `getPointList(pgroup_id, selected_only)` | `getPointList(pgroup_id, selected_only=None)` → `list[DBObjID_t]` | R8.1 contract: `0` or omitted returns all point IDs; `1` returns selected points only. Inspector passes `0`. |
| `getPointName(pgroup_id, point_id)` | `getPointName(<pgroup_id>,<point_id>)` → `<name>` | Point name; all three summaries. |
| `getPointCalcPosition3D(pgroup_id, point_id)` | `getPointCalcPosition3D(<pgroup_id>,<point_id>)` → `<vector 3d>` | Calculated point location; all three summaries. Availability/sentinel behavior for uncalculated points is not specified in the summaries. Per-item errors are reported. |
| `getPointSurveyPosition3D(pgroup_id, point_id)` | `getPointSurveyPosition3D(<pgroup_id>,<point_id>)` → `<vector 3d>` | Survey location; all three summaries. The summary does not define when the value is meaningful. |
| `getPointSurveyMode(pgroup_id, point_id)` | `getPointSurveyMode(<pgroup_id>,<point_id>)` → `<survey mode>` | Survey state; all three summaries. |
| `getCurrentFrame(camera_id)` | `getCurrentFrame(<camera_id>)` → `<frame>` | Reads, without changing, the camera's current frame; all three summaries. |
| `isPointPos2DValid(pgroup_id, point_id, camera_id, frame)` | `isPointPos2DValid(<pgroup_id>,<point_id>,<camera_id>,<frame>)` → `0` or `1` | Checks whether a 2D observation is valid; all three summaries. |
| `getPointPosition2D(pgroup_id, point_id, camera_id, frame)` | `getPointPosition2D(<pgroup_id>,<point_id>,<camera_id>,<frame>)` → `<vector 2d>` | Reads position only when validity returns `1`; all three summaries. |

The R8.1 structured document specifies `selected_only` as an optional integer flag, with `1` returning only selected points and `0`/omission returning all points. It also specifies a TypeError for argument type/signature mismatch. It does not establish the same detailed selector contract for R7.1 or R8.0, so the implementation does not call this list function in those releases.

## UI APIs

The R7.1, R8.0, and R8.1 command summaries list the following Custom Requester operations and argument shapes. The toolkit uses the modal requester path only; it does not use callbacks or non-blocking requester lifecycle APIs.

| API | Documented signature / result | Use |
|---|---|---|
| `createCustomRequester()` | `createCustomRequester()` → `<requester id>` | Creates a temporary report dialog. |
| `addTextAreaWidget(...)` | `addTextAreaWidget(<requester id>,<widget name>,<label>,<height>,<editable>)` | Adds a non-editable report area. |
| `appendTextAreaWidgetString(...)` | `appendTextAreaWidgetString(<requester id>,<widget name>,<string>)` | Fills report text. |
| `postCustomRequester(...)` | `postCustomRequester(<requester id>,<window title>,<width>,<height>,<label 0>,...)` → `<int>` | Posts the modal requester with a Close label. Runtime return meaning is not used. |
| `deleteCustomRequester(requester_id)` | `deleteCustomRequester(<requester id>)` | Releases the temporary requester after it closes. |
| `getLastScriptMenuLabel()` | `getLastScriptMenuLabel()` → `<menu_label>` | Dispatches the menu item/addlabel invoked by the user. Runtime interaction with all addlabel entries is not yet verified in-app. |

## Read-only guarantee

The implementation calls only the getters listed above and requester presentation APIs. It does not call setters, change current camera/frame/point group, run calculations, write files, or access the network from inside 3DE.

## Unverified details

- R7.1/R8.0 accepted `selected_only` values and detailed return/exception contracts; deep point enumeration is disabled there.
- Exact version string format returned by `get3DEVersion()`; the R8.1 gate currently checks whether its text contains `8.1`.
- End-of-iteration sentinel semantics for `getNextCamera` and `getNextPGroup`; iteration is bounded by the corresponding documented count.
- Whether a point's calculated/survey getters return a special value or raise when data is absent.
- UI sizing, addlabel order/dispatch, Python import resolution between the two scripts, and dialog lifecycle in each installed application.
- In-application behavior and performance in all three releases.
