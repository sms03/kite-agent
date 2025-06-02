@echo off
title Zerodha AI Agent
color 0A

echo.
echo ========================================
echo   ZERODHA AI AGENT - LAUNCHER
echo ========================================
echo.

:menu
echo Choose an option:
echo.
echo 1. Run Interactive Trading Interface
echo 2. Run Feature Demo
echo 3. Run Setup (Install Dependencies)
echo 4. View README
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto interactive
if "%choice%"=="2" goto demo
if "%choice%"=="3" goto setup
if "%choice%"=="4" goto readme
if "%choice%"=="5" goto exit
echo Invalid choice. Please try again.
goto menu

:interactive
echo.
echo Starting Interactive Trading Interface...
echo.
python main.py
echo.
pause
goto menu

:demo
echo.
echo Starting Feature Demo...
echo.
python demo.py
echo.
pause
goto menu

:setup
echo.
echo Running Setup...
echo.
python setup.py
echo.
pause
goto menu

:readme
echo.
echo Opening README.md...
echo.
start README.md
goto menu

:exit
echo.
echo Thank you for using Zerodha AI Agent!
echo.
pause
exit
