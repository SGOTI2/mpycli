@echo off
echo run with nwin for best results
:l
taskkill /f /im ClassroomWindows.exe
timeout 1 > NUL
goto l