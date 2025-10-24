# Repository Guidelines

## Project Structure & Module Organization
- `core/` — shared runtime for all Maya tools, includes `scripts/core/pipeline/` for configuration loaders and `data/config/` for project templates.
- `tools/` — Git submodules pointing to tool-specific repositories (e.g., `tools/zxtMaya_Alembic`). Run `git submodule update --init --recursive` after cloning.
- `docs/` — working notes and integration plans. Add new guides here (e.g., `docs/dev_env_maya2026.md`).
- `suite_manifest.json` & `.mod` — describe how the suite is mounted inside Maya.

## Build, Test, and Development Commands
- `conda activate maya_2026` — enter the Python 3.11 environment aligned with Maya 2026 (see `docs/dev_env_maya2026.md`).
- `python -m pytest core/tests` — run core unit tests; add `-k name` to target a subset.
- `python tools/generate_mod.py --validate` — regenerate and validate `.mod` manifests; runs in CI.

## Coding Style & Naming Conventions
- Python code uses 4-space indentation; prefer type hints and `logging` over prints.
- Configuration stored as JSON overrides seeded by `template.yaml`; keep JSON minimal and UTF-8 encoded.
- Follow existing module layout (e.g., `scripts/core/pipeline/<component>.py`) and snake_case for functions.

## Testing Guidelines
- Primary framework: PyTest. Place tests under `core/tests/` mirroring module structure.
- Name tests `test_<module>.py` with functions `test_behavior_description`.
- Ensure new config behaviour is covered; run `python -m pytest core/tests/test_pipeline.py` before submitting.

## Commit & Pull Request Guidelines
- Commit messages: short imperative summary (`Fix ConfigManager merge`) with optional details in body.
- PRs should describe scope, mention related tool repos/submodules, and include test commands executed.
- Update `docs/session_notes.md` or relevant guides whenever workflow or environment steps change.

## Security & Configuration Tips
- Do not commit secrets or proprietary project paths; store overrides in project-specific JSON that can be templated.
- When adding third-party libraries, vendor them under `core/scripts/packages/thirdparty/` and document usage.
