@echo off
echo Starting Django Server...
cd /d "%~dp0"

:: Activate the virtual environment
if exist "venv\Scripts\activate" (
    call venv\Scripts\activate
) else if exist "venv2\Scripts\activate" (
    call venv2\Scripts\activate
) else (
    echo Error: Virtual environment (venv or venv2) not found.
    pause
    exit /b
)

:: Start the server in a new window
echo Launching Django server...
start cmd /k "python manage.py runserver"

:: Wait for server to initialize
echo Waiting for server to start...
timeout /t 5 /nobreak > NUL

:: Open the browser
echo Opening dashboard in browser...
start http://127.0.0.1:8000/

echo Setup complete! You can close this window, but keep the server terminal open.
pause
