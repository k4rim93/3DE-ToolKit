# API Examples

These are documentation examples only, not implementation scripts or runtime tests. API signatures below are independently present in the [R7.1](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r7.1.txt), [R8.0](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.0.txt), and [R8.1](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.1.txt) command summaries, unless explicitly marked R8.1-specific. See [API_REFERENCE.md](API_REFERENCE.md) for full classifications and evidence.

## Guard calculated 3D coordinates

```python
status = tde4.getPointCalculated3DStatus(pgroup_id, point_id)

if status == "NOT_CALCULATED":
    calculated_position = None
    result_state = "not calculated"
elif status in ("CALCULATED", "TRIANGULATED"):
    try:
        calculated_position = tde4.getPointCalcPosition3D(
            pgroup_id, point_id
        )
        result_state = status
    except Exception as error:
        calculated_position = None
        result_state = "unavailable: %s" % error
else:
    calculated_position = None
    result_state = "unknown status: %s" % status
```

All three version summaries list the status getter and these three enum values, as well as the calculated-position getter. The references do not promise the position getter's behavior for every scene state; per-point exception reporting is therefore still necessary. Do not treat unknown future status values as valid coordinates.

## Read survey point information separately

```python
survey_mode = tde4.getPointSurveyMode(pgroup_id, point_id)
try:
    survey_position = tde4.getPointSurveyPosition3D(pgroup_id, point_id)
except Exception as error:
    survey_position = None
    survey_error = str(error)
```

The survey mode names are `SURVEY_FREE`, `SURVEY_APPROX`, `SURVEY_EXACT`, and `SURVEY_LINEUP`. The summaries don't state which modes guarantee a meaningful vector or define its units. Keep survey and calculated results as distinct report fields.

For a Mocap point, the three release summaries also list per-camera, per-frame getters:

```python
mocap_survey = tde4.getPointMoCapSurveyPosition3D(
    pgroup_id, point_id, camera_id, frame
)
mocap_calculated = tde4.getPointMoCapCalcPosition3D(
    pgroup_id, point_id, camera_id, frame
)
```

These use the same documented signature in R7.1, R8.0 and R8.1. The summaries do not specify missing-value handling or units. R8.0/R8.1 also list array/list variants; their ordering semantics are not established and they are not part of the shared example.

## Validate before reading a 2D observation

```python
valid = tde4.isPointPos2DValid(
    pgroup_id, point_id, camera_id, frame
)

if valid == 1:
    position_2d = tde4.getPointPosition2D(
        pgroup_id, point_id, camera_id, frame
    )
else:
    position_2d = None
```

This is the conservative use of the documented `0|1` validity result. The API is queried for the specific group, point, camera and frame. Keep `frame` within a verified camera frame domain; invalid-ID and out-of-range behavior are not specified in the summaries.

## Identify the assigned lens and model

```python
lens_id = tde4.getCameraLens(camera_id)
lens_name = tde4.getLensName(lens_id)
ld_model = tde4.getLensLDModel(lens_id)
distortion_mode = tde4.getLensDynamicDistortionMode(lens_id)
```

Each call's signature is listed in all three summaries. They establish the camera's lens handle, lens name, model identifier and dynamic-distortion mode. They don't establish behavior for a missing lens handle. Lens parameter names can be enumerated from a known model:

```python
parameter_count = tde4.getLDModelNoParameters(ld_model)
parameter_names = [
    tde4.getLDModelParameterName(ld_model, index)
    for index in range(parameter_count)
]
```

For each known parameter name, the docs list `getLDModelParameterType(model, para_name)`, `getLDModelParameterDefault(model, para_name)`, and `getLDModelParameterRange(model, para_name)`. Read values with `getLensLDRegularParameter(lens_id, para_name)` or `getLensLDAdjustableParameter(lens_id, para_name, focal_length, focus_distance)` according to the documented model metadata. The API summaries do not define universal parameter names/units, so do not hard-code assumptions. `getLensLDModelList()` is documented in R8.0/R8.1, but not listed in R7.1; it is not used here.

## Shared Custom Requester call shape

```python
requester_id = tde4.createCustomRequester()
widget_name = "scene_report"

try:
    tde4.addTextAreaWidget(
        requester_id, widget_name, "Scene report", 280, 0
    )
    tde4.appendTextAreaWidgetString(
        requester_id, widget_name, report_text
    )
    tde4.postCustomRequester(
        requester_id, "Scene Inspector", 640, 420, "Close"
    )
finally:
    tde4.deleteCustomRequester(requester_id)
```

The exact functions and argument order are listed in R7.1, R8.0 and R8.1 summaries. `postCustomRequester` returns `<int>`, but its button mapping is unspecified and intentionally unused. The summaries do not explicitly state whether this call blocks; the code shape is a compatibility recommendation, not proof of modal behavior, visual layout, or guaranteed cleanup semantics in any installed release. Verify first in R7.1. The official R8.1 structured reference includes a text-area example, but it is supplemental and not substituted for the per-release summary evidence.

## Status of examples

These snippets are API guidance, not tests, and were not run inside 3DE. Exact signatures are documented; runtime UI appearance, error paths, getter sentinel values, and coordinate conventions remain unverified. See `VERSION_COMPATIBILITY.md` for the readiness decision.
