"""Read-only scene data collection and report display for 3DEqualizer.

Only documented getters are used. Deep point/observation collection is enabled
only for R8.1, whose official API contract documents the selector semantics.
"""

try:
    import tde4
except ImportError:
    tde4 = None


def _call(api, name, *args):
    """Call a documented host API and return (value, error)."""
    function = getattr(api, name, None)
    if not callable(function):
        return None, "API unavailable: %s" % name
    try:
        return function(*args), None
    except Exception as error:
        return None, "%s: %s" % (name, error)


def _version_is_r81(version):
    return "8.1" in str(version)


def _as_text(value):
    try:
        return str(value)
    except Exception:
        return "<unprintable>"


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

    camera_id, error = _call(api, "getFirstCamera")
    if error:
        issues.append(error)
        return cameras

    for unused_index in range(max(0, count)):
        if camera_id is None:
            issues.append("Camera iteration ended before the documented camera count.")
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
        for field, function_name in getters:
            value, field_error = _call(api, function_name, camera_id)
            if field_error:
                issues.append("Camera %s: %s" % (_as_text(camera_id), field_error))
            else:
                item[field] = value
        lens_id = item.get("lens_id")
        if lens_id is not None:
            lens_name, lens_error = _call(api, "getLensName", lens_id)
            if lens_error:
                issues.append("Camera %s lens: %s" % (_as_text(camera_id), lens_error))
            else:
                item["lens_name"] = lens_name
        cameras.append(item)
        if unused_index + 1 < count:
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

    group_id, error = _call(api, "getFirstPGroup")
    if error:
        issues.append(error)
        return groups

    for unused_index in range(max(0, count)):
        if group_id is None:
            issues.append("Point-group iteration ended before the documented count.")
            break
        item = {"id": group_id}
        getters = [("name", "getPGroupName"), ("type", "getPGroupType")]
        if not quick:
            getters.extend([
                ("enabled", "getPGroupEnabledFlag"),
                ("point_count", "getNoPoints"),
            ])
        for field, function_name in getters:
            value, field_error = _call(api, function_name, group_id)
            if field_error:
                issues.append("Point group %s: %s" % (_as_text(group_id), field_error))
            else:
                item[field] = value
        groups.append(item)
        if unused_index + 1 < count:
            group_id, error = _call(api, "getNextPGroup", group_id)
            if error:
                issues.append(error)
                break
    return groups


def _collect_deep_r81(api, cameras, groups, issues):
    """Inspect per-point values and current-frame 2D observations in R8.1."""
    points = []
    camera_ids = [camera["id"] for camera in cameras]
    current_frames = {}
    for camera_id in camera_ids:
        frame, frame_error = _call(api, "getCurrentFrame", camera_id)
        if frame_error:
            issues.append("Camera %s: %s" % (_as_text(camera_id), frame_error))
        else:
            current_frames[camera_id] = frame

    for group in groups:
        group_id = group["id"]
        point_ids, error = _call(api, "getPointList", group_id, 0)
        if error:
            issues.append("Point group %s: %s" % (_as_text(group_id), error))
            continue
        for point_id in point_ids or []:
            point = {"group_id": group_id, "id": point_id}
            for field, function_name in (
                ("name", "getPointName"),
                ("calculated_3d", "getPointCalcPosition3D"),
                ("survey_3d", "getPointSurveyPosition3D"),
                ("survey_mode", "getPointSurveyMode"),
            ):
                value, field_error = _call(api, function_name, group_id, point_id)
                if field_error:
                    issues.append("Point %s: %s" % (_as_text(point_id), field_error))
                else:
                    point[field] = value

            observations = []
            for camera_id in camera_ids:
                if camera_id not in current_frames:
                    continue
                frame = current_frames[camera_id]
                valid, valid_error = _call(
                    api, "isPointPos2DValid", group_id, point_id, camera_id, frame
                )
                if valid_error:
                    issues.append("Point %s: %s" % (_as_text(point_id), valid_error))
                    continue
                observation = {"camera_id": camera_id, "frame": frame, "valid": valid}
                if valid == 1:
                    position, position_error = _call(
                        api, "getPointPosition2D", group_id, point_id, camera_id, frame
                    )
                    if position_error:
                        issues.append("Point %s: %s" % (_as_text(point_id), position_error))
                    else:
                        observation["position"] = position
                observations.append(observation)
            point["observations"] = observations
            points.append(point)
    return points


def collect_scene(api=None, deep=False, quick=False):
    """Return structured read-only scene data and scoped diagnostic messages."""
    api = api or tde4
    if api is None:
        return {"version": "unknown", "cameras": [], "point_groups": [],
                "points": [], "issues": ["The 3DE tde4 module is unavailable."]}

    version, error = _call(api, "get3DEVersion")
    issues = []
    if error:
        issues.append(error)
        version = "unknown"

    cameras = _collect_cameras(api, issues, quick=quick)
    groups = _collect_point_groups(api, issues, quick=quick)
    points = []
    if deep:
        if _version_is_r81(version):
            points = _collect_deep_r81(api, cameras, groups, issues)
        else:
            issues.append(
                "Deep point/observation inspection is disabled outside R8.1: "
                "the selected-only list argument semantics are not verified "
                "for the older releases."
            )

    return {
        "version": version,
        "cameras": cameras,
        "point_groups": groups,
        "points": points,
        "issues": issues,
        "deep": bool(deep),
    }


def format_report(result, quick=False):
    lines = [
        "Kikz Toolkit — Scene Inspector",
        "Safety: Read Only",
        "3DE version: %s" % _as_text(result.get("version", "unknown")),
        "Cameras: %d" % len(result.get("cameras", [])),
        "Point groups: %d" % len(result.get("point_groups", [])),
        "",
        "CAMERAS",
    ]
    for camera in result.get("cameras", []):
        lines.append("- %s [%s]" % (
            _as_text(camera.get("name", camera.get("id", "?"))),
            _as_text(camera.get("type", "type unavailable")),
        ))
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
            _as_text(group.get("point_count", "unknown")),
        ))

    if result.get("deep") and not quick:
        lines.extend(["", "DEEP POINT DATA"])
        for point in result.get("points", []):
            lines.append("- %s | group=%s | calc3D=%s | survey3D=%s | survey=%s" % (
                _as_text(point.get("name", point.get("id", "?"))),
                _as_text(point.get("group_id", "?")),
                _as_text(point.get("calculated_3d", "unavailable")),
                _as_text(point.get("survey_3d", "unavailable")),
                _as_text(point.get("survey_mode", "unavailable")),
            ))
            for observation in point.get("observations", []):
                line = "  camera=%s frame=%s valid=%s" % (
                    _as_text(observation.get("camera_id")),
                    _as_text(observation.get("frame")),
                    _as_text(observation.get("valid")),
                )
                if "position" in observation:
                    line += " position=%s" % _as_text(observation["position"])
                lines.append(line)

    if result.get("issues"):
        lines.extend(["", "PARTIAL RESULTS / DIAGNOSTICS"])
        for issue in result["issues"]:
            lines.append("- %s" % _as_text(issue))
    return "\n".join(lines)


def show_report(report, title="Kikz Toolkit — Scene Inspector"):
    """Display text in a native requester; fall back to the 3DE console."""
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
    result = collect_scene(deep=deep, quick=quick)
    show_report(format_report(result, quick=quick))
    return result
