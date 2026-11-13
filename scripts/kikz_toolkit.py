# 3DE4.script.name: Scene Inspector
# 3DE4.script.gui: 3DE4::Kikz Toolkit
# 3DE4.script.addlabel: Scene Inspector !
# 3DE4.script.addlabel: Quick Inspection
# 3DE4.script.addlabel: Quick Inspection !
# 3DE4.script.addlabel: Deep Inspection
# 3DE4.script.addlabel: Deep Inspection !
# 3DE4.script.addlabel: API Reference
# 3DE4.script.addlabel: API Reference !
"""3DEqualizer R7.1 read-only Kikz Toolkit menu entry points."""

try:
    import tde4
except ImportError:
    tde4 = None

try:
    import scene_inspector
except ImportError as import_error:
    scene_inspector = None
    _IMPORT_ERROR = import_error
else:
    _IMPORT_ERROR = None


_HELP = {
    "Scene Inspector": (
        "WHAT: Read-only overview of cameras, point groups and scene metadata.\n"
        "WHEN: Initial health check of the open scene.\n"
        "HOW: Choose Scene Inspector.\n"
        "INPUTS: An open 3DE project; no manual input.\n"
        "OUTPUT: Native report requester (console fallback if requester fails).\n"
        "SAFETY: Read-only; no scene data is changed."
    ),
    "Quick Inspection": (
        "WHAT: Compact camera and point-group overview.\n"
        "WHEN: Fast routine scene check.\n"
        "HOW: Choose Quick Inspection.\n"
        "INPUTS: An open 3DE project.\n"
        "OUTPUT: Compact read-only report.\n"
        "SAFETY: Read-only."
    ),
    "Deep Inspection": (
        "WHAT: Point names, calculated-3D status/position, survey data and "
        "current-frame 2D observation validity/positions.\n"
        "WHEN: Point-level snapshot of an R7.1 scene.\n"
        "HOW: Choose Deep Inspection.\n"
        "INPUTS: An open 3DEqualizer R7.1 project. Point enumeration is "
        "cross-checked against the documented point count.\n"
        "OUTPUT: Read-only point report with per-item diagnostics.\n"
        "SAFETY: Read-only; calculated coordinates are requested only after "
        "a CALCULATED or TRIANGULATED status."
    ),
    "API Reference": (
        "KIKZ TOOLKIT — R7.1 ONLY\n"
        "Camera and point-group overview uses documented R7.1 getters.\n"
        "Deep inspection uses getPointList, getNoPoints, "
        "getPointCalculated3DStatus, 2D validity and position getters.\n"
        "Calculated position is requested only for CALCULATED/TRIANGULATED.\n"
        "The report checks getPointList length against getNoPoints.\n"
        "No R8.0/R8.1 compatibility is claimed.\n"
        "Safety: read-only."
    ),
}


def _show(text, title):
    if scene_inspector is None:
        print(text)
    else:
        scene_inspector.show_report(text, title)


def main():
    if tde4 is None:
        print("Kikz Toolkit requires the 3DE tde4 module.")
        return
    if scene_inspector is None:
        print("Kikz Toolkit could not import scene_inspector.py: %s" % _IMPORT_ERROR)
        return

    label, error = scene_inspector._call(tde4, "getLastScriptMenuLabel")
    if error:
        print(error)
        return
    label = str(label or "Scene Inspector")

    if label.endswith(" !"):
        base_label = label[:-2]
        _show(_HELP.get(base_label, "No help is available."), base_label + " Help")
    elif label == "API Reference":
        _show(_HELP["API Reference"], "Kikz Toolkit — R7.1 API Reference")
    elif label == "Deep Inspection":
        scene_inspector.run_inspection(deep=True)
    elif label == "Quick Inspection":
        scene_inspector.run_inspection(quick=True)
    else:
        scene_inspector.run_inspection()


if __name__ == "__main__":
    main()
