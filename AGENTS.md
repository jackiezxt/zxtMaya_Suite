# Repository Guidelines

## Project Structure & Module Organization
- `core/` hosts the shared runtime, configuration loaders, and tests; `docs/` captures workflow notes and onboarding guides.
- Each Maya tool lives in a Git submodule under `tools/<ToolName>` with its own `scripts/`, `tool_manifest.yaml`, and optional `requirements/` folder.
- Shared libraries and tool bundles are declared in `requirements/packages.yaml`; the resolver copies them to `%APPDATA%\zxtTools\bundle_cache` and publishes roots through `ZXT_MAYA_PACKAGE_ROOTS`.

## Build, Test, and Development Commands
- Activate the suite environment with `conda activate maya_2026`.
- Resolve dependencies via `python tools/setup_env.py --env maya --format text`; the output includes `PYTHONPATH` and `ZXT_MAYA_PACKAGE_ROOTS` assignments suitable for launchers.
- Run the full test suite with `python -m pytest core/tests`; target resolver-only coverage via `python -m pytest core/tests/test_setup_env.py`.
- Launch Maya with pre-configured paths by double-clicking `start_maya_suite.bat`.

## Coding Style & Naming Conventions
- Python uses 4-space indentation, type hints, and `logging` instead of `print`.
- Keep JSON/YAML minimal and snake_case; reference paths relative to the repo root.
- Qt UI helpers should gracefully fall back between PySide2/PySide6/PyQt5 and live under `scripts/packages/<package>`.

## Testing Guidelines
- Mirror package structure when adding tests under `core/tests`, naming files `test_<module>.py`.
- Use lightweight smoke tests to validate menu registration when adding new tool manifests.
- Before opening a PR, run `python -m pytest core/tests` and capture the command/output in the PR description.

## Commit & Pull Request Guidelines
- Write imperative commit titles such as `Add github_release resolver`; explain cross-repo impacts and bundle-cache changes in the body.
- PRs should document scope, executed commands, and any updated docs (`README.md`, `docs/dev_workflow.md`).
- Include repro steps plus screenshots or GIFs when changing menus, manifests, or launcher behavior.

## Environment Resolution & Security
- `tools/setup_env.py` supports `path`, `git`, `github_release`, and generic `zip` descriptors; missing fields raise actionable errors.
- The resolver maps category outputs to environment variables (`PYTHONPATH`, `ZXT_MAYA_PACKAGE_ROOTS`) so launchers can bootstrap Maya without shell scripts.
- The bundle cache stores only shared libraries—never project data or secrets. Track the exact version/tag for any vendored third-party code for auditability.

- Use Chinese in dialog, and in markdown files