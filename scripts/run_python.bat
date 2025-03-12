@echo off
chcp 65001 > nul
SET SCRIPT_DIR=%~dp0
SET PATH=%SCRIPT_DIR%;%SCRIPT_DIR%\Scripts;%PATH%
SET PYTHONPATH=%SCRIPT_DIR%\Lib;%SCRIPT_DIR%\Lib\site-packages;%SCRIPT_DIR%;%PYTHONPATH%

if "%1"=="" (
    python.exe
) else (
    python.exe %*
)