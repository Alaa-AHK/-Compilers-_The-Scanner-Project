@echo off
REM ===================================================================================
REM SCRIPT: build_exe.bat
REM ASSIGNED TO: Subteam 3 (Integration, QA & Build - 1 Member)
REM ===================================================================================
REM [OBJECTIVE]
REM Automate compiling the project into a standalone Windows .exe (Deliverable #1).
REM Runs on any Windows machine without requiring Python or third-party tools.
REM
REM How to run:
REM   Double-click build_exe.bat OR execute `.\build_exe.bat`
REM ===================================================================================

echo [1/3] Checking PyInstaller installation...
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing pyinstaller...
    python -m pip install pyinstaller
)

echo [2/3] Building standalone Windows executable (TinyScanner.exe)...
python -m PyInstaller --noconfirm --onedir --windowed --name "TinyScanner" main.py

echo [3/3] Build finished!
echo Executable is located at: dist\TinyScanner\TinyScanner.exe
pause
