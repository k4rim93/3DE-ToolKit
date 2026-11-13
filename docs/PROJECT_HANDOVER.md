# 3DE-ToolKit — Project Handover

## Purpose
Build a professional, maintainable Python toolkit for 3DEqualizer matchmove workflows. The toolkit should reduce repetitive artist tasks, provide reliable scene diagnostics, and grow through small, independently testable tools.

## User / workflow context
- Primary user: an experienced Senior Matchmove Artist and On-Set Supervisor.
- **Current supported target: 3DEqualizer R7.1 only.** R8.0 and R8.1 are out of current scope. Do not spend time implementing or validating compatibility for them unless the owner changes this decision.
- R7.1 is the sole acceptance target for API choices, UI behavior, syntax/runtime assumptions, and in-application testing.
- Priority order for future integrations: 3DEqualizer first, Maya second, Nuke third. This repository is specifically the 3DE toolkit.
- Prefer native 3DE UI and native APIs. Avoid external Python dependencies unless separately justified and approved.

## Architecture principles
1. **Read-only by default.** Inspection and reporting must not mutate the current 3DE scene.
2. **Explicit consent for writes.** Any operation that changes scene data must clearly describe the changes and require an explicit user confirmation immediately before execution.
3. **R7.1-first, not speculative multi-version support.** Use only APIs verified for R7.1. Do not add compatibility branches for R8.x in this phase.
4. **Fail safely.** Missing APIs, unsupported features, malformed scene data, and per-item errors should be reported without crashing the whole inspection.
5. **Artist-first UX.** Keep tools discoverable, concise, and predictable. Each tool must have a nearby `!` help control.
6. **No hidden side effects.** No scene edits, file overwrites, environment changes, dependency installation, or external network calls unless explicitly approved.
7. **Small modules.** Keep each tool independently understandable and testable.

## Initial toolkit modules
- Scene Inspector — inspect scene structure and produce a readable report.
- API Reference — surface verified R7.1 API guidance.
- Quick Inspection — a fast overview for routine checks.
- Deep Inspection — optional detailed tracking / point observations analysis.

## Script help contract
Every tool entry in the UI must have a `!` control. Help content must state:
- What it does
- When to use it
- How to use it
- Required inputs
- Expected output
- Safety level: Read Only or Requires Confirmation

## Protected existing work
The user's existing Maya-to-3DE exporter/importer is out of scope and must remain untouched. Its protected behavior includes:
- Camera-relative OBJ export.
- Object-relative OBJ export.
- Existing `import.json` structure.
- Existing CAMERA and OBJECT Point Group logic.

Do not import, copy, refactor, rename, overwrite, delete, or integrate those scripts as part of this toolkit unless the user gives separate explicit approval.

## Public repository warning
This repository is public. Never commit production footage, client/project names that are not approved for publication, credentials, tokens, private paths, personal data, licensed third-party scripts, or proprietary studio material. Commit only original material the owner is authorized to publish.

## Collaboration model
- GitHub is the shared source of truth for specifications, code, tests, and review history.
- Work on a dedicated feature/docs branch; do not commit directly to `main`.
- Codex may implement locally only after the owner approves the specific implementation task, then push changes to a branch and summarize tests and limitations.
- Review changes before merging. No merge to `main` without the owner's explicit approval.
- ChatGPT reviews specifications, API claims, diffs, safety, and test evidence when the user asks or shares an update. It cannot directly control the user's local Codex Desktop session or observe it continuously in the background.

## Current project status
- Repository: `k4rim93/3DE-ToolKit`
- Current working branch: `docs/project-handover-foundation`
- **Active target: 3DEqualizer R7.1 only.**
- R8.0/R8.1 notes in existing research are historical reference only, not current implementation requirements.
- Existing prototype scripts require a read-only audit against R7.1 before any further implementation is approved.
