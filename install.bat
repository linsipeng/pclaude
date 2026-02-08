@echo off
REM pclaude 一键安装脚本
REM 自动安装 pclaude 并设置 claude alias

echo ============================================================
echo  pclaude - Claude Prompt 自动捕获工具
echo ============================================================
echo.
echo 正在检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.11+
    echo 下载地址: https://python.org/downloads
    pause
    exit /b 1
)
echo [OK] Python 已安装

echo.
echo 正在安装 pclaude...
pip install -e "%~dp0" -q
if errorlevel 1 (
    echo [错误] 安装失败
    pause
    exit /b 1
)
echo [OK] pclaude 已安装

echo.
echo 正在设置 alias...
echo # pclaude - Auto-capture Claude prompts>> "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
echo Set-Alias -Name claude -Value "pclaude">> "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
echo [OK] alias 已设置

echo.
echo ============================================================
echo  安装完成！
echo ============================================================
echo.
echo 下一步：
echo   1. 关闭当前终端，打开新的 PowerShell
echo   2. 运行以下命令激活 alias：
echo.
echo      . $PROFILE
echo.
echo   3. 然后就可以直接使用：
echo.
echo      claude "你的 prompt"
echo.
echo 每次运行 claude，prompt 都会自动保存！
echo.
pause
