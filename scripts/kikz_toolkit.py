# 3DE4.script.name: Scene Inspector
# 3DE4.script.gui: 3DE4::Kikz Toolkit
# 3DE4.script.addlabel: Scene Inspector !
# 3DE4.script.addlabel: Quick Inspection
# 3DE4.script.addlabel: Quick Inspection !
# 3DE4.script.addlabel: Deep Inspection
# 3DE4.script.addlabel: Deep Inspection !
# 3DE4.script.addlabel: API Reference
# 3DE4.script.addlabel: API Reference !
"""3DEqualizer menu entry points for the read-only Kikz Toolkit."""

try:
    import tde4
except ImportError:
    tde4 = None

try:
    import scene_inspector
except ImportError:
    scene_inspector = None


_HELP = {
    "Scene Inspector": (
        "What it does: summarizes cameras, point groups, frame metadata, and point counts.\n"
        "When to use it: for a read-only overview of the open 3DE scene.\n"
        "How to use it: choose Scene Inspector from the Kikz Toolkit menu.\n"
        "Required inputs: an open 3DE project; no user-entered values.\n"
        "Expected output: a native requester with the available scene summary.\n"
        "Safety level: Read Only."
    ),
    "Quick Inspection": (
        "What it does: shows a compact camera and point-group overview.\n"
        "When to use it: for a fast routine check.\n"
        "How to use it: choose Quick Inspection from the Kikz Toolkit menu.\n"
        "Required inputs: an open 3DE project; no user-entered values.\n"
        "Expected output: a compact native scene report.\n"
        "Safety level: Read Only."
    ),
    "Deep Inspection": (
        "What it does: adds per-point calculated/survey data and valid 2D observations "
        "at each camera's current frame.\n"
        "When to use it: when a detailed point-level snapshot is needed.\n"
        "How to use it: choose Deep Inspection from the Kikz Toolkit menu.\n"
        "Required inputs: an open 3DE project. R7.1 is the primary supported release; "
        "deep point details remain disabled there until its selector behavior is verified.\n"
        "Expected output: a detailed read-only report.\n"
        "Safety level: Read Only."
    ),
    "API Reference": (
        "What it does: displays the toolkit's verified API scope and version caveats.\n"
        "When to use it: to review the data sources used by the inspector.\n"
        "How to use it: choose API Reference from the Kikz Toolkit menu.\n"
        "Required inputs: none.\n"
        "Expected output: a short API and compatibility summary.\n"
        "Safety level: Read Only."
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
        print("scene_inspector.py must be installed beside kikz_toolkit.py.")
        return

    label, error = scene_inspector._call(tde4, "getLastScriptMenuLabel")
    if error:
        print(error)
        return
    label = str(label or "Scene Inspector")

    if label.endswith(" !"):
        base_label = label[:-2]
        _show(_HELP.get(base_label, "No help is available."), base_label + " Help")
        return
    if label == "API Reference":
        _show(
            "Verified in R7.1, R8.0, and R8.1 summaries: version, camera, point-group, "
            "and point getter names/signatures.\n"
            "Deep point-list selection semantics are documented here for R8.1 only.\n"
            "See docs/API_REFERENCE.md and docs/VERSION_COMPATIBILITY.md in the repository.\n"
            "Read Only.",
            "Kikz Toolkit — API Reference",
        )
        return
    if scene_inspector is None:
        print("scene_inspector.py must be installed beside kikz_toolkit.py.")
        return
    if label == "Deep Inspection":
        scene_inspector.run_inspection(deep=True)
    else:
        scene_inspector.run_inspection(quick=(label == "Quick Inspection"))


if __name__ == "__main__":
    main()
