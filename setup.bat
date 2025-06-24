@echo off
REM Quick setup script for AI Club Quiz - Windows

echo 🚀 Setting up AI Club Revision Quiz...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Initialize database
echo 🗄️ Initializing database...
python -c "from app import init_db; init_db(); print('Database initialized!')"

echo ✅ Setup complete!
echo.
echo 🌟 To run the quiz locally:
echo    python app.py
echo.
echo 🌐 To deploy online, check DEPLOYMENT.md for detailed instructions
echo.
echo 🎓 Your AI Club Quiz is ready!
pause
