# Development Rules

These rules apply to every contributor and coding agent working in this repository.

## Active version scope
- **Support and test 3DEqualizer R7.1 only.**
- R8.0 and R8.1 are out of scope unless the owner explicitly changes this decision.
- Do not add R8.x compatibility branches, APIs, or acceptance requirements in the current phase.
- Official R7.1 documentation is the authority for API availability and signatures.

## Branch and review discipline
- Never work directly on `main`.
- Work only on the currently assigned feature/docs branch unless the owner approves another branch.
- Keep changes scoped and commits understandable.
- Push changes to the working branch for review.
- Never merge, rebase destructively, force-push, or delete branches without explicit owner approval.
- Before editing, inspect the repository tree and read relevant files.

## Protected scope
Do not modify, overwrite, rename, delete, or copy into this repository any existing Maya-to-3DE exporter/importer code unless separately approved. Preserve its camera-relative OBJ, object-relative OBJ, `import.json`, CAMERA Point Group, and OBJECT Point Group behavior.
Do not alter Maya, Nuke, ComfyUI, system Python, PATH, or any unrelated project/environment.

## API correctness
- Verify every API against the official **R7.1** documentation.
- Never fabricate function names, signatures, parameters, return types, or behavior.
- Do not use R8.0/R8.1 API documentation as proof of R7.1 support.
- Label uncertain or undocumented behavior clearly and keep it out of production paths.

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
- Keep UI, API access, data collection, and report formatting separated.
- Handle errors at the smallest useful scope and include actionable diagnostics.
- Keep names and help text clear for working matchmove artists.
- Do not add placeholder buttons that appear functional but do nothing.

## Validation and reporting
For every change, report:
1. Files changed and why.
2. R7.1 APIs used and official documentation references checked.
3. Static checks run and exact results.
4. Mocked tests run, if any.
5. In-application tests run in 3DEqualizer R7.1, if any.
6. Known limitations and anything not tested.

Never say a feature is tested in 3DE unless it was actually run inside R7.1.

## Public repository hygiene
Before every commit, inspect staged files. Do not commit credentials, tokens, private user data, production media, client materials, proprietary third-party code, or private machine paths. This repository is public.
