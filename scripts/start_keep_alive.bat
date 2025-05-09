@echo off
echo Starting Keep-Alive Service for Habit Tracker App...
echo.
echo This will periodically ping your application to prevent it from sleeping on Render.
echo Press Ctrl+C to stop the service.
echo.

REM Use the Anaconda Python path as specified in preferences
C:\Users\nelso\anaconda3\python.exe -m pip install requests
C:\Users\nelso\anaconda3\python.exe scripts\keep_alive.py

pause
