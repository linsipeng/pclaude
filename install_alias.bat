@echo off
REM pclaude Alias Installer for Windows
REM
REM This script replaces 'claude' command with pclaude for automatic prompt capture.
REM
REM Usage: Double-click this file or run in CMD/PowerShell

echo ============================================================
echo pclaude Alias Installer
echo ============================================================
echo.
echo This script will replace 'claude' command with pclaude.
echo All prompts will be automatically captured.
echo.
echo Detecting environment...

REM Check if running in CMD or PowerShell
echo Checking PowerShell profile...

set "PROFILE_PATH=%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
set "PROFILE_DIR=%USERPROFILE%\Documents\PowerShell"

if not exist "%PROFILE_DIR%" (
    echo Creating PowerShell profile directory...
    mkdir "%PROFILE_DIR%" 2>nul
)

REM Check if alias already exists
if exist "%PROFILE_PATH%" (
    findstr /C:"Set-Alias -Name claude" "%PROFILE_PATH%" >nul
    if %errorlevel% equ 0 (
        echo Alias already installed in PowerShell profile.
        goto :done
    )
)

REM Add alias to PowerShell profile
echo Adding alias to PowerShell profile...
echo. >> "%PROFILE_PATH%"
echo # pclaude - Automatic prompt capture >> "%PROFILE_PATH%"
echo Set-Alias -Name claude -Value pclaude >> "%PROFILE_PATH%"

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo IMPORTANT: Run this command to activate:
echo.
echo   . $PROFILE
echo.
echo Or restart PowerShell.
echo.
echo After activation, 'claude' command will automatically
echo capture all prompts using pclaude.
echo.

:done
pause
