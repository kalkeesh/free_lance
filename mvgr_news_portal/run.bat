@echo off

:: Navigate to the 'C:\naidu' folder
cd C:\mvgr_news_portal

:: Check if virtual environment exists by checking the Scripts folder
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

:: Install the required packages
pip install fastapi python-multipart

python.exe -m pip install --upgrade pip

pip install uvicorn
:: Start the FastAPI application using Uvicorn
python -m uvicorn main:app --reload