@echo off
title OES LMS - Live Examination System
cd /d "%~dp0"
echo ===================================================
echo   Starting OES LMS Server at http://127.0.0.1:8000/
echo ===================================================
echo Press Ctrl+C in this window to stop the server anytime.
echo.
"..\venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8000
pause
