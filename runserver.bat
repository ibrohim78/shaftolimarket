@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  call ".venv\Scripts\python.exe" manage.py runserver
) else (
  call python manage.py runserver
)
