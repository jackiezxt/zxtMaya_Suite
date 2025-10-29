# ZXT Suite Architecture Plan

## Goals
- Deliver Maya tools as a modular suite to external vendors while preserving shared core functionality.
- Reuse a common UI component library across Maya and future DCC suites.
- Provide a pipeline-level launcher that orchestrates environment setup for multiple DCC applications.

## Repository Roles
- `zxtMaya_Suite`: Primary Maya package containing `core/` runtime and tool submodules under `tools/`.
- Tool repositories (e.g., `zxtMaya_Alembic`, `zxtMaya_Validate`): Hold feature-specific code, tests, and metadata consumed by the suite.
- `zxtUI_Library`: Fork of `dayu_widgets` plus custom styling and utilities; referenced by each suite for consistent UI.
- Future suites (`zxtNuke_Suite`, `zxtUE_Suite`, `zxtPS_Suite`, `zxtBlender_Suite`, `zxtHoudini_Suite`): Follow the same pattern of core runtime, tool submodules, and shared UI library.
- `zxtPipeline_Launcher` (planned): Separate pipeline repository that manages project selection, environment variables, and launches DCC applications with the correct suite version.

## Submodule and Metadata Strategy
- Keep Maya tools as Git submodules inside `tools/`, mirroring ZooTools. Supply vendors with `zxtMaya_Suite` and instruct them to run `git submodule update --init --recursive`.
- Introduce per-tool metadata file (e.g., `tool_manifest.yaml`) describing menu categories, shelf buttons, icons, and dependencies.
- Extend `suite_manifest.json` and installer scripts to ingest tool metadata and register Maya menus and shelves automatically.

## Installer Flow
- Continue shipping `dragdropinstall.py` for drag-and-drop installation inside Maya.
- Update the installer and core runtime to:
  - Load `suite_manifest.json` entries.
  - Discover tool metadata to build menus and shelves without hard-coding each tool.
  - Validate submodule availability and highlight missing content.

## Launcher Concept
- Maintain launcher as an independent repository to avoid coupling pipeline tooling with a single DCC suite.
- Responsibilities:
  - Present projects and DCC application list (Maya, Nuke, Houdini, Blender, Photoshop, etc.).
  - Resolve project configuration to environment variables and suite versions.
  - Ensure target suite repositories (e.g., `zxtMaya_Suite`) are updated or checked out to the expected revision before launching.
- Suites remain self-installable; launcher adds centralized control similar to ShotGrid Desktop.

## UI Library Integration
- Vendor `dayu_widgets` via `zxtUI_Library`; expose a thin API for theming and common widgets.
- Suites import UI helpers through a stable module path (e.g., `core/ui/widgets`).
- Document Qt compatibility requirements per DCC (PySide2 for Maya, Nuke, and Houdini; investigate PySide distribution for Blender and Photoshop).

## Recommended Next Steps
1. Finalize `zxtUI_Library` structure and write usage guidelines in its README.
2. Choose one Maya tool submodule as a pilot to adopt the metadata format and UI library.
3. Enhance `zxtMaya_Suite` core loader and installer to read metadata and generate menus and shelves dynamically.
4. Once the Maya flow is stable, scaffold the `zxtPipeline_Launcher` repository with minimal project to Maya launch support.
5. Replicate the suite template for other DCCs, reusing UI library and metadata conventions.

## Notes
- Retain ASCII-only paths and keep configuration in JSON or YAML for consistent automation.
- Document new workflows in `docs/` (for example, metadata schema and launcher usage) as features mature.


## Bundle Cache & YAML Configuration (Planned)
- Move away from git submodules for shared libraries; adopt ShotGrid-style YAML descriptors that list required packages and versions.
- Standard design:
  - `requirements/packages.yaml` enumerates shared dependencies (e.g., `zxtUI_Library`), with location types (`git`, `path`) and version pins.
  - A bundle cache directory (e.g., `%APPDATA%/zxtTools/bundle_cache`) stores downloaded dependencies; the cache is shared across all suites and launcher.
  - A resolver script reads YAML, downloads/upgrades packages into the cache, and exposes the paths to each environment (Maya, Nuke, UE, etc.).
- Adapt existing startup scripts (`start_maya_suite.bat` / future launcher) to parse YAML, inject resolved paths into `sys.path`/environment, and replace manual submodule pointers.
- Benefits:
  - One central UI library (and other shared packages) with version control via YAML.
  - Easier cross-suite upgrades—update YAML once, run resolver everywhere.
  - launcher can reuse the same package cache for all DCCs.
- Incremental plan:
  1. Implement resolver/loader for Maya suite.
  2. Update tools to read manifests from resolved cache paths.
  3. Extend same mechanism to future suites (`zxtNuke_Suite`, `zxtUE_Suite`, etc.) and `zxtPipeline_Launcher`.

