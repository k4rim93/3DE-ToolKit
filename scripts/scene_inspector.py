"""Read-only scene inspection for 3DEqualizer R7.1.

No scene setters, calculations, file writes, or network access are used.
Deep inspection validates point-list completeness and calculated-3D status
before requesting calculated coordinates.
"""

try:
    import tde4
except ImportError:
    tde4 = None


def _call(api, name, *args):
    function = getattr(api, name, None)
    if not callable(function):
        return None, "API unavailable: %s" % name
    try:
        return function(*args), None
    except Exception as error:
        return None, "%s: %s" % (name, error)


def _as_text(value):
    try:
        return str(value)
    except Exception:
        return "<unprintable>"


def _is_r71(version):
    return "7.1" in str(version)


def _collect_cameras(api, issues, quick=False):
    cameras = []
    count, error = _call(api, "getNoCameras")
    if error:
        issues.append(error)
        return cameras
    try:
        count = int(count)
    except Exception:
        issues.append("getNoCameras returned a non-integer value.")
        return cameras
    if count < 0:
        issues.append("getNoCameras returned a negative count.")
        return cameras
    if count == 0:
        return cameras

    camera_id, error = _call(api, "getFirstCamera")
    if error:
        issues.append(error)
        return cameras
    for index in range(count):
        if camera_id is None:
            issues.append("Camera iteration ended before getNoCameras count.")
            break
        item = {"id": camera_id}
        getters = [("name", "getCameraName"), ("type", "getCameraType")]
        if not quick:
            getters.extend([
                ("frame_count", "getCameraNoFrames"),
                ("fps", "getCameraFPS"),
                ("sequence", "getCameraSequenceAttr"),
                ("lens_id", "getCameraLens"),
            ])
        for field, api_name in getters:
            value, field_error = _call(api, api_name, camera_id)
            if field_error:
                issues.append("Camera %s: %s" % (_as_text(camera_id), field_error))
            else:
                item[field] = value
        lens_id = item.get("lens_id")
        if lens_id:
            lens_name, lens_error = _call(api, "getLensName", lens_id)
            if lens_error:
                issues.append("Camera %s lens: %s" % (_as_text(camera_id), lens_error))
            else:
                item["lens_name"] = lens_name
        cameras.append(item)
        if index + 1 < count:
            camera_id, error = _call(api, "getNextCamera", camera_id)
            if error:
                issues.append(error)
                break
    return cameras


def _collect_point_groups(api, issues, quick=False):
    groups = []
    count, error = _call(api, "getNoPGroups")
    if error:
        issues.append(error)
        return groups
    try:
        count = int(count)
    except Exception:
        issues.append("getNoPGroups returned a non-integer value.")
        return groups
    if count < 0:
        issues.append("getNoPGroups returned a negative count.")
        return groups
    if count == 0:
        return groups

    group_id, error = _call(api, "getFirstPGroup")
    if error:
        issues.append(error)
        return groups
    for index in range(count):
        if group_id is None:
            issues.append("Point-group iteration ended before getNoPGroups count.")
            break
        item = {"id": group_id}
        getters = [("name", "getPGroupName"), ("type", "getPGroupType")]
        if not quick:
            getters.extend([
                ("enabled", "getPGroupEnabledFlag"),
                ("point_count", "getNoPoints"),
            ])
        for field, api_name in getters:
            value, field_error = _call(api, api_name, group_id)
            if field_error:
                issues.append("Point group %s: %s" % (_as_text(group_id), field_error))
            else:
                item[field] = value
        groups.append(item)
        if index + 1 < count:
            group_id, error = _call(api, "getNextPGroup", group_id)
            if error:
                issues.append(error)
                break
    return groups


def _collect_deep_r71(api, cameras, groups, issues):
    points = []
    current_frames = {}
    for camera in cameras:
        camera_id = camera["id"]
        frame, error = _call(api, "getCurrentFrame", camera_id)
        if error:
            issues.append("Camera %s: %s" % (_as_text(camera_id), error))
        else:
            current_frames[camera_id] = frame

    for group in groups:
        group_id = group["id"]
        expected_count = group.get("point_count")
        point_ids, error = _call(api, "getPointList", group_id, 0)
        if error:
            issues.append("Point group %s: %s" % (_as_text(group_id), error))
            continue
        if not isinstance(point_ids, (list, tuple)):
            issues.append("Point group %s: getPointList returned a non-list; skipped." %
                          _as_text(group_id))
            continue
        if expected_count is not None:
            try:
                if len(point_ids) != int(expected_count):
                    issues.append(
                        "Point group %s: point-list count (%d) does not match "
                        "getNoPoints (%s); group skipped." %
                        (_as_text(group_id), len(point_ids), _as_text(expected_count))
                    )
                    continue
            except Exception:
                issues.append("Point group %s: invalid point count; group skipped." %
                              _as_text(group_id))
                continue

        for point_id in point_ids:
            point = {"group_id": group_id, "id": point_id}
            for field, api_name in (
                ("name", "getPointName"),
                ("survey_3d", "getPointSurveyPosition3D"),
                ("survey_mode", "getPointSurveyMode"),
            ):
                value, field_error = _call(api, api_name, group_id, point_id)
                if field_error:
                    issues.append("Point %s: %s" % (_as_text(point_id), field_error))
                else:
                    point[field] = value

            status, status_error = _call(
                api, "getPointCalculated3DStatus", group_id, point_id
            )
            if status_error:
                issues.append("Point %s calculated-3D status: %s" %
                              (_as_text(point_id), status_error))
                point["calculated_3d_status"] = "unavailable"
            else:
                point["calculated_3d_status"] = status
                if status in ("CALCULATED", "TRIANGULATED"):
                    value, value_error = _call(
                        api, "getPointCalcPosition3D", group_id, point_id
                    )
                    if value_error:
                        issues.append("Point %s calculated-3D position: %s" %
                                      (_as_text(point_id), value_error))
                    else:
                        point["calculated_3d"] = value
                elif status == "NOT_CALCULATED":
                    point["calculated_3d"] = "Not calculated"
                else:
                    issues.append("Point %s: unknown calculated-3D status %s; "
                                  "position not requested." %
                                  (_as_text(point_id), _as_text(status)))

            observations = []
            for camera_id, frame in current_frames.items():
                valid, valid_error = _call(
                    api, "isPointPos2DValid", group_id, point_id, camera_id, frame
                )
                if valid_error:
                    issues.append("Point %s observation: %s" %
                                  (_as_text(point_id), valid_error))
                    continue
                observation = {"camera_id": camera_id, "frame": frame, "valid": valid}
                if valid == 1:
                    position, position_error = _call(
                        api, "getPointPosition2D", group_id, point_id, camera_id, frame
                    )
                    if position_error:
                        issues.append("Point %s 2D position: %s" %
                                      (_as_text(point_id), position_error))
                    else:
                        observation["position"] = position
                observations.append(observation)
            point["observations"] = observations
            points.append(point)
    return points


def collect_scene(api=None, deep=False, quick=False):
    api = api or tde4
    if api is None:
        return {"version": "unknown", "cameras": [], "point_groups": [],
                "points": [], "issues": ["The 3DE tde4 module is unavailable."],
                "deep": bool(deep)}
    version, error = _call(api, "get3DEVersion")
    issues = []
    if error:
        issues.append(error)
        version = "unknown"

    cameras = _collect_cameras(api, issues, quick=quick)
    groups = _collect_point_groups(api, issues, quick=quick)
    points = []
    if deep:
        if _is_r71(version):
            points = _collect_deep_r71(api, cameras, groups, issues)
        else:
            issues.append(
                "Deep Inspection is restricted to detected 3DEqualizer R7.1. "
                "Version string did not identify R7.1; point-level calls were skipped."
            )
    return {
        "version": version, "cameras": cameras, "point_groups": groups,
        "points": points, "issues": issues, "deep": bool(deep),
    }


def format_report(result, quick=False):
    lines = [
        "Kikz Toolkit — Scene Inspector",
        "Target: 3DEqualizer R7.1",
        "Safety: READ ONLY — no scene changes",
        "Detected version: %s" % _as_text(result.get("version", "unknown")),
        "Cameras: %d" % len(result.get("cameras", [])),
        "Point groups: %d" % len(result.get("point_groups", [])),
        "", "CAMERAS",
    ]
    for camera in result.get("cameras", []):
        lines.append("- %s [%s]" % (
            _as_text(camera.get("name", camera.get("id", "?"))),
            _as_text(camera.get("type", "type unavailable"))))
        details = []
        for label, key in (("frames", "frame_count"), ("fps", "fps"),
                           ("sequence", "sequence"), ("lens", "lens_name")):
            if key in camera:
                details.append("%s=%s" % (label, _as_text(camera[key])))
            elif key == "lens_name" and "lens_id" in camera:
                details.append("lens_id=%s" % _as_text(camera["lens_id"]))
        if details:
            lines.append("  " + "; ".join(details))

    lines.extend(["", "POINT GROUPS"])
    for group in result.get("point_groups", []):
        lines.append("- %s [%s] enabled=%s points=%s" % (
            _as_text(group.get("name", group.get("id", "?"))),
            _as_text(group.get("type", "type unavailable")),
            _as_text(group.get("enabled", "unknown")),
            _as_text(group.get("point_count", "unknown"))))

    if result.get("deep") and not quick:
        lines.extend(["", "DEEP POINT DATA"])
        for point in result.get("points", []):
            lines.append("- %s | group=%s | calc3D status=%s | calc3D=%s | "
                         "survey3D=%s | survey=%s" % (
                _as_text(point.get("name", point.get("id", "?"))),
                _as_text(point.get("group_id", "?")),
                _as_text(point.get("calculated_3d_status", "unknown")),
                _as_text(point.get("calculated_3d", "unavailable")),
                _as_text(point.get("survey_3d", "unavailable")),
                _as_text(point.get("survey_mode", "unavailable"))))
            for observation in point.get("observations", []):
                line = "  camera=%s frame=%s valid=%s" % (
                    _as_text(observation.get("camera_id")),
                    _as_text(observation.get("frame")),
                    _as_text(observation.get("valid")))
                if "position" in observation:
                    line += " position=%s" % _as_text(observation["position"])
                lines.append(line)

    if result.get("issues"):
        lines.extend(["", "PARTIAL RESULTS / DIAGNOSTICS"])
        lines.extend(["- %s" % _as_text(issue) for issue in result["issues"]])
    return "\n".join(lines)


def show_report(report, title="Kikz Toolkit — Scene Inspector"):
    api = tde4
    if api is None:
        print(report)
        return
    requester, error = _call(api, "createCustomRequester")
    if error:
        print(report)
        return
    try:
        unused, error = _call(api, "addTextAreaWidget", requester, "report", "Report", 28, 0)
        if error:
            print(report)
            return
        unused, error = _call(api, "appendTextAreaWidgetString", requester, "report", report)
        if error:
            print(report)
            return
        unused, error = _call(api, "postCustomRequester", requester, title, 900, 620, "Close")
        if error:
            print(report)
    finally:
        _call(api, "deleteCustomRequester", requester)


def run_inspection(deep=False, quick=False):
    try:
        result = collect_scene(deep=deep, quick=quick)
        show_report(format_report(result, quick=quick))
        return result
    except Exception as error:
        message = "Inspection stopped safely after an unexpected Python error: %s" % error
        print(message)
        return {"version": "unknown", "cameras": [], "point_groups": [],
                "points": [], "issues": [message], "deep": bool(deep)}
