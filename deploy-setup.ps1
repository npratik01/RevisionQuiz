# PowerShell script to deploy AI Club Quiz to GitHub and hosting platforms
# Run this script to automatically set up Git and prepare for deployment

Write-Host "🚀 AI Club Quiz - Deployment Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Check if Git is installed
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not installed. Please install Git first:" -ForegroundColor Red
    Write-Host "   https://git-scm.com/download/win" -ForegroundColor Yellow
    pause
    exit 1
}

# Initialize Git repository
Write-Host "📁 Initializing Git repository..." -ForegroundColor Blue
git init

# Add all files
Write-Host "📦 Adding files to Git..." -ForegroundColor Blue
git add .

# Create initial commit
Write-Host "💾 Creating initial commit..." -ForegroundColor Blue
git commit -m "Initial commit - AI Club Revision Quiz for global deployment"

Write-Host "" 
Write-Host "✅ Git repository created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Next Steps for Global Deployment:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create GitHub Repository:" -ForegroundColor White
Write-Host "   • Go to https://github.com/new" -ForegroundColor Gray
Write-Host "   • Repository name: ai-club-quiz" -ForegroundColor Gray
Write-Host "   • Make it public" -ForegroundColor Gray
Write-Host "   • Don't initialize with README (we have one)" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Push to GitHub:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOURUSERNAME/ai-club-quiz.git" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Deploy to Render.com (Easiest):" -ForegroundColor White
Write-Host "   • Go to https://render.com" -ForegroundColor Gray
Write-Host "   • Sign up for free" -ForegroundColor Gray
Write-Host "   • New Web Service → Connect GitHub → Select your repo" -ForegroundColor Gray
Write-Host "   • Build Command: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "   • Start Command: gunicorn app:app" -ForegroundColor Gray
Write-Host "   • Deploy!" -ForegroundColor Gray
Write-Host ""
Write-Host "🎓 Your quiz will be live and ready to share with your entire college!" -ForegroundColor Green
Write-Host ""
Write-Host "📖 For detailed deployment guides, see DEPLOYMENT.md" -ForegroundColor Yellow

pause
