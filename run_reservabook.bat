@echo off
setlocal

title Reservabook - Backend + Open HTML
cd /d "%~dp0"

echo Checking Python and pip...
python --version >nul 2>&1 || (echo Python not found. Install from https://python.org && pause && exit /b 1)
pip --version >nul 2>&1 || (echo pip not found. Ensure Python was installed with pip && pause && exit /b 1)

echo Installing Python dependencies...
pip install -r "BACKEND\requirements.txt" --quiet || (echo Failed to install dependencies && pause && exit /b 1)

echo Starting backend on http://127.0.0.1:5500 ...
start "Reservabook Backend" powershell -NoExit -Command "cd '%CD%\BACKEND'; python reservabook_server.py"

REM Wait a bit for backend
timeout /t 2 /nobreak > nul

set HTML_FILE=%CD%\second.html
if not exist "%HTML_FILE%" (
  echo second.html not found in %CD%.
  echo Place your HTML as 'second.html' in this folder, then re-run.
  goto :eof
)

echo Opening HTML...
start "Reservabook UI" "%HTML_FILE%"

echo Done. Keep the backend window open while using the UI.
pause


