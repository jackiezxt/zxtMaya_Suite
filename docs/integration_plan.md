# 工具仓库整合规划


### 当前进度

- [x] zxtMaya_ConvertShader：已拆分并接入套件
- [x] zxtMaya_AntiVirus：已拆分并接入套件
- [x] zxtMaya_Alembic：已拆分并接入套件
- [x] zxtMaya_Validate：已拆分并接入套件

## 核心 (`zxtMaya_ToolsCore`)
- 吸收 `proj_cs_tools/maya_tools/common` 中的配置、路径、Maya utils，拆分为 `core/config`, `core/utils/maya`, `core/pipeline/asset_manager` 并补充单测。
- 从 `vertpipe_maya/pythonScripts/zxtToolCommon.py` 提取仍通用的几何/场景操作，与现有核心工具整理合并。
- 完成后统一提供 `PackageManager`、`MenuBuilder`、日志等基础能力，供各工具子模块调用。

## 工具子模块
- 将 `proj_cs_tools/maya_tools` 下的功能拆成独立 `zxtMaya_*` 仓库：
  - `alembic_exporter`
  - `alembic_mtl`
  - `alembic_renderSetup`
  - `model_check`
  - `scene_clean`
  - `uv_check`
  - `lookdev_transfer`
  - `validate`
  - `zxtAntiVirus`
- `vertpipe_maya/plugins` 中未覆盖的工具（`instanceAlongCurve`, `zxtConvertShaders`, `zxtModClean`, `zxtRenderSetting` 等）同样拆分为独立仓库。
- 与 `zxtMaya_M2Ue` 功能重复的部分（`zxtMaya2Ue`, `zxtM2UeXgen`）择优合并进现有仓库，其余归档。
- 每个仓库按统一结构组织：`scripts/packages/<tool>` + `resources/<tool>` + `tests` + README。

## 壳仓库 (`zxtMaya_Suite`)
- manifest 只写相对路径，通过脚本生成 `.mod`；迁移完成后移除旧式 `vertpipe_maya` `.mod`。
- 新增工具子模块时更新 manifest、重建 `.mod`；CI 维持 manifest 校验 + 核心 pytest，视需求为关键工具添加 smoke test。

## 启动与清理
- 待核心能力稳定后，设计新的统一 `userSetup.py`（在核心仓库），负责执行抗病毒检查、加载 `PackageManager`、构建菜单。
- 逐步移除各旧仓库内零散的启动脚本，将启动逻辑集中管理。
- 完成迁移的旧仓库（如 `vertpipe_maya`）打标签后归档，保留回溯能力。

## 推荐推进顺序
1. 整合核心依赖：先迁 `common` 和 `zxtToolCommon` 的通用代码，确保核心 API 完整。
2. 拆出优先级最高的工具仓库（建议从 `alembic_exporter`, `scene_clean`, `model_check` 开始）。
3. 合并 M2Ue 相关工具，避免重复实现。
4. 调整启动脚本，切换至新的核心加载流程。
5. 更新文档和 CI，确保每个新仓库、壳仓库以及核心都有明确的测试/发布流程。

用这份记录可以在连接中断后快速继续对应的迁移步骤。

## 目标工具仓库映射
- `zxtMaya_Alembic`：合并 `alembic_exporter`, `alembic_mtl`, `alembic_renderSetup`, `lookdev_transfer`。
- `zxtMaya_Validate`：合并 `model_check`, `scene_clean`, `uv_check`, `validate`。
- `zxtMaya_AntiVirus`：迁移 `zxtAntiVirus`。
- `zxtMaya_ConvertShader`：迁移 `vertpipe_maya/plugins/zxtConvertShaders`。
- `zxtMaya_M2Ue`：整合 `vertpipe_maya/plugins/zxtMaya2Ue`、`zxtM2UeXgen`。
- `zxtMaya_Arnold`：迁移 `MyMayaTools/plugins/zxtArnoldCTRL`。
- 其余旧插件（`instanceAlongCurve`, `zxtModClean`, `zxtRenderSetting`, `zxtScnClear`）暂归档，后续视需要重写。
