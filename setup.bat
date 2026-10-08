@echo off
echo =========================================================
echo       MentorMatch AI - Hackathon Environment Setup
echo =========================================================
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Setup completed! You can now launch the app with run.bat.
pause
