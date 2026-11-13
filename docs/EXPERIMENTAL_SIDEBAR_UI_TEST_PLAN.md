# Experimental Sidebar UI — R7.1 Test Plan

**Branch:** `feature/r71-sidebar-ui-prototype`  
**Status:** Experimental; do not merge before owner validation.

## Files to install together

Copy these three files into the existing 3DEqualizer R7.1 custom Python scripts folder:

- `scripts/kikz_toolkit.py`
- `scripts/kikz_toolkit_ui.py`
- `scripts/scene_inspector.py`

Do not overwrite the Maya-to-3DE exporter/importer or unrelated scripts. Refresh/rescan the Python scripts menu using the normal 3DE UI workflow.

## Expected behavior

1. A single `Kikz Toolkit` menu entry appears.
2. Launching it opens one Custom Requester titled `Kikz Toolkit — Workspace`.
3. The requester contains a left navigation list and a right report/content area.
4. Select Dashboard, Scene Inspector, Quick Inspection, Deep Inspection, Camera Tools, Tracking Tools, Point Group Tools, Utilities, or Help & API; press **Open Section**.
5. Inspection sections populate the same requester with read-only reports and contextual help.
6. **Back** returns to the navigation/dashboard state; **Close** exits.
7. Camera Tools, Tracking Tools, Point Group Tools and Utilities are explicitly informational placeholders, not functional scene tools.
8. No scene data is modified and no report file is written.

## Safe test procedure

- Use a disposable copy of a non-critical R7.1 project.
- Confirm the detected version is R7.1.
- Test each navigation entry.
- Test Scene Inspector and Quick Inspection on an empty/minimal scene and a normal test scene.
- Test Deep Inspection only after the R7.1 point enumeration semantics have been accepted for the installed build.
- Close the requester using both Close and the window close control if available.
- Re-open the toolkit and confirm there is no stale requester or duplicate UI.
- Confirm no project dirty-state change and no unexpected console traceback.

## Known limitations / unverified items

- The UI has not been run inside 3DEqualizer R7.1.
- Widget attachment geometry, list root-item index semantics, requester button return values, re-posting the same requester, and close lifecycle require in-app validation.
- The R7.1 command summary documents the functions used (`createCustomRequester`, `postCustomRequester`, `addListWidget`, `insertListWidgetItem`, `getListWidgetSelectedItems`, `addTextAreaWidget`, `clearTextAreaWidget`, `appendTextAreaWidgetString`, `setWidgetAttachModes`, `setWidgetOffsets`, and `deleteCustomRequester`), but does not fully specify every layout/interaction semantic.
- Module import resolution for the three sibling files must be verified in the user's actual R7.1 custom-script folder.
- No static Python compile check, mocked test, or in-app test has yet been run in this handoff.

## Safety

This branch does not modify `main`. The existing Scene Inspector collector is called as-is; no exporter/importer files are touched. The new navigation sections are not advertised as functional tools until implemented and tested.
