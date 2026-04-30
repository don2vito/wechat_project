@echo off
chcp 65001 >nul
title DataQuery Pro - Data Query & Analysis System

echo ========================================
echo    DataQuery Pro - Query & Analysis
echo ========================================
echo.

echo [1/3] Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8+ first.
    pause
    exit /b 1
)
echo Python environment OK

echo.
echo [2/3] Installing dependencies...
cd /d "%~dp0backend"
pip install -r requirements.txt -q
if errorlevel 1 (
    echo Warning: Dependencies installation may be incomplete, trying to continue...
)

echo.
echo [3/3] Starting service...
echo.
echo ========================================
echo    Service is starting...
echo    Frontend: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press Ctrl+C to stop the service
echo.

start http://localhost:8000
python app.py

pause