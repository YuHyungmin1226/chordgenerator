@echo off
setlocal enabledelayedexpansion
title Chord Progression Generator - Web App

:: Move to current directory
cd /d "%~dp0"

echo =======================================================
echo    Starting Chord Progression Generator Web App...
echo =======================================================
echo.
echo Please open http://localhost:5000 in your browser.
echo.
echo Press CTRL+C to stop the server.
echo =======================================================

python main.py

pause
