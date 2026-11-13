"""Kikz Toolkit single-window navigation prototype for 3DEqualizer R7.1.

The UI is read-only. Navigation uses a native list widget and a report area.
No scene setters, calculations, file writes, or network access are used.
"""
try:
    import tde4
except ImportError:
    tde4 = None

try:
    import scene_inspector
except ImportError:
    scene_inspector = None

_PAGES = [
    ("Dashboard", "dashboard"),
    ("Scene Inspector", "scene"),
    ("Quick Inspection", "quick"),
    ("Deep Inspection", "deep"),
    ("Camera Tools", "camera"),
    ("Tracking Tools", "tracking"),
    ("Point Group Tools", "points"),
    ("Utilities", "utilities"),
    ("Help & API", "help"),
]

_PAGE_TEXT = {
    "dashboard": (
        "KIKZ TOOLKIT\n"
        "3DEqualizer R7.1 only\n\n"
        "A single workspace for scene inspection and future matchmove tools.\n\n"
        "Select a section from the navigation list, then choose Open Section.\n"
        "Scene access is read-only by default."
    ),
    "camera": (
        "CAMERA TOOLS\n\n"
        "This section is reserved for future camera utilities.\n"
        "No placeholder action is exposed as functional."
    ),
    "tracking": (
        "TRACKING TOOLS\n\n"
        "This section is reserved for future tracking utilities.\n"
        "No tracking operation is executed by this prototype."
    ),
    "points": (
        "POINT GROUP TOOLS\n\n"
        "This section is reserved for future point-group utilities.\n"
        "No scene data is modified."
    ),
    "utilities": (
        "UTILITIES\n\n"
        "Future utility tools will be hosted here after separate review."
    ),
    "help": (
        "KIKZ TOOLKIT — R7.1\n\n"
        "WHAT: Unified access to the toolkit sections.\n"
        "WHEN: Use this as the main entry point inside 3DE.\n"
        "HOW: Select a section on the left and choose Open Section.\n"
        "INPUTS: An open 3DE project for inspection tools.\n"
        "OUTPUT: Reports appear in this toolkit window.\n"
        "SAFETY: Read-only. No scene changes or file writes.\n\n"
        "The Camera, Tracking, Point Group and Utilities sections are "
        "navigation placeholders only in this prototype."
    ),
}


def _safe_call(name, *args):
    function = getattr(tde4, name, None)
    if not callable(function):
        raise RuntimeError("R7.1 API unavailable: %s" % name)
    return function(*args)


def _page_text(key):
    if key == "scene" or key == "quick" or key == "deep":
        if scene_inspector is None:
            return "Scene Inspector module could not be imported. Install scene_inspector.py beside this file."
        result = scene_inspector.collect_scene(
            deep=(key == "deep"), quick=(key == "quick")
        )
        return scene_inspector.format_report(result, quick=(key == "quick"))
    return _PAGE_TEXT.get(key, "No page content is available.")


def _set_page_content(requester, page_key):
    _safe_call("clearTextAreaWidget", requester, "page_content")
    _safe_call("appendTextAreaWidgetString", requester, "page_content",
               _page_text(page_key))


def main():
    if tde4 is None:
        print("Kikz Toolkit requires the 3DE tde4 module.")
        return
    requester = None
    try:
        requester = _safe_call("createCustomRequester")
        _safe_call("addLabelWidget", requester, "brand",
                   "KIKZ TOOLKIT  |  R7.1", "ALIGN_LABEL_LEFT")
        _safe_call("addListWidget", requester, "navigation",
                   "Navigation", 0, 10)
        for label, key in _PAGES:
            _safe_call("insertListWidgetItem", requester, "navigation",
                       label, key, "LIST_ITEM_ATOM", -1)
        _safe_call("addLabelWidget", requester, "hint",
                   "Choose a section on the left.", "ALIGN_LABEL_LEFT")
        _safe_call("addTextAreaWidget", requester, "page_content",
                   "Workspace", 24, 0)
        _safe_call("appendTextAreaWidgetString", requester, "page_content",
                   _PAGE_TEXT["dashboard"])

        while True:
            result = _safe_call("postCustomRequester", requester,
                                "Kikz Toolkit — Workspace", 900, 620,
                                "Open Section", "Close")
            if result != 1:
                break
            selected = _safe_call("getListWidgetSelectedItems",
                                  requester, "navigation")
            if not selected:
                _safe_call("clearTextAreaWidget", requester, "page_content")
                _safe_call("appendTextAreaWidgetString", requester, "page_content",
                           "Select a section from the navigation list first.")
                continue
            selected_index = int(selected[0])
            if selected_index < 0 or selected_index >= len(_PAGES):
                continue
            page_key = _PAGES[selected_index][1]
            _set_page_content(requester, page_key)

            # Re-post the same requester: one requester, one workspace,
            # no separate tool windows. Back returns to navigation.
            result = _safe_call("postCustomRequester", requester,
                                "Kikz Toolkit — Workspace", 900, 620,
                                "Back", "Close")
            if result != 1:
                break
            _set_page_content(requester, "dashboard")
    except Exception as error:
        try:
            _safe_call("postQuestionRequester", "Kikz Toolkit",
                       "The toolkit UI could not be opened safely:\\n%s" % error,
                       "Close")
        except Exception:
            print("Kikz Toolkit UI error: %s" % error)
    finally:
        if requester is not None:
            _safe_call("deleteCustomRequester", requester)


if __name__ == "__main__":
    main()
