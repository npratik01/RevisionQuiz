# 🎓 AI Club Revision Quiz

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

> **🚀 One-Click Deploy:** Click the button above to deploy instantly to Render!

A comprehensive web-based quiz system for testing knowledge in Mathematics, Python Programming, and Python Libraries.

## ✨ Features

- 🎯 **50 Professional Questions** across 3 sections
- 💻 **Code Analysis Questions** for Python sections
- 📱 **Mobile-Responsive Design**
- ⚡ **Instant Results & Analytics**
- 🗄️ **Automatic Data Storage**
- 🎨 **Professional Interface**

### 📚 Topics Covered

#### Mathematics Section:

1. Introduction to Probability
2. Discrete Random Variables
3. Continuous Random Variables
4. Joint Probability Distribution
5. Binomial Distribution
6. Bernoulli Trials
7. Poisson Distribution
8. Mean and Variance
9. Normal Distribution
10. Bivariate Normal Distribution

#### Python Programming Section:

- Data types and structures
- Functions and classes
- Control flow
- Error handling
- Modules and imports
- Object-oriented programming concepts

#### Python Libraries Section:

- **NumPy**: Array operations, mathematical functions
- **Pandas**: DataFrames, data manipulation
- **Matplotlib**: Plotting and visualization
- **Seaborn**: Statistical plots and styling

## 🛠️ Technical Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with gradients and animations
- **Responsive**: Mobile-friendly design

## 🚀 Quick Deployment (Free Hosting)

Deploy your quiz globally in minutes! Choose from these free hosting options:

### 🌟 **Render.com** (Recommended - Zero Configuration)

1. Fork/upload this repository to GitHub
2. Visit [render.com](https://render.com) and sign up
3. Create "New Web Service" → Connect GitHub → Select this repo
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `gunicorn app:app`
6. Deploy! Your quiz will be live at `https://your-app-name.onrender.com`

### ⚡ **Other Great Options:**

- **Railway.app** - Automatic deployment, $5 free monthly credit
- **Heroku** - Industry standard, 550+ dyno hours free
- **Vercel** - Lightning fast, perfect for students
- **PythonAnywhere** - Educational discounts available

📖 **Detailed deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions for all platforms.

## 📦 Installation

## 📦 Local Installation

### Quick Setup (Windows)

```bash
setup.bat
```

### Quick Setup (Mac/Linux)

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

1. **Clone or download the project**
2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   python app.py
   ```
5. **Access locally**: Open `http://localhost:5000`

## 🌐 Production Deployment

Your app is production-ready with:

- ✅ Environment-based configuration
- ✅ Gunicorn WSGI server
- ✅ Security best practices
- ✅ Database auto-initialization
- ✅ Cross-platform compatibility

## 💡 Usage

1. **Student Registration**: Enter name and PRN number
2. **Take Quiz**: Answer all 50 multiple-choice questions
3. **Submit**: Review and submit your answers
4. **View Results**: See your score and performance analysis

## 📊 Database Schema

### Students Table

- `id`: Primary key
- `name`: Student name
- `prn`: Student PRN number
- `total_score`: Final score
- `submission_time`: Timestamp

### Quiz Responses Table

- `id`: Primary key
- `student_id`: Foreign key to students
- `question_id`: Question identifier
- `selected_option`: Student's answer choice
- `is_correct`: Boolean for correctness
- `section`: Quiz section name

## 🎨 UI Features

- **Modern Design**: Gradient backgrounds and smooth animations
- **Progress Tracking**: Visual progress bar
- **Interactive Elements**: Hover effects and smooth transitions
- **Performance Indicators**: Color-coded results based on score
- **Print Support**: Printable results page

## 🔧 Customization

You can easily customize:

- **Questions**: Modify the `QUIZ_QUESTIONS` dictionary in `app.py`
- **Scoring**: Adjust marks per question
- **Styling**: Update CSS in the HTML templates
- **Database**: Switch to other databases by modifying connection strings

## 📱 Responsive Design

The website is fully responsive and works on:

- Desktop computers
- Tablets
- Mobile phones
- Different screen orientations

## 🎓 Educational Value

This quiz system helps students:

- Test their knowledge across multiple domains
- Identify areas for improvement
- Track their learning progress
- Practice exam-style questions

## 📝 License

This project is created for educational purposes for the AI Club.

## 🤝 Contributing

To add more questions or features:

1. Update the question database in `app.py`
2. Modify the frontend templates as needed
3. Test thoroughly before deployment

---

**Created for AI Club - Revision Quiz System**
_Empowering students through interactive learning and assessment_
