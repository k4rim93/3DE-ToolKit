# Version Compatibility

**Priority:** R7.1 is the owner's primary production version and the first target for compatibility verification and in-application validation. R8.0 and R8.1 remain secondary targets.

## Evidence basis

Each release was checked independently against its vendor command summary:

- [R7.1 Python command summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r7.1.txt)
- [R8.0 Python command summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.0.txt)
- [R8.1 Python command summary](https://www.3dequalizer.com/user_daten/sections/tech_docs/txt/py_doc_r8.1.txt)
- [R8.1 structured API reference](https://www.3dequalizer.com/user_daten/sections/tech_docs/py_doc/tde4_with_examples.wtrl.core.rfc-2119.json)

The three summaries contain the exact getter signatures used for the common camera, point-group, point-count, lens-name, and UI calls. Detailed contracts in the structured reference are versioned for R8.1 and are not silently projected backward onto R7.1 or R8.0.

| Capability | R7.1 | R8.0 | R8.1 |
|---|---|---|---|
| Version detection with `get3DEVersion()` | Documented | Documented | Documented |
| Cameras via count plus first/next iteration; name/type/frame/FPS/sequence/lens getters | Documented signatures; not run in app | Documented signatures; not run in app | Documented signatures; not run in app |
| Point groups via count plus first/next iteration; name/type/enabled/point-count getters | Documented signatures; not run in app | Documented signatures; not run in app | Documented signatures; not run in app |
| Per-point names, survey/calculated 3D values, current-frame 2D validity/position | Names/signatures present in summary; not used by current code | Names/signatures present in summary; not used by current code | Detailed point list selector contract documented; deep mode enabled, not run in app |
| Custom Requester modal report display | Signature listed; UI behavior not run | Signature listed; UI behavior not run | Signature listed; UI behavior not run |

## Runtime behavior

- The toolkit does not infer behavior from the major release number except to gate the deep point-list selector to strings containing `8.1`.
- Common overview collection uses count-bounded `getFirst...`/`getNext...` iteration. If an item API is unavailable or raises, the report contains the error and continues where possible.
- Deep inspection is opt-in and reads each camera's current frame only. It does not change the current frame. It is enabled only for R8.1 because the official detailed `getPointList(..., selected_only)` contract explicitly documents `0` as “all points” there.
- On R7.1/R8.0, a requested deep inspection returns the common overview and a clear UNVERIFIED diagnostic; it does not call `getPointList` with an assumed selector value.
- No in-application validation has been performed. The installed versions and 3DE Python runtimes available to the owner are unknown.

## Known compatibility risks

1. The exact text format of `get3DEVersion()` has not been established. The R8.1 detector uses a substring check and will safely withhold deep inspection if the string does not contain `8.1`.
2. End-of-iteration behavior for `getNextCamera` and `getNextPGroup` is not specified in the legacy summaries. The code limits iterations to the documented object count and reports early termination.
3. Custom Requester dimensions, addlabel menu presentation, importing a sibling module from the custom scripts directory, and close/delete behavior require smoke testing in each exact application release.
4. Calculated and survey point getters can fail on absent/unavailable values. These are isolated as per-point diagnostics rather than treated as valid coordinates.

## Verification record

No 3DE application instance was available during this work. No static checks, mocked tests, or in-application smoke tests are claimed. See `docs/PHASE1_INSPECTION_REPORT.md` for the proposed test strategy.
