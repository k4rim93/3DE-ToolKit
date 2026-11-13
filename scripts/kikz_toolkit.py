# 3DE4.script.name: Kikz Toolkit
# 3DE4.script.gui: 3DE4::Kikz Toolkit
"""Single-window launcher for the 3DEqualizer R7.1 Kikz Toolkit."""

try:
    import tde4
except ImportError:
    tde4 = None

try:
    import kikz_toolkit_ui
except ImportError as import_error:
    kikz_toolkit_ui = None
    _IMPORT_ERROR = import_error
else:
    _IMPORT_ERROR = None


def main():
    if tde4 is None:
        print("Kikz Toolkit requires the 3DE tde4 module.")
        return
    if kikz_toolkit_ui is None:
        message = (
            "Kikz Toolkit UI module could not be imported. "
            "Install kikz_toolkit.py, kikz_toolkit_ui.py and "
            "scene_inspector.py together. Details: %s" % _IMPORT_ERROR
        )
        try:
            tde4.postQuestionRequester("Kikz Toolkit", message, "Close")
        except Exception:
            print(message)
        return
    kikz_toolkit_ui.main()


if __name__ == "__main__":
    main()
