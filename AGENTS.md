# 仓库指南

## 项目结构与模块组织
`core/` 存放共享运行时（脚本、资源、配置与测试）。工具仓以 Git 子模块形式位于 `tools/<ToolName>`，各自维护 `scripts/` 目录与 `tool_manifest.yaml`。方案文档集中在 `docs/`。`suite_manifest.json` 与生成后的 `modules/<mayaVersion>/*.mod` 描述 Maya 中的挂载方式。共享 UI 组件由 `requirements/packages.yaml` 注册（如 `zxtUI_Library`）。

## 构建、测试与开发命令
在仓库根目录执行：`python tools/generate_mod.py --validate` 校验 manifest 路径；`python tools/generate_mod.py --maya 2024` 重新生成 `.mod`。核心测试使用 `python -m pytest core/tests`。更新某个子模块时运行 `git submodule update --remote tools/<ToolName>`，随后 `git add tools/<ToolName>`。本地调试可直接使用 `start_maya_suite.bat` 预配置 Maya 启动环境。

## 编码风格与命名约定
采用 Python 3.10+、4 空格缩进，使用类型注解和 `logging`（避免 `print`）。工具 manifest 统一使用 YAML（`tool_manifest.yaml`），键名小写、标识符采用 snake_case。共享辅助代码放在 `core/scripts/core/`，工具相关逻辑留在子模块内部。Qt 代码需兼容 PySide2、PySide6 与 PyQt5 的回退。

## 测试指引
默认使用 PyTest。`core/tests/` 中按源码结构组织测试（文件 `test_<module>.py`，函数命名体现行为）。鼓励每个工具子模块维护独立 `tests/` 目录，用于 smoke/unit 覆盖。提交 PR 前务必运行 manifest 校验与 `python -m pytest core/tests`，并在必要时附上工具级测试命令。

## 提交与 PR 规范
提交信息使用祈使句（如 `Switch UI library to zxtUI_Library`）。更新子模块时说明受影响工具，并附上 `generate_mod.py`、pytest 输出。PR 描述需列出改动工具、manifest 调整，并在涉及 Maya 菜单改动时附截图或 GIF。合并前须通过 CI（`suite-checks`、`core-tests`）。

## 安全与配置提示
勿提交密码或机器专用路径。共享依赖写在 `requirements/packages.yaml`，解析后放入 `bundle_cache`。若需纳入第三方库，请放在 `core/scripts/packages/thirdparty/` 并标注文档。Windows 路径保持 ASCII，以避免 Maya 加载异常。
