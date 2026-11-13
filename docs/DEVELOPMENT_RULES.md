# Development Rules

These rules apply to every contributor and coding agent working in this repository.

## Branch and review discipline
- Never work directly on `main`.
- Create a focused branch from the latest `main`.
- Keep changes scoped and commits understandable.
- Open a pull request for review.
- Never merge, rebase destructively, force-push, or delete branches without explicit owner approval.
- Before editing, inspect the repository tree and read relevant files. Do not assume the repository is empty.

## Protected scope
Do not modify, overwrite, rename, delete, or copy into this repository any existing Maya-to-3DE exporter/importer code unless separately approved. Preserve its camera-relative OBJ, object-relative OBJ, `import.json`, CAMERA Point Group, and OBJECT Point Group behavior.

Do not alter Maya, Nuke, ComfyUI, system Python, PATH, or any unrelated project/environment.

## API correctness
- Official 3DEqualizer documentation is the authority for API availability and signatures.
- Verify R7.1, R8.0, and R8.1 independently.
- Never fabricate function names, signatures, parameters, return types, or behavior.
- Use capability detection for version differences.
- Label uncertain or undocumented behavior clearly and keep it out of production paths until verified.

## Safety
- Default to read-only scene access.
- A write operation must be clearly identified, preview its intended changes, and request explicit confirmation immediately before applying them.
- No automatic scene cleanup, point deletion, camera changes, lens changes, or geometry changes.
- No silent file writes or overwrites. Use explicit output paths and safe collision handling.
- No package installation or environment mutation without approval.
- Do not access the network from inside 3DE scripts unless explicitly approved.

## Code quality
- Prefer the standard library and 3DE's documented built-in Python environment.
- Avoid unnecessary dependencies.
- Keep UI, API compatibility, data collection, and report formatting separated.
- Handle errors at the smallest useful scope and include actionable diagnostics.
- Keep names and help text clear for working matchmove artists.
- Do not add placeholder buttons that appear functional but do nothing.

## Validation and reporting
For every change, report:
1. Files changed and why.
2. APIs used and the official version-specific references checked.
3. Static checks run and their exact results.
4. Mocked tests run, if any.
5. In-application tests run, with exact 3DE version, if any.
6. Known limitations and anything not tested.

Never say a feature is tested in 3DE unless it was actually run inside that exact application/version.

## Public repository hygiene
Before every commit, inspect staged files. Do not commit credentials, tokens, private user data, production media, client materials, proprietary third-party code, or private machine paths. This repository is public.
