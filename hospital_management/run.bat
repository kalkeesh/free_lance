@echo off

:: Navigate to the 'C:\hospital_management' folder
cd C:\hospital_management

:: Check if the virtual environment exists by checking the Scripts folder
IF NOT EXIST "Scripts" (
    echo Virtual environment not found. Creating one...
    python -m venv .
    :: Sleep for 1 second (using timeout)
    timeout /t 1 /nobreak >nul
) ELSE (
    echo Virtual environment already exists.
)

:: Activate the virtual environment (for Windows)
call Scripts\activate.bat

:: Sleep for 1 second (using timeout)
timeout /t 1 /nobreak >nul

:: Update pip
python -m pip install --upgrade pip

:: Install the required packages
pip install django

:: Check if Django installed successfully
IF ERRORLEVEL 1 (
    echo Django installation failed. Exiting script.
    exit /b 1
)

:: Run the Django server
python manage.py runserver
