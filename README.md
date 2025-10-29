# zxtMaya_Suite

Main wrapper repository for the zxt Maya tool suite. It aggregates the shared core runtime plus individual tool repositories (via Git submodules), generates Maya `.mod` entries, and packages everything into a coherent menu/shelf experience.

## Repository Layout
- `core/` – shared runtime, manifest loader, and startup scripts. Tests live in `core/tests`.
- `tools/<ToolName>/` – Git submodules pointing to individual tool repos (e.g., `tools/zxtMaya_Arnold`). Each tool maintains its own `scripts/`, resources, and `tool_manifest.yaml`.
- `docs/` – contributor guides (`dev_workflow.md`, `suite_architecture_plan.md`, etc.).
- `modules/<mayaVersion>/` – generated Maya module descriptors; `tools/generate_mod.py` keeps them in sync with the manifest.
- `suite_manifest.json` – top-level list of components (core + tools) used when producing `.mod` files.

## Getting Started
```powershell
git clone https://github.com/jackiezxt/zxtMaya_Suite.git
cd zxtMaya_Suite
git submodule update --init --recursive
```
To update a specific tool:
```powershell
git submodule update --remote tools/zxtMaya_Arnold
```
Then resolve shared packages and regenerate manifests/tests:
```powershell
python tools/setup_env.py --env maya --format text
python tools/generate_mod.py --validate
python tools/generate_mod.py --validate
python tools/generate_mod.py --maya 2024
python -m pytest core/tests
```

## `tool_manifest.yaml`
Each tool exposes menu/shelf metadata through `tool_manifest.yaml`:
```yaml
tool:
  name: zxtMaya_Arnold
  entry_point: "from zxt_arnold import show; show()"
menus:
  - menu: zxtMaya
    category: Rendering
    items:
      - label: Arnold AOV Setup
        command: "from zxt_arnold import show; show()"
        source: python
```
During startup `core/scripts/userSetup.py` loads every manifest, prepends the relevant `scripts/` folders to `sys.path`, and registers menus/shelves automatically.

## Launching Maya Locally
Use the helper script to bootstrap environment variables and launch Maya 2026:
```bat
start_maya_suite.bat
```

## Contribution Workflow (summary)
1. Develop inside the tool’s submodule (`tools/<ToolName>`), add tests, and push to its repository.
2. In `zxtMaya_Suite`, run `git submodule update --remote tools/<ToolName>` and `git add tools/<ToolName>` to bump the pointer.
3. Regenerate `.mod`, run `python -m pytest core/tests`, and commit.
4. Open a PR describing affected tools and the commands you executed. CI will re-run manifest validation and pytest.

For detailed instructions, see `docs/dev_workflow.md` and `docs/ci.md`.
