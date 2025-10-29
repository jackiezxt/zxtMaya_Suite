# 开发流程指南

本指南概述在 `zxtMaya_Suite` 主仓与各工具子仓之间协作开发的推荐流程，并解释共享依赖解析器与 bundle cache 的使用方式。

## 准备工作
- 克隆主仓：`git clone git@github.com:jackiezxt/zxtMaya_Suite.git`
- 初始化子模块：`git submodule update --init --recursive`
- 激活 Maya Python 环境：`conda activate maya_2026`
- 解析共享依赖（首次或依赖更新后执行）：`python tools/setup_env.py --env maya --format text`，输出中同时写入 `PYTHONPATH` 与 `ZXT_MAYA_PACKAGE_ROOTS`
- 本地启动 Maya：双击 `start_maya_suite.bat`，脚本会调用解析器并配置 `PYTHONPATH`/`MAYA_MODULE_PATH`/`ZXT_MAYA_PACKAGE_ROOTS`

## 解析共享依赖与 bundle cache
- `requirements/packages.yaml` 采用 ShotGrid 风格描述符，按类别声明可复用资源：
  - `python`：共享库（如 `zxtUI_Library`）
  - `tool_roots`：工具代码根目录，会同步写入 `ZXT_MAYA_PACKAGE_ROOTS`
- 支持的 `location.type`：`path`、`git`、`github_release`、`zip`
- 解析结果默认缓存到 `%APPDATA%\zxtTools\bundle_cache`，缓存目录名由 `cache_id` 或 “包名+版本” 组成
- `setup_env.py` 提供 `text`/`bat`/`shell`/`json` 等输出格式，便于 launcher/CI 直接消费；若配置缺失字段，会抛出明确错误

## 工具子仓开发流程
1. 准备工作副本：
   - 在 `tools/<ToolName>` 子模块中直接开发，或
   - 使用 `git worktree` / 单独 clone 工具仓库，保持与主仓指针同步
2. 编写/修改代码与 `tool_manifest.yaml`，必要时更新工具自带 `requirements/`
3. 启动 Maya 后通过脚本编辑器热重载：
   ```python
   import importlib, zxtMaya_M2Ue
   importlib.reload(zxtMaya_M2Ue)
   zxtMaya_M2Ue.show()
   ```
4. 在工具仓运行自有测试或手动验证 UI 行为；提交并 push 新的 commit

## 回到主仓同步改动
1. 更新子模块指针：`git submodule update --remote tools/<ToolName>`
2. 将变更加入暂存：`git add tools/<ToolName>`
3. 重新生成 `.mod` 并校验 manifest：
   ```powershell
   python tools/generate_mod.py --validate
   python tools/generate_mod.py --maya 2024
   ```
4. 运行核心测试：`python -m pytest core/tests`
5. 若 `requirements/packages.yaml` 有更新，记得重新执行 `setup_env.py`

## 调试与菜单重建
- 如需刷新菜单/工具架，可在 Maya 中执行：
  ```python
  from core.menu_builder import MenuBuilder
  from core.package_manager import PackageManager
  from core.config import Config
  MenuBuilder().rebuild(PackageManager(Config.get()))
  ```
- `setup_env.py` 写入的 `ZXT_MAYA_PACKAGE_ROOTS` 会被 `core.config.Config` 读取，确保 bundle cache 中的工具也能被自动加载

## CI、提交与 PR
- 提交信息使用祈使句，例如 `Add github_release resolver`
- PR 描述需包含：改动范围、执行的命令（解析器、`generate_mod.py`、pytest 等）、更新的文档或启动脚本
- 主仓 CI 会运行 manifest 校验与 `python -m pytest core/tests`；工具仓可按需配置各自的 pytest/lint
- 涉及菜单或 UI 变更时，建议附上关键截图 / 录屏，便于审查

## 常见问题排查
- **ModuleNotFoundError**：确认 `tool_manifest.yaml` 中的 `scripts` 目录已被 resolver 写入 `PYTHONPATH`，并检查 `ZXT_MAYA_PACKAGE_ROOTS`
- **PySide 相关错误**：确保工具兼容 PySide2/PySide6，并核对 Maya 自带 Qt 版本
- **bundle cache 冲突**：删除 `%APPDATA%\zxtTools\bundle_cache/<包名>` 后重新执行 `python tools/setup_env.py --env maya`