# 开发流程指南

本指南说明如何在独立工具仓和 `zxtMaya_Suite` 主仓之间协作，保持菜单/manifest 的自动化工作。

## 环境准备
- 克隆主仓：`git clone git@github.com:jackiezxt/zxtMaya_Suite.git`。
- 初始化子模块：`git submodule update --init --recursive`。
- Maya 调试可直接运行 `start_maya_suite.bat`，自动设置 `PYTHONPATH`、`MAYA_MODULE_PATH`。

## 开发单个工具
1. 在子模块目录直接工作，例如 `tools/zxtMaya_M2Ue`（此目录本身就是独立仓库）。
2. 修改代码、更新 `tool_manifest.yaml`（菜单/架子命令、`source`、依赖等）。
3. 在 Maya 中调试：
   ```python
   import importlib, zxtMaya_M2Ue
   importlib.reload(zxtMaya_M2Ue)
   zxtMaya_M2Ue.show()
   ```
4. 跑工具仓自己的测试（可以在仓库添加 pytest/flake8 等 CI）。
5. 提交并推送：`git commit` → `git push`。

> 若想在其它路径开发，可使用 `git worktree` 或单独 clone，但最终需要把改动同步回 `tools/<ToolName>`，以便 Maya 加载最新代码。

## 同步到主仓
1. 在主仓根目录拉最新：`git pull`。
2. 更新子模块指针（可封装脚本）：
   ```bash
   git submodule update --remote tools/zxtMaya_M2Ue
   git add tools/zxtMaya_M2Ue
   ```
3. 运行校验脚本：
   ```bash
   python tools/generate_mod.py --validate
   python tools/generate_mod.py --maya 2024
   ```
4. 跑核心测试：`python -m pytest core/tests`。
5. 提交并推送主仓：`git commit -m "Update zxtMaya_M2Ue"` → `git push`。
6. 创建 PR，等待 CI（manifest 校验 + core pytest）通过后合并。

## 菜单与 manifest 约定
- 每个工具需要 `tool_manifest.yaml`，字段包括 `tool`、`menus`、`shelves`、`dependencies`。
- 菜单层级来自 `menus[].menu` → `menus[].category` → `menus[].items[]`。
- 命令使用纯 Python 代码，`source: python`；如需 MEL，可设置 `source: mel`。
- `userSetup.py` 会自动把工具目录和 `scripts/`、`scripts/packages` 加入 `sys.path`，无需额外设置。

## 运行 / 调试流程
1. 双击 `start_maya_suite.bat` 启动 Maya，菜单名默认 `zxtMaya Tools`。
2. 修改工具代码后，可在 Maya Script Editor 中使用 `MenuBuilder` 重新生成菜单：
   ```python
   from core.menu_builder import MenuBuilder
   from core.package_manager import PackageManager
   from core.config import Config
   MenuBuilder().rebuild(PackageManager(Config.get()))
   ```

## CI 约定
- 主仓 CI（`.github/workflows/ci.yml`）会执行 manifest 校验、生成 `.mod`、跑 `core/tests`。
- 工具仓可根据需要自行配置 CI（pytest、lint、manifest schema 校验等），推送后再更新主仓指针。

## 常见问题
- **菜单点击报 `ModuleNotFoundError`**：确认 `tool_manifest.yaml` 中命令引用的模块位于工具目录下，并检查 `userSetup.py` 是否已加载最新路径。
- **Qt 版本不兼容**：编写 Qt 代码时按顺序尝试 PySide2 → PySide6 → PyQt5，确保 fallback 分支导入 Maya API（`OpenMayaUI` 等）。
- **子模块指针未更新**：推完工具仓后记得运行 `git submodule update --remote tools/<ToolName>` 并在主仓提交。

## 清理建议
- 可删除 `core/.pytest_cache/`、`core/zxtMaya_ToolsCore.code-workspace` 等编辑器缓存文件，避免污染仓库。

