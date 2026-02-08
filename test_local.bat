@echo off
REM Local test script for pclaude

REM Set mock claude path
set CLAUDE_PATH=%~dp0mock_claude.py
echo CLAUDE_PATH: %CLAUDE_PATH%

REM Clean up old test data
del "%USERPROFILE%\.prompt-archive\prompts.jsonl" 2>nul
echo Cleaned old data
echo.

REM Step 1: Run a prompt
echo ============================================
echo Step 1: Running prompt through pclaude
echo ============================================
python "%CLAUDE_PATH%" test prompt 2>nul || (
    echo Note: Expected error - no real claude installed
)
echo.
echo Running: pclaude "Write a Python function to calculate Fibonacci"
pclaude "Write a Python function to calculate Fibonacci"
echo.

REM Step 2: List prompts
echo ============================================
echo Step 2: List prompts
echo ============================================
pclaude ls
echo.

REM Step 3: Search
echo ============================================
echo Step 3: Search for 'Fibonacci'
echo ============================================
pclaude search Fibonacci
echo.

REM Step 4: Show
echo ============================================
echo Step 4: Show prompt #1
echo ============================================
pclaude show 1
echo.

REM Step 5: Run another prompt
echo ============================================
echo Step 5: Run second prompt
echo ============================================
pclaude "Analyze my FBA ad spend data"
echo.

REM Step 6: List again
echo ============================================
echo Step 6: List again (should show 2 prompts)
echo ============================================
pclaude ls
echo.

echo ============================================
echo Test complete!
echo ============================================
