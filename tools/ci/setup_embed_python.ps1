# 嵌入式Python安装脚本

# 基本变量
$PythonVersion = "3.12.9"
$Architecture = "amd64" # 可选 "win32"
$DestDir = "install/python"
$ScriptsDir = "tools/ci"  # 存放准备好的文件的目录

# 创建目标目录
if (-not (Test-Path $DestDir)) {
    New-Item -ItemType Directory -Path $DestDir | Out-Null
}
Write-Host "create directory: $DestDir" -ForegroundColor Cyan

# 检查Python是否已经存在
$PythonExePath = Join-Path $DestDir "python.exe"
if (Test-Path $PythonExePath) {
    Write-Host "Python already exitst in $DestDir, skip install." -ForegroundColor Yellow
} else {
    # 下载Python嵌入式包
    $PythonUrl = "https://www.python.org/ftp/python/$PythonVersion/python-$PythonVersion-embed-$Architecture.zip"
    $PythonZip = "python-embedded.zip"
    Write-Host "download Python: $PythonUrl" -ForegroundColor Cyan
    Invoke-WebRequest -Uri $PythonUrl -OutFile $PythonZip

    # 解压Python
    Write-Host "extract Python to: $DestDir" -ForegroundColor Cyan
    Expand-Archive -Path $PythonZip -DestinationPath $DestDir -Force
    Remove-Item $PythonZip
}

# 修改_pth文件
$PthFile = Get-ChildItem -Path $DestDir -Filter "python*._pth" | Select-Object -First 1
if (-not $PthFile) {
    Write-Host "error: don't find _pth file" -ForegroundColor Red
    exit 1
}

Write-Host "modify _pth file: $($PthFile.FullName)" -ForegroundColor Cyan
$PthContent = Get-Content $PthFile.FullName -Raw
$PthContent = $PthContent -replace '#\s*import\s+site', 'import site'

# 添加搜索路径
$RequiredPaths = @(".", ".\Lib", ".\Lib\site-packages", ".\DLLs")
foreach ($Path in $RequiredPaths) {
    if ($PthContent -notmatch [regex]::Escape($Path)) {
        $PthContent += "`r`n$Path"
    }
}

# 写入_pth文件
Set-Content -Path $PthFile.FullName -Value $PthContent -NoNewline

# 复制准备好的文件
Write-Host "copy scripts..." -ForegroundColor Cyan

# 复制setup_pip.py
$SetupPipSource = Join-Path $ScriptsDir "setup_pip.py"
$SetupPipDest = Join-Path $DestDir "setup_pip.py"
if (Test-Path $SetupPipSource) {
    Copy-Item -Path $SetupPipSource -Destination $SetupPipDest -Force
} else {
    Write-Host "error: don't find $SetupPipSource" -ForegroundColor Red
    exit 1
}

# 运行pip安装脚本
Write-Host "run setup_pip.py..." -ForegroundColor Green
$CurrentLocation = Get-Location
Set-Location $DestDir
$PythonExe = Join-Path (Get-Location) "python.exe"

# 检查pip是否已经安装
$PipInstalled = $false
try {
    $PipCheckOutput = & $PythonExe -m pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "pip already installed, edition: $PipCheckOutput" -ForegroundColor Yellow
        $PipInstalled = $true
    }
} catch {
    # 如果出错，则认为pip未安装
    $PipInstalled = $false
}

try {
    if (-not $PipInstalled) {
        Write-Host "install pip..." -ForegroundColor Cyan
        & $PythonExe setup_pip.py
        Write-Host "pip installed" -ForegroundColor Green
    }
    Write-Host "install finished" -ForegroundColor Green
} catch {
    Write-Host "install failed: $_" -ForegroundColor Red
} finally {
    Set-Location $CurrentLocation
}

Write-Host "all done" -ForegroundColor Green