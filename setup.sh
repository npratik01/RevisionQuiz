#!/bin/bash
# Quick setup script for AI Club Quiz

echo "🚀 Setting up AI Club Revision Quiz..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate || .venv\Scripts\activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "🗄️ Initializing database..."
python -c "from app import init_db; init_db(); print('Database initialized!')"

echo "✅ Setup complete!"
echo ""
echo "🌟 To run the quiz locally:"
echo "   python app.py"
echo ""
echo "🌐 To deploy online, check DEPLOYMENT.md for detailed instructions"
echo ""
echo "🎓 Your AI Club Quiz is ready!"
