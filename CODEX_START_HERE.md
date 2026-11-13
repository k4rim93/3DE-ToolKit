# Codex Start Here

You are working in the public GitHub repository `k4rim93/3DE-ToolKit`.

## Read first
1. `README.md`
2. `docs/PROJECT_HANDOVER.md`
3. `docs/BUILD_SPEC_PHASE_1.md`
4. `docs/DEVELOPMENT_RULES.md`
5. Inspect the repository tree, current branch, and working-tree status.

## Owner's current decision
**Work with 3DEqualizer R7.1 only for now.** R8.0 and R8.1 are out of scope. Do not implement multi-version support or spend time validating R8.x unless the owner explicitly changes this decision.

## Current assignment
Perform a READ-ONLY audit of the existing prototype scripts:
- `scripts/scene_inspector.py`
- `scripts/kikz_toolkit.py`

Compare every API call and behavior against official R7.1 documentation only. Check calculated 3D status-before-position logic, tracking validity checks, lens access, Custom Requester signatures/assumptions, read-only safety, error handling, and whether each menu item/help action is genuinely functional.

Write the findings to `docs/CODE_AUDIT_REPORT.md`. Report-only: do not modify/create/delete/rename implementation files. Do not run scripts inside 3DE and do not claim runtime validation.

## Hard constraints
- Stay on `docs/project-handover-foundation`.
- Do not commit to or modify `main`.
- Do not implement or modify code until the owner explicitly approves a specific task.
- Do not install packages or modify Python environments / PATH.
- Do not change any 3DE scene.
- Do not touch the user's existing Maya-to-3DE exporter/importer or any unrelated project.
- Do not invent `tde4` APIs or signatures; use R7.1 official docs only.
- This is a public repository: do not add secrets, production assets, client data, or proprietary third-party code.

After the audit, review the report, commit and push the report to the current branch only, and provide the commit SHA and file URL. Then stop and wait for explicit approval.
