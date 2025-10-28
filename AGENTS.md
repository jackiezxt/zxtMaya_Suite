# Repository Guidelines

## Project Structure & Module Organization
Core runtime lives under `core/`, with shared scripts in `core/scripts`, static assets in `core/resources`, and configuration templates in `core/data`. Tool-specific code is pulled in as Git submodules under `tools/<ToolName>`; each submodule owns its Python packages and manifests (see `tools/zxtMaya_Arnold/tool_manifest.yaml`). Suite-level docs sit in `docs/`, while `suite_manifest.json` and `.mod` files describe how the bundle mounts inside Maya.

## Build, Test, and Development Commands
Run validations from the repo root: `python tools/generate_mod.py --validate` checks manifest paths; `python tools/generate_mod.py --maya 2024` regenerates the `.mod` file. Execute core tests with `python -m pytest core/tests`. Submodules should expose their own pytest entry points (e.g., `python -m pytest tests/` inside `tools/zxtMaya_M2Ue`). Use `git submodule update --remote tools/<ToolName>` to pull the latest tool commits into the suite.

## Coding Style & Naming Conventions
Use Python 3.10+ with 4-space indentation. Prefer type hints and `logging` over `print`. Keep tool manifests in YAML (`tool_manifest.yaml`) with lowercase keys and snake_case identifiers. Shared utility modules belong in `core/scripts/core/`; tool-specific logic stays inside each submodule’s `scripts/` tree. Ensure Qt code supports PySide2 fallback before importing PySide6/PyQt5.

## Testing Guidelines
PyTest is the standard framework. Mirror module paths in `core/tests/` and name files `test_<module>.py`; test functions should describe behaviour (e.g., `test_loader_handles_yaml`). Tools are encouraged to provide smoke or unit tests under their `tests/` directory. Before opening a PR, run the suite-level pytest command and the manifest validation script.

## Commit & Pull Request Guidelines
Write commits in imperative mood (e.g., `Update zxtMaya_M2Ue manifest`). When tool submodules change, update the pointer via `git submodule update --remote` and commit the resulting diff. PRs should list affected tools, include command transcripts for `generate_mod.py` and pytest, and describe any Maya UI impact (screenshots or GIFs if relevant).

## Security & Configuration Tips
Do not embed secrets or machine-specific paths. Keep configuration overrides in YAML files that can be templated. Vendored packages belong under `core/scripts/packages/thirdparty/` and must be documented. Windows paths should remain ASCII-friendly to avoid Maya loader issues.
