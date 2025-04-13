@echo off
set TASK_NAME="ClassItemScript"
set PYTHON_PATH="C:\Python311\pythonw.exe"
set SCRIPT_PATH="D:\your_script.py"

:: 检查管理员权限
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system" || (
    echo 请求管理员权限...
    powershell -Command "Start-Process cmd -ArgumentList '/c %0' -Verb RunAs"
    exit /b
)

:: 创建计划任务
schtasks /create /tn %TASK_NAME% /tr "%PYTHON_PATH% %SCRIPT_PATH%" /sc onlogon /ru SYSTEM /rl HIGHEST /f

echo 计划任务已创建！按任意键退出...
pause >nul