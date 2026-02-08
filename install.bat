@echo off
chcp 65001 >nul
REM pclaude one-click installer

echo ============================================================
echo  pclaude - Claude Prompt Auto-Capture
echo ============================================================
echo.

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.11+
    echo Download: https://python.org/downloads
    pause
    exit /b 1
)
echo [OK] Python installed

echo.
echo Installing pclaude...
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
pip install -e "%SCRIPT_DIR%" -q
if errorlevel 1 (
    echo [ERROR] Installation failed
    pause
    exit /b 1
)
echo [OK] pclaude installed

echo.
echo Setting up alias...
echo # pclaude - Auto-capture Claude prompts>> "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
echo Set-Alias -Name claude -Value "pclaude">> "%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
echo [OK] Alias configured

echo.
echo ============================================================
echo  Installation Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Close this window, open a new PowerShell
echo   2. Run: . $PROFILE
echo   3. Then use: claude "your prompt"
echo.
echo Every 'claude' command will auto-capture your prompts!
echo.
pause
