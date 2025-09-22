# MyMayaTools 拆分与迁移计划

## 核心能力迁移到 zxtMaya_ToolsCore
- `scripts/userSetup.py`：保留菜单加载、工具入口逻辑，迁移后改为调用核心 `package_manager`。
- `scripts/core/config.py`、`scripts/core/package_manager.py`：作为配置管理和包注册框架，重构为模块化 API（路径解析、日志、异常包装等）。
- `pythonScripts/zxtToolClass.py` 及其他通用函数：筛选出项目无关的基础能力，拆成 `core/utils` 子包并补充单元测试。
- `resources/icons`、`resources/templates`、`data/config`：整理后迁入核心仓库资源层，保持标准 32×32 图标、模板与默认配置。
- 旧 `.mod` 定义只保留模板；壳仓库根据 manifest 自动生成，核心只暴露相对路径结构。

## 工具子模块抽取方向
- `pythonScripts` 内各场景化脚本拆分为主题工具仓库（如 `zxtMat2UE`, `zxtExportABC`, `zxtHud` 等），统一 `scripts/packages/<tool>` + `resources/<tool>` 结构并提供 `show()` 入口。
- `plugins/zxtM2Ue`, `plugins/zxtArnoldCTRL`, `plugins/zxtAntiVirus` 等已有独立目录的工具，直接迁出为 submodule，保留现有 `scripts/ui/utils` 组织。
- 大量 MEL 工具（`craSceneTools.mel`, `zxtPaintNormal.mel` 等）按功能归类，暂存于“Legacy MEL Tools” 仓库，后续视需要重写。
- 第三方/Vendor 插件（AdvancedSkeleton, Red9, studiolibrary 等）集中存放在壳仓库 `plugins/` 子模块，并在 README 标注来源与版本。

## 拆分步骤建议
1. 为旧仓库打 tag 或创建 `MyMayaTools_archive`，只读存档以便回溯历史。
2. 在 `zxtMaya_ToolsCore` 建立 `scripts/core`, `scripts/bootstrap`, `resources`, `data` 骨架，迁入核心文件并逐步模块化。
3. 为每个目标工具创建模板仓库（或复用现有 repo），迁移代码/资源/配置，补齐 `tests/` 与 README。
4. 在 `zxtMaya_Suite` 中增加各子模块引用，更新 `suite_manifest.json`，运行 `tools/generate_mod.py` 重建所有 Maya 版本的 `.mod`。
5. 梳理依赖：确认 `.pyd`、第三方库许可；无用资产留在 archive，中长期计划重写或移除。
6. 配置 CI 与测试：核心仓库运行 `mayapy -m pytest`，工具仓库做功能或 smoke test，壳仓库负责集成验证和 `.mod` 路径检查。

## 注意事项
- 保持相对路径引用，避免在 manifest 或核心代码中硬编码盘符。
- 迁移过程中记录每个工具所需资源（模板、图标、配置）；缺失则在 README 中声明。
- 在新增子模块前先清点 `scripts/` 根目录的零散脚本，确认是否归档或纳入某工具仓库，减少后续维护成本。
- 更新文档同步流程变更：壳仓库 README、各子模块 README、核心仓库贡献指南都需要校对。
