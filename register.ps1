# 定义参数
$taskName = "ClassItemScript"
$pythonwPath = ""
$scriptPath = "C:\Users\EEO\Documents\课表"

# 检查管理员权限
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# 搜索 Pythonw.exe 的路径
if ($pythonwPath -eq "") {
    $pythonwPath = Get-Command pythonw.exe -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
    if (-not $pythonwPath) {
        Write-Host "未找到 Pythonw.exe，请手动输入路径："
        $pythonwPath = Read-Host "Pythonw.exe 路径"
    }
}

# 将pythonw.exe路径转换为绝对路径
$pythonwPath = [System.IO.Path]::GetFullPath($pythonwPath)


if (-not (Test-Path $pythonwPath)) {
    Write-Host "Pythonw.exe 路径无效，请检查路径。"
    exit
}


#将当前目录设置为脚本所在目录
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Definition)
# 搜索脚本的路径
if ($scriptPath -eq "") {
    $scriptPath = Get-ChildItem -Path . -Filter "manager.py" -Recurse | Select-Object -First 1 -ExpandProperty FullName
    if (-not $scriptPath) {
        Write-Host "未找到脚本，请手动输入路径："
        $scriptPath = Read-Host "脚本路径"
    }
}

# 创建任务配置
$action = New-ScheduledTaskAction -Execute $pythonwPath -Argument $scriptPath
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -Hidden -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

# 注册任务
Register-ScheduledTask -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Force

Write-Host "计划任务创建成功！"