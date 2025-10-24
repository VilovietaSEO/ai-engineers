@echo off
REM Schema Visualizer - Automated Installation Script (Windows)
REM Made by Vibe Coders - https://www.skool.com/ai-agent-vibe-engineers

echo.
echo ============================================================
echo      Schema Visualizer - Installation Script
echo      Vibe Coders Community
echo ============================================================
echo.

REM Check if Python is installed
echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.7 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo Python found!
echo.

REM Check if pip is installed
echo Checking for pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip is not installed!
    echo pip usually comes with Python. Try reinstalling Python.
    pause
    exit /b 1
)

echo pip found!
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a minute...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo Try running: pip install --user -r requirements.txt
    pause
    exit /b 1
)

echo Dependencies installed successfully!
echo.

REM Test the installation
echo Testing installation...
python -c "import pyvis" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: pyvis module not found
    echo Try running: pip install --user pyvis
    pause
    exit /b 1
)

echo Installation test passed!
echo.

REM Run example
echo Running example visualization...
echo This will create and open an interactive graph...
echo.
python schema_visualizer.py examples\person_schema.json

echo.
echo ============================================================
echo   Installation Complete!
echo ============================================================
echo.
echo You're ready to visualize schemas!
echo.
echo Try these commands:
echo   python schema_visualizer.py examples\local_business_schema.json
echo   python schema_visualizer.py examples\product_schema.json --theme blue
echo   python schema_visualizer.py examples\article_schema.json --layout hierarchical
echo.
echo For more help, see README.md
echo Join Vibe Coders: https://www.skool.com/ai-agent-vibe-engineers
echo.
pause
