@echo off
setlocal enabledelayedexpansion
title Chord Progression Generator - Easy Launcher

:: Move to current directory
cd /d "%~dp0"

:menu
cls
echo =======================================================
echo    Chord Progression Generator
echo =======================================================
echo.
echo  Please select an execution mode:
echo.
echo    [1] Local Web Application (Recommended)
echo    [2] Desktop GUI (tkinter)
echo    [3] MusicXML Editor
echo    [4] Exit
echo.
echo =======================================================
set /p choice="Enter number (1-4, Default: 1): "

if "%choice%"=="" set choice=1
if "%choice%"=="1" goto run_web
if "%choice%"=="2" goto run_gui
if "%choice%"=="3" goto run_editor
if "%choice%"=="4" goto exit
echo [Error] Invalid input.
pause
goto menu

:run_web
echo.
echo [WEB] Starting Local Web App...
echo Please open http://localhost:5000 in your browser.
python main.py --web
pause
goto menu

:run_gui
echo.
echo [GUI] Starting Desktop GUI...
python main.py --gui
pause
goto menu

:run_editor
echo.
echo [EDITOR] Starting MusicXML Editor...
python main.py --musicxml-editor
pause
goto menu

:exit
echo Exiting...
timeout /t 2 >nul
exit
