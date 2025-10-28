@echo off
setlocal

rem Launch Maya 2026 with zxtMaya_Suite modules
set "REPO_ROOT=%~dp0"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

rem Activate Maya 2026 conda environment (adjust paths if your setup differs)
set "CONDA_ENV=C:\Users\86186\.conda\envs\maya_2026"
set "PATH=%CONDA_ENV%;%CONDA_ENV%\Scripts;%PATH%"
set "CONDA_DEFAULT_ENV=maya_2026"
set "CONDA_PREFIX=%CONDA_ENV%"
set "QT_API=pyside2"

echo Maya 2026 environment activated from %CONDA_ENV%

rem Configure suite paths for Maya
set "MAYA_MODULE_PATH=%REPO_ROOT%;%MAYA_MODULE_PATH%"
set "PYTHONPATH=%REPO_ROOT%\core\scripts;%PYTHONPATH%"
echo Using repository root: %REPO_ROOT%

echo Launching Maya...
start "" "C:\Program Files\Autodesk\Maya2026\bin\maya.exe"

endlocal
