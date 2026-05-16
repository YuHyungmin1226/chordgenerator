@echo off
setlocal enabledelayedexpansion
title Chord Progression Generator - Easy Launcher

:: Move to the directory where the batch file is located
cd /d "%~dp0"

:menu
cls
echo =======================================================
echo    🎵 Chord Progression Generator (코드 진행 생성기)
echo =======================================================
echo.
echo  원하시는 실행 모드를 선택해주세요:
echo.
echo    [1] 로컬 웹 애플리케이션 (현대적인 웹 브라우저 기반)
echo    [2] 데스크톱 GUI (기본 tkinter 기반)
echo    [3] MusicXML 편집기 (MusicXML 파일 처리 도구)
echo    [4] 종료
echo.
echo =======================================================
set /p choice="번호를 입력하세요 (기본값: 1): "

if "%choice%"=="" set choice=1
if "%choice%"=="1" goto run_web
if "%choice%"=="2" goto run_gui
if "%choice%"=="3" goto run_editor
if "%choice%"=="4" goto exit
echo [오류] 잘못된 입력입니다. 다시 선택해주세요.
pause
goto menu

:run_web
echo.
echo [WEB] 로컬 웹 앱을 시작합니다...
echo 브라우저에서 http://localhost:5000 을 열어주세요.
python main.py --web
pause
goto menu

:run_gui
echo.
echo [GUI] 데스크톱 GUI를 시작합니다...
python main.py --gui
pause
goto menu

:run_editor
echo.
echo [EDITOR] MusicXML 편집기를 시작합니다...
python main.py --musicxml-editor
pause
goto menu

:exit
echo.
echo 프로그램을 종료합니다. 이용해주셔서 감사합니다!
timeout /t 2 >nul
exit
