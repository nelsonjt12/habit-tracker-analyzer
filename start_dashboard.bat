@echo off
echo Starting Habit Tracker Dashboard...
echo.
echo This will start the web application to visualize your habit tracking data.
echo The dashboard will be available at http://localhost:5000
echo.
echo Press Ctrl+C to stop the application when you're done viewing your dashboard.
echo.

:: Try different Python paths
SETLOCAL

:: Try standard anaconda paths
IF EXIST %USERPROFILE%\Anaconda3\python.exe (
    echo Using Anaconda Python...
    %USERPROFILE%\Anaconda3\python.exe -m pip install flask
    %USERPROFILE%\Anaconda3\python.exe app.py
    goto :end
)

IF EXIST %USERPROFILE%\miniconda3\python.exe (
    echo Using Miniconda Python...
    %USERPROFILE%\miniconda3\python.exe -m pip install flask
    %USERPROFILE%\miniconda3\python.exe app.py
    goto :end
)

:: Try the standard Program Files path for Anaconda
IF EXIST "C:\ProgramData\Anaconda3\python.exe" (
    echo Using Program Files Anaconda Python...
    "C:\ProgramData\Anaconda3\python.exe" -m pip install flask
    "C:\ProgramData\Anaconda3\python.exe" app.py
    goto :end
)

:: Last resort, try regular python
WHERE python >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    echo Using system Python...
    python -m pip install flask
    python app.py
    goto :end
) ELSE (
    echo Python could not be found on your system.
    echo Please install Python or make sure it's in your PATH.
)

:end
ENDLOCAL
pause
