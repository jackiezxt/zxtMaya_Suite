# zxtMaya_Suite

本仓库是 zxt Maya 工具集的壳仓库，负责组合核心框架和各独立工具的 Git 子模块，并为 Maya 提供统一的 `.mod` 入口及部署脚本。

## 目录结构
- `modules/<mayaVersion>/`：每个 Maya 版本的模块描述文件，运行生成脚本后会根据 `suite_manifest.json` 自动写入 `PYTHONPATH`、`MAYA_SCRIPT_PATH`、`XBMLANGPATH`。
- `tools/`：辅助脚本目录，包含 `.mod` 自动生成、子模块清单等工具；后续会放置核心与各工具子模块（如 `core/`、`tools/<tool_name>/`）。
- `docs/`：方案和使用文档。
- `suite_manifest.json`：记录需要纳入套件的各子模块及其资源路径，供生成脚本与其他自动化使用。

## 初次克隆
```powershell
git clone <repo-url> d:\git\zxtMaya_Suite
cd d:\git\zxtMaya_Suite
git submodule update --init --recursive
```
> 若仓库中尚未添加子模块，以上命令会跳过；请参考下文添加核心与工具仓库。

## 添加子模块
```powershell
git submodule add <core-repo-url> core
git submodule add <tool-repo-url> tools/<tool_name>
git commit -am "Add core/tool submodule"
```
完成后在 `suite_manifest.json` 中补充对应条目，或运行 `tools/list_modules.ps1` 查看当前登记的模块。

## 生成 `.mod`
```powershell
python tools/generate_mod.py --maya 2024
```
脚本会读取 `suite_manifest.json`，并更新 `modules/maya2024/MyMayaSuite.mod`。请根据需要为其他 Maya 版本执行同样命令。

## Maya 配置
1. 将 `modules/<mayaVersion>` 加入 `MAYA_MODULE_PATH`。
2. 启动 Maya 后验证核心菜单 / 工具是否加载；若有问题，检查 `.mod` 内路径是否指向有效子模块。

## 后续工作
- 将 `zxtMaya_ToolsCore` 与各工具仓库作为子模块引入。
- 根据实际子模块路径调整 `suite_manifest.json`。
- 在 `docs/` 补充 CI、发布和贡献指南。