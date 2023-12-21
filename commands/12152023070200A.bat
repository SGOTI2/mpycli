@echo off
python.exe app.py
taskkill /f /im python.exe > nul 2> nul