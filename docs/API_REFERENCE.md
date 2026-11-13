# Phase 1 API Reference

**Version priority:** R7.1 is the owner's production version and is the primary compatibility target. R8.0 and R8.1 are secondary targets.

## Official sources and status labels

- [R7.1 Python Interface Command Summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r7.1.txt) — lines cited below are from this release-specific document.
- [R8.0 Python Interface Command Summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.0.txt)
- [R8.1 Python Interface Command Summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.1.txt)
- [R8.1 structured Python API reference](https://www.3dequalizer.com/user_daten/sections/tech_docs/py_doc/tde4_with_examples.wtrl.core.rfc-2119.json) (R8.1 only; never treated as evidence for R7.1/R8.0).

**VERIFIED** means the release's own official document lists the exact function and signature/return placeholder. **VERSION-SPECIFIC** means the function or a more detailed contract is documented only for particular releases. **UNVERIFIED** means official evidence does not establish the required semantics, runtime behavior, or availability. A verified signature does not imply an in-application test.

## Shared scene enumeration APIs

The earlier report also references these APIs for camera/group/point discovery. The exact signatures are in all three release summaries; detailed selector semantics are only present in the R8.1 structured reference.

| API | Documented signature / result | R7.1 | R8.0 | R8.1 | Gap |
|---|---|---|---|---|---|
| `get3DEVersion()` | `()` → `<3de_version>` | VERIFIED | VERIFIED | VERIFIED | Text format and parsing rules UNVERIFIED. |
| `getNoCameras()` / `getFirstCamera()` / `getNextCamera(camera_id)` | count / first ID / next ID | VERIFIED | VERIFIED | VERIFIED | End sentinel semantics are not specified in summaries. |
| `getCameraName(camera_id)` / `getCameraType(camera_id)` | name / `SEQUENCE` or `REF_FRAME` | VERIFIED | VERIFIED | VERIFIED | Camera type-specific field rules need care. |
| `getCameraNoFrames(camera_id)` / `getCameraSequenceAttr(camera_id)` / `getCameraFPS(camera_id)` | frame count / `[start,end,step]` / double | VERIFIED | VERIFIED | VERIFIED | Frame indexing, range inclusivity and units are not fully explained. |
| `getNoPGroups()` / `getFirstPGroup()` / `getNextPGroup(pgroup_id)` | count / first ID / next ID | VERIFIED | VERIFIED | VERIFIED | End sentinel semantics are not specified in summaries. |
| `getPGroupName(pgroup_id)` / `getPGroupType(pgroup_id)` / `getPGroupEnabledFlag(pgroup_id)` | name / type / `0|1` | VERIFIED | VERIFIED | VERIFIED | Type names are listed by each summary. |
| `getNoPoints(pgroup_id)` / `getPointName(pgroup_id, point_id)` | count / name | VERIFIED | VERIFIED | VERIFIED | — |
| `getPointList(pgroup_id, selected_only)` | list of point IDs | VERIFIED | VERIFIED | VERIFIED | R8.1 documents `0`/omission as all and `1` as selected. Exact accepted values for R7.1/R8.0 are UNVERIFIED; do not assume selector semantics there. |
| `getCurrentFrame(camera_id)` | `<frame>` | VERIFIED | VERIFIED | VERIFIED | Range and meaning for non-sequence/reference cameras not elaborated. |

## 3D points and survey data

| API | Documented signature / result | R7.1 | R8.0 | R8.1 | Notes |
|---|---|---|---|---|---|
| `getPointCalculated3DStatus(pgroup_id, point_id)` | `<point_3d_status>`; enum: `NOT_CALCULATED`, `CALCULATED`, `TRIANGULATED` | VERIFIED | VERIFIED | VERIFIED | Official summaries: R7.1 lines 71, 813; R8.0 lines 71, 857; R8.1 lines 73, 865. Query before calculated-position getter. |
| `getPointCalcPosition3D(pgroup_id, point_id)` | `<vector 3d>` | VERIFIED | VERIFIED | VERIFIED | R7.1 lines 716–719; R8.0 lines 760–763; R8.1 lines 768–771. R8.1 structured signature returns `Vector3D_t`. |
| `isPointCalculated3D(pgroup_id, point_id)` | `0|1` | VERIFIED | VERIFIED | VERIFIED | R7.1 line 736; R8.0 line 780; R8.1 line 788. The summaries do not explain its relation to the three-valued status enum; prefer the status getter. |
| `getPointSurveyPosition3D(pgroup_id, point_id)` | `<vector 3d>` | VERIFIED | VERIFIED | VERIFIED | R7.1 lines 716–717; R8.0 lines 760–761; R8.1 lines 768–769. |
| `getPointSurveyMode(pgroup_id, point_id)` | `<survey mode>`; enum values listed above | VERIFIED | VERIFIED | VERIFIED | R7.1 line 724; R8.0 line 768; R8.1 line 776. The mode names are documented; validity conditions and coordinate units are not. |
| `getPointMoCapSurveyPosition3D(pgroup_id, point_id, camera_id, frame)` | `<vector 3d>` | VERIFIED | VERIFIED | VERIFIED | R7.1 lines 720–721; R8.0 lines 764–765; R8.1 lines 772–773. Per-camera, per-frame Mocap survey value. Conditions/units remain unspecified. |
| `getPointMoCapCalcPosition3D(pgroup_id, point_id, camera_id, frame)` | `<vector 3d>` | VERIFIED | VERIFIED | VERIFIED | R7.1 lines 722–723; R8.0 lines 766–767; R8.1 lines 774–775. Per-camera, per-frame Mocap calculated value. Availability semantics remain unspecified. |
| `getPointMoCapSurveyPosition3DList(pgroup_id, point_id, camera_id)` | list of `<vector3d>` | UNVERIFIED | VERSION-SPECIFIC | VERSION-SPECIFIC | Present in R8.0 lines 871–872 and R8.1 lines 879–880, absent from R7.1 command summary. It is an additional per-camera survey-data accessor for Mocap points; list indexing/meaning is not specified by the summary. |
| `getPointMoCapCalcPosition3DList(pgroup_id, point_id, camera_id)` | list of `<vector3d>` | UNVERIFIED | VERSION-SPECIFIC | VERSION-SPECIFIC | Same release evidence as above; per-camera list semantics are not fully specified. |

**Safe inspection rule:** call `getPointCalculated3DStatus` first. If it returns `NOT_CALCULATED`, do not present a calculated coordinate as available. For `CALCULATED` or `TRIANGULATED`, a subsequent `getPointCalcPosition3D` is the cautious candidate workflow, but the summaries do not explicitly promise that the getter cannot fail or define a missing-value sentinel. Catch and report per-point getter failure; never substitute a survey position for calculated data. This sequence is **VERIFIED as an API workflow candidate**, while guaranteed getter safety for every scene remains **UNVERIFIED** pending official semantic detail or an in-application check.

Survey values must be reported separately from calculated values and include the survey mode. The summaries do not define the conditions under which a survey vector is meaningful or its units. For Mocap, the per-camera list accessors are documented only in R8.0/R8.1; their ordering and correspondence semantics remain **UNVERIFIED**.

## Tracking observations

| API | Documented signature / result | R7.1 | R8.0 | R8.1 | Notes |
|---|---|---|---|---|---|
| `isPointPos2DValid(pgroup_id, point_id, camera_id, frame)` | `0|1` | VERIFIED | VERIFIED | VERIFIED | R7.1 lines 730–736; R8.0 lines 774–780; R8.1 lines 782–788. R8.1 structured signature has four positional-or-keyword arguments, frame `int`, result `int`. |
| `getPointPosition2D(pgroup_id, point_id, camera_id, frame)` | `<vector 2d>` | VERIFIED | VERIFIED | VERIFIED | R7.1 line 730; R8.0 line 774; R8.1 line 782. R8.1 structured signature returns `Vector2D_t`. |

Read an observation only after `isPointPos2DValid(...) == 1`; treat `0` as unavailable and do not read its position. This is the conservative interpretation of the documented validity predicate and `0|1` result. Validity is queried for a particular point-group, point, camera, and frame tuple. The references do not specify out-of-range frame behavior, exceptions for invalid IDs, coordinate units/normalization, or whether validity includes every possible tracker status. Do not probe frames outside a documented camera range; isolate per-observation errors. R8.1 structured documentation includes an example using the predicate with the position getter, but this detailed example is R8.1-only and is not needed to establish the same signatures in R7.1/R8.0.

## Camera lens and distortion data

| API | Documented signature / result | R7.1 | R8.0 | R8.1 | Notes |
|---|---|---|---|---|---|
| `getCameraLens(camera_id)` | `<lens_id>` | VERIFIED | VERIFIED | VERIFIED | R7.1 line 582; R8.0 line 610; R8.1 line 618. This returns the camera's assigned lens handle; the summaries do not document null/invalid lens behavior. |
| `getLensName(lens_id)` | `<name>` | VERIFIED | VERIFIED | VERIFIED | R7.1 line 848; R8.0 line 911; R8.1 line 919. |
| `getLensLDModel(lens_id)` | `<model>` (R8.1 structured type: `str`) | VERIFIED | VERIFIED | VERIFIED | R7.1 line 888; R8.0 line 944; R8.1 line 952. Use to identify the lens distortion model. |
| `getLensDynamicDistortionMode(lens_id)` | `<dyn_distortion_mode>` | VERIFIED | VERIFIED | VERIFIED | R7.1 line 868; R8.0 line 923; R8.1 line 931. Mode enum is documented in each summary; R7.1 lines 53–55, later releases lines 54–56. |
| `getLensLDRegularParameter(lens_id, para_name)` | `<value>` | VERIFIED | VERIFIED | VERIFIED | R7.1 line 893; R8.0 line 949; R8.1 line 957. |
| `getLensLDAdjustableParameter(lens_id, para_name, focal_length, focus_distance)` | `<double>` | VERIFIED | VERIFIED | VERIFIED | R7.1 lines 890–891; R8.0 lines 946–947; R8.1 lines 954–955. |
| `getLensLDAdjustableParameterCurve(lens_id, para_name)` | `<curve_id>` | VERIFIED | VERIFIED | VERIFIED | R7.1 line 892; R8.0 line 948; R8.1 line 956. |
| `getLDModelNoParameters(model)` | `<number_of_parameters>` | VERIFIED | VERIFIED | VERIFIED | R7.1 line 895; R8.0 line 951; R8.1 line 959. |
| `getLDModelParameterName(model, index)` | `<para_name>` | VERIFIED | VERIFIED | VERIFIED | R7.1 line 896; R8.0 line 952; R8.1 line 960. |
| `getLDModelParameterType(model, para_name)` | `<para_type>` | VERIFIED | VERIFIED | VERIFIED | R7.1 line 897; R8.0 line 953; R8.1 line 961. |
| `getLDModelParameterDefault(model, para_name)` | `<value>` | VERIFIED | VERIFIED | VERIFIED | R7.1 line 898; R8.0 line 954; R8.1 line 962. |
| `getLDModelParameterRange(model, para_name)` | `[<a>, <b>]` | VERIFIED | VERIFIED | VERIFIED | R7.1 line 899; R8.0 line 955; R8.1 line 963. |
| `getLensLDModelList()` | `[<ld model>, ...]` | UNVERIFIED | VERSION-SPECIFIC | VERSION-SPECIFIC | Listed by R8.0 line 943 and R8.1 line 951; not present in R7.1 lens summary. R8.1 JSON includes it. Do not use as cross-version API. |

R7.1 summary additionally lists basic lens getters: `getLensFBackWidth/Height`, `getLensFocalLength`, `getLensFilmAspect`, `getLensLensCenterX/Y`, `getLensPixelAspect`, `getLensHorizAngle`, `getLensVertiAngle`, and `getLensFocus` (lines 850–868). Their corresponding entries exist in later summaries (R8.0 around lines 905–923; R8.1 around 913–931). These signatures are **VERIFIED** across all three. Units/conventions are **UNVERIFIED** by the command summaries. For model-specific fields, enumerate model parameter names/types and select regular vs adjustable getters based on verified model metadata; parameter names, value interpretation, and units must not be guessed. Legacy `getLensDistortion`, `getLensAnamorphSqueeze`, `getLensCurvatureX/Y`, and `getLensQuarticDistortion` are explicitly marked obsolete in all three summaries; do not use them for new inspection.

## Custom Requester UI

The following signatures appear unchanged in the three release-specific summaries: R7.1 lines 145–152 and 210–211; R8.0 lines 144–157 and 215–216; R8.1 lines 147–160 and 219–220.

| API | Exact documented signature / result | R7.1 | R8.0 | R8.1 |
|---|---|---|---|---|
| `createCustomRequester()` | `createCustomRequester()` → `<requester id>` | VERIFIED | VERIFIED | VERIFIED |
| `deleteCustomRequester(requester_id)` | `deleteCustomRequester(<requester id>)`; no result stated | VERIFIED | VERIFIED | VERIFIED |
| `addTextAreaWidget(requester_id, widget_name, label, height, editable)` | `addTextAreaWidget(<requester id>, <widget name>, <label>, <height>, <editable>)` | VERIFIED | VERIFIED | VERIFIED |
| `appendTextAreaWidgetString(requester_id, widget_name, string)` | `appendTextAreaWidgetString(<requester id>, <widget name>, <string>)` | VERIFIED | VERIFIED | VERIFIED |
| `postCustomRequester(requester_id, title, width, height, label0, ...)` | `postCustomRequester(<requester id>, <window title>, <width>, <height>, <label 0>, <label 1>, ...)` → `<int>` | VERIFIED | VERIFIED | VERIFIED |
| `postCustomRequesterAndContinue(requester_id, title, width, height, update_callback_function_name)` | Exact positional signature listed; no return stated | VERIFIED | VERIFIED | VERIFIED |
| `getLastScriptMenuLabel()` | `getLastScriptMenuLabel()` → `<menu_label>` | VERIFIED | VERIFIED | VERIFIED |

**Compatible strategy recommendation:** use the same `postCustomRequester` call shape in each release, with one text-area widget, append the rendered report, provide a single Close label, and call `deleteCustomRequester` after posting returns. This uses only calls whose exact signatures are documented in all three releases and avoids callback APIs. The summaries don't explicitly define whether `postCustomRequester` blocks, so modal/blocking behavior is **UNVERIFIED** until checked in-app. `editable=0` is the documented argument shape for a non-editable state, but exact UI behavior/layout and cleanup on exceptional exits are **UNVERIFIED at runtime**. The `<int>` returned by `postCustomRequester` is documented, but its exact button-index/value mapping is not; do not interpret it beyond closing the requester. Script tags include `3DE4.script.name`, `.addlabel`, and `.gui` in all three summaries (R7.1 lines 15–23; R8.0 same; R8.1 same); dispatch behavior through `getLastScriptMenuLabel()` still needs an in-app check.

R8.1 summary adds the script tag `3DE4.script.gui.attribute_editor_pos` (R8.1 line 34), absent in R7.1/R8.0. This is **VERSION-SPECIFIC** and unnecessary for the modal strategy.

## Remaining verification gaps

- None of the official sources are runtime results from the owner's R7.1 installation.
- The old text summaries don't specify exceptions, missing-value sentinels, or invalid-ID behavior for point/lens getters.
- Calculated vector getter safety after status check is not guaranteed explicitly by the sources.
- Survey-vector validity conditions, units, and Mocap list ordering/correspondence semantics are unspecified.
- 2D coordinate units/conventions and out-of-range frame behavior are unspecified.
- Lens parameter units/meaning are model-specific and not enumerated generically; the generic summaries establish parameter-access APIs, not a universal parameter schema.
- Requester geometry, return-value mapping, modal lifecycle, close/delete behavior, help-label dispatch, and script import behavior have not been verified in an application.
