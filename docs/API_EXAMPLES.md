# API Examples

These small examples use only read-only API calls. They are reference snippets, not standalone tests. The vendor command summaries for [R7.1](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r7.1.txt), [R8.0](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.0.txt), and [R8.1](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.1.txt) document the shared getter signatures. The R8.1 selector example is additionally checked against the [structured R8.1 API reference](https://www.3dequalizer.com/user_daten/sections/tech_docs/py_doc/tde4_with_examples.wtrl.core.rfc-2119.json).

## Read camera metadata

```python
camera_count = tde4.getNoCameras()
camera_id = tde4.getFirstCamera()

for unused_index in range(camera_count):
    if camera_id is None:
        break
    name = tde4.getCameraName(camera_id)
    camera_type = tde4.getCameraType(camera_id)
    frame_count = tde4.getCameraNoFrames(camera_id)
    fps = tde4.getCameraFPS(camera_id)
    sequence = tde4.getCameraSequenceAttr(camera_id)
    lens_id = tde4.getCameraLens(camera_id)
    print(name, camera_type, frame_count, fps, sequence, lens_id)
    if unused_index + 1 < camera_count:
        camera_id = tde4.getNextCamera(camera_id)
```

The count bounds iteration, so the snippet does not rely on an undocumented `getNextCamera` end sentinel.

## Read point-group summary

```python
group_count = tde4.getNoPGroups()
group_id = tde4.getFirstPGroup()

for unused_index in range(group_count):
    if group_id is None:
        break
    name = tde4.getPGroupName(group_id)
    group_type = tde4.getPGroupType(group_id)
    enabled = tde4.getPGroupEnabledFlag(group_id)
    point_count = tde4.getNoPoints(group_id)
    print(name, group_type, enabled, point_count)
    if unused_index + 1 < group_count:
        group_id = tde4.getNextPGroup(group_id)
```

## Enumerate all points in R8.1 only

```python
point_ids = tde4.getPointList(pgroup_id, 0)
```

The R8.1 structured contract says `0` (or omission) returns all points and `1` returns only selected points. The R7.1 and R8.0 command summaries show the parameter name but not this selector contract; do not copy this call into older-version code until the value is verified there.

## Check one 2D observation before reading its position

```python
if tde4.isPointPos2DValid(pgroup_id, point_id, camera_id, frame) == 1:
    position_2d = tde4.getPointPosition2D(
        pgroup_id, point_id, camera_id, frame
    )
```

This uses the documented validity getter before the documented position getter. The example does not change the camera, frame, point, or scene.
