@echo off
echo Running Habit Tracker Dashboard Generator...
cd /d "C:\Users\nelso\Desktop\Projects\habit-tracker-analyzer"
"C:\Users\nelso\anaconda3\python.exe" scripts\generate_dashboard.py
echo Script completed at %time% on %date%
pause
