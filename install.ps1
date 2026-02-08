# pclaude 一键安装脚本
# 自动安装 pclaude 并设置 claude alias

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  pclaude - Claude Prompt 自动捕获工具" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python 已安装 ($pythonVersion)" -ForegroundColor Green
} catch {
    Write-Host "[错误] 未找到 Python，请先安装 Python 3.11+" -ForegroundColor Red
    Write-Host "下载地址: https://python.org/downloads" -ForegroundColor Yellow
    exit 1
}

# 安装 pclaude
Write-Host ""
Write-Host "正在安装 pclaude..." -ForegroundColor Yellow
pip install -e "$PSScriptRoot" -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "[错误] 安装失败" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] pclaude 已安装" -ForegroundColor Green

# 设置 alias
Write-Host ""
Write-Host "正在设置 alias..." -ForegroundColor Yellow

$profilePath = "$HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
$profileDir = Split-Path $profilePath -Parent

if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

$aliasContent = @"
# pclaude - Auto-capture Claude prompts
Set-Alias -Name claude -Value "pclaude"
"@

if (Test-Path $profilePath) {
    $existing = Get-Content $profilePath -Raw
    if ($existing -match "Set-Alias.*claude.*pclaude") {
        Write-Host "[OK] Alias 已存在" -ForegroundColor Green
    } else {
        Add-Content -Path $profilePath -Value $aliasContent -Encoding UTF8
        Write-Host "[OK] Alias 已添加" -ForegroundColor Green
    }
} else {
    Set-Content -Path $profilePath -Value $aliasContent -Encoding UTF8
    Write-Host "[OK] Alias 已添加" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  安装完成！" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步：" -ForegroundColor White
Write-Host "  1. 运行以下命令激活 alias：" -ForegroundColor Yellow
Write-Host ""
Write-Host "     . \$PROFILE" -ForegroundColor Cyan
Write-Host ""
Write-Host "  2. 然后就可以直接使用：" -ForegroundColor Yellow
Write-Host ""
Write-Host "     claude \"你的 prompt\"" -ForegroundColor Cyan
Write-Host ""
Write-Host "每次运行 claude，prompt 都会自动保存！" -ForegroundColor Gray
