@echo off
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
echo =========================================================
echo       Launching MentorMatch AI Platform...
echo       Tagline: Find the right mentor. Build the right future.
echo =========================================================
python -m streamlit run app.py
pause
