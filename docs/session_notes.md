# 当前工作要点
- `core/scripts/core/config.py` 注入 `thirdparty` 目录扫描，保证随仓库分发的 PyYAML 自动可用。
- `core/scripts/core/pipeline/` 新增 `ConfigManager`/`PathManager`/`AssetManager`，集中解析 `projects/<Project>/template.yaml` 并向旧工具暴露格式化接口。
- `core/data/config/projects/CSProject/` 建立首个项目模板，配套 `active_project.yaml` 指向自身；示例 YAML 只保留模板外的差异（如渲染附加开关），其余默认值由 `template.yaml` 统一注入。
- `docs/dev_env_maya2026.md` 记录 Maya 2026 对应的 Conda 环境搭建流程，与新配置体系同步交付。
- `core/scripts/packages/thirdparty/dayu_widgets_bundle/` 引入 `dayu_widgets` + `qtpy` 以支持 Maya 内部 UI，默认在 `userSetup.py` 中设置 `QT_API=pyside2`。


# 背景信息
- `zxtMaya_Suite` 将 `zxtMaya_ToolsCore` 作为子模块挂载在 `core/`，开发时需先在子模块仓提交，再回主仓记录引用。
- 各 `zxtMaya_*` 工具仍依赖 `core.pipeline` 提供的路径、镜头、任务定义；新模板体系保持这些 import 不变，仅替换数据来源。
- PyYAML 以源码形式放在 `core/scripts/packages/thirdparty/pyyaml`，避免目标环境缺少 `pip` 依赖；未来新增第三方库可复用该机制。
