# CI 配置说明

仓库包含 `.github/workflows/ci.yml`，默认在每次 `push` 到 `main` 分支或任意 PR 时触发。工作流包括：

- **Validate manifest and .mod**：
  - 检出所有子模块。
  - 校验 `suite_manifest.json` 中声明的路径是否存在。
  - 调用 `python tools/generate_mod.py --maya 2024` 重新生成 `.mod` 文件，并确保生成后没有脏差异。
- **Core pytest**：
  - 在 Ubuntu 环境下检出子模块。
  - 安装 Python 3.10 + pytest。
  - 进入 `core/` 子模块运行 `python -m pytest`。

> 注意：GitHub 托管环境没有 Maya，因此该流程使用普通 Python 解释器。若需要用 `mayapy` 验证 UI 或依赖 Maya 的测试，请在自托管 Runner 上新增额外 Job，并在 workflow 中指定 `runs-on: [self-hosted, maya]` 这类标签。

## 本地预检
提交前，可在壳仓库根执行：
```powershell
python tools/generate_mod.py --maya 2024
python -m pip install pytest
pushd core
python -m pytest
popd
```
确保 `.mod` 文件无 diff 且核心单测通过。

## 扩展建议
- 若未来为其它子模块增设测试，可在 workflow 中追加新的 Job，或在 `core-tests` 内再运行 `python -m pytest`（通过 `working-directory` 指定）。
- 需要 `mayapy` 测试时，建议在公司内部配置带 Maya 的 Windows Runner，把 `PYTHON` 指向 `mayapy`。
