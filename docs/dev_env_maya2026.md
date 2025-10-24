# Maya 2026 Conda 环境搭建指引

以下步骤以 Windows + Conda 为例，目标是提供一个与 Maya 2026 自带 `mayapy` 兼容的 Python 3.11 环境，方便在命令行运行 suite 的脚本、单元测试或调试 `maya.cmds`。

## 1. 创建环境

```powershell
conda create -n maya_2026 python=3.11
conda activate maya_2026
```

如果团队使用 Miniconda，请将上述命令在 `Anaconda Prompt` 中执行。

## 2. 安装常用依赖

```powershell
conda install pyyaml pytest pip
```

根据需求再补充其它包（如 requests / PySide6 等）。

## 3. 注入 Maya SDK 路径

1. 在环境目录下新建激活脚本：
   - `envs\maya_2026\etc\conda\activate.d\maya_env.ps1`
   - 内容：
     ```powershell
     $mayaRoot = "C:\Program Files\Autodesk\Maya2026"
     $env:MAYA_LOCATION = $mayaRoot
     $env:PATH = "$mayaRoot\bin;$mayaRoot\Python\Scripts;$env:PATH"
     ```

2. 新建反激活脚本：
   - `envs\maya_2026\etc\conda\deactivate.d\maya_env.ps1`
   - 内容：
     ```powershell
     $mayaRoot = "C:\Program Files\Autodesk\Maya2026"
     $env:PATH = ($env:PATH -replace [regex]::Escape("$mayaRoot\bin;"), "")
     $env:PATH = ($env:PATH -replace [regex]::Escape("$mayaRoot\Python\Scripts;"), "")
     Remove-Item Env:MAYA_LOCATION -ErrorAction SilentlyContinue
     ```

3. 在 `envs\maya_2026\Lib\site-packages` 下创建 `maya2026.pth`，写入：
   ```
   C:\Program Files\Autodesk\Maya2026\Python\Lib\site-packages
   C:\Program Files\Autodesk\Maya2026\Python\DLLs
   C:\Program Files\Autodesk\Maya2026\Python
   ```

完成后重新激活：
```powershell
conda deactivate
conda activate maya_2026
```

## 4. 验证

```powershell
python -c "import sys; print('\n'.join(sys.path))"
python -c "import maya.cmds; print('maya.cmds ok')"
```

只要看到 `maya.cmds ok`，说明环境已正确加载 Maya 的 Python API。

## 5. 共享环境

```powershell
conda env export > maya_2026.yaml
```

团队成员可用 `conda env create -f maya_2026.yaml` 复刻环境。

---

若 Maya 安装路径不同（比如安装在 D 盘），记得把脚本中的路径替换成实际位置。
