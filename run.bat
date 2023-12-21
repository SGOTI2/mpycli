@echo off
where python>nul 2>nul
if %ERRORLEVEL% neq 0 (
    color C
    echo Python was not found, you must install it!
    echo.
    echo To install, open company portal via the start menu.
    echo Next search for python and click it.
    echo Click install.
    echo After its installed you must restart your computer and run this file again.
    echo.
    echo Press any key to exit
    pause > nul
    color 7
    exit 0
)
echo Starting...
start "" python .\app.py