@echo off
chcp 65001 >nul
echo ========================================
echo   就业指导助手 - Web界面启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Python，请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] 检查Python环境...
python --version
echo.

REM 检查虚拟环境
if not exist "venv" (
    echo [2/3] 创建虚拟环境...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [错误] 虚拟环境激活失败
    pause
    exit /b 1
)
echo.

REM 安装依赖
echo [2/3] 检查并安装依赖...
echo 正在安装必要的Python包，请稍候...
pip install --upgrade pip >nul 2>&1
pip install fastapi uvicorn >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)
echo 依赖安装完成
echo.

REM 启动Web服务
echo [3/3] 启动Web服务...
echo.
echo ========================================
echo   Web服务正在启动...
echo   访问地址: http://localhost:8000
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

cd src
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
