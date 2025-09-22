# 环境搭建指南

本文描述如何在本地克隆 `zxtMaya_Suite`、初始化子模块、生成 `.mod` 并在 Maya 中验证加载。

## 1. 克隆仓库
```powershell
git clone <repo-url> d:\git\zxtMaya_Suite
cd d:\git\zxtMaya_Suite
```
若仓库已配置子模块，可直接执行：
```powershell
git submodule update --init --recursive
```

## 2. 添加或更新子模块
- 核心：
  ```powershell
  git submodule add <core-repo-url> core
  ```
- 工具：
  ```powershell
  git submodule add <tool-repo-url> tools/<tool_name>
  ```
- 更新已有子模块：
  ```powershell
  git submodule update --remote core
  git submodule update --remote tools/<tool_name>
  ```
变更完成后记得 `git add .gitmodules core tools/<tool_name>` 并提交。

## 3. 更新 manifest
子模块路径调整后，编辑 `suite_manifest.json`：
```json
{
  "suite_name": "MyMayaSuite",
  "entries": [
    {
      "name": "core",
      "python_paths": ["core/src"],
      "script_paths": ["core/scripts"],
      "icon_paths": ["core/resources/icons"]
    }
  ]
}
```
> 建议仅使用相对路径；生成脚本会自动基于仓库根目录补全绝对路径。

## 4. 生成 `.mod`
```powershell
python tools/generate_mod.py --maya 2024
```
可同时指定多个 Maya 版本（如 `--maya 2024 --maya 2026`）。脚本会对 `modules/<mayaVersion>/MyMayaSuite.mod` 重新写入路径。

## 5. Maya 配置与验证
1. 将 `modules/<mayaVersion>` 目录加入 `MAYA_MODULE_PATH`。
2. 启动对应版本的 Maya：
   ```powershell
   "C:\Program Files\Autodesk\Maya2024\bin\maya.exe"
   ```
3. 检查核心菜单、工具面板是否正常显示。
4. 如未加载，查看 Maya 输出窗口或 `scripts/core/logs`（若有）获取错误信息。

## 6. 常用 Git 命令
```powershell
git status
git pull
git submodule status
git submodule update --remote --merge
```
在提交前请确认所有子模块指向期望的提交哈希，必要时在壳仓库内记录对应 tag。

## 7. 后续规划
- 集成 CI：验证 `generate_mod.py` 是否成功、路径是否存在。
- 发布脚本：打包 `.mod` 与资源，供非 Git 用户安装。
- 文档扩展：在 `docs/` 添加贡献指南与问题排查手册。
