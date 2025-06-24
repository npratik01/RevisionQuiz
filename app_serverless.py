from flask import Flask, render_template, request, jsonify, send_file
import json
from datetime import datetime
import os
import uuid
import time
import csv
import io
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Create data directory if it doesn't exist
DATA_DIR = Path('quiz_data')
DATA_DIR.mkdir(exist_ok=True)

# File paths for persistent storage
STUDENTS_FILE = DATA_DIR / 'students.json'
RESPONSES_FILE = DATA_DIR / 'responses.json'

# Admin credentials (you can change these)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'aiclub2024')

def load_students_data():
    """Load students data from JSON file"""
    try:
        if STUDENTS_FILE.exists():
            with open(STUDENTS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading students data: {e}")
    return {}

def save_students_data(data):
    """Save students data to JSON file"""
    try:
        with open(STUDENTS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving students data: {e}")

def load_responses_data():
    """Load responses data from JSON file"""
    try:
        if RESPONSES_FILE.exists():
            with open(RESPONSES_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading responses data: {e}")
    return {}

def save_responses_data(data):
    """Save responses data to JSON file"""
    try:
        with open(RESPONSES_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving responses data: {e}")

# Load existing data
students_data = load_students_data()
quiz_responses = load_responses_data()

# Security headers middleware
@app.after_request
def after_request(response):
    # Security headers to prevent various attacks
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src 'self'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Quiz questions data (keeping the same structure)
QUIZ_QUESTIONS = {
    "mathematics": [
        {
            "id": 1,
            "question": "What is the probability of getting a head when flipping a fair coin?",
            "options": ["0.25", "0.5", "0.75", "1.0"],
            "correct": 1
        },
        {
            "id": 2,
            "question": "A discrete random variable can take which type of values?",
            "options": ["Continuous values", "Countable values", "Infinite decimal values", "Complex numbers"],
            "correct": 1
        },
        {
            "id": 3,
            "question": "Which of the following is an example of a continuous random variable?",
            "options": ["Number of students in a class", "Temperature", "Number of cars", "Number of books"],
            "correct": 1
        },
        {
            "id": 4,
            "question": "In joint probability distribution, P(X,Y) represents:",
            "options": ["P(X) + P(Y)", "P(X) * P(Y)", "P(X and Y)", "P(X or Y)"],
            "correct": 2
        },
        {
            "id": 5,
            "question": "In a binomial distribution, what are the two possible outcomes called?",
            "options": ["Success and Failure", "True and False", "Yes and No", "All of the above"],
            "correct": 3
        },
        {
            "id": 6,
            "question": "Bernoulli trials have how many possible outcomes?",
            "options": ["1", "2", "3", "4"],
            "correct": 1
        },
        {
            "id": 7,
            "question": "Poisson distribution is used to model:",
            "options": ["Continuous data", "Rare events", "Normal data", "Binary outcomes"],
            "correct": 1
        },
        {
            "id": 8,
            "question": "The variance of a dataset measures:",
            "options": ["Central tendency", "Spread of data", "Skewness", "Kurtosis"],
            "correct": 1
        },
        {
            "id": 9,
            "question": "In a normal distribution, what percentage of data falls within 1 standard deviation?",
            "options": ["68%", "95%", "99%", "50%"],
            "correct": 0
        },
        {
            "id": 10,
            "question": "Bivariate normal distribution involves how many variables?",
            "options": ["1", "2", "3", "4"],
            "correct": 1
        }
    ],
    "python": [
        {
            "id": 11,
            "question": "What is the output of the following code?\n\nx = [1, 2, 3]\ny = x\ny.append(4)\nprint(x)",
            "options": ["[1, 2, 3]", "[1, 2, 3, 4]", "[4]", "Error"],
            "correct": 1
        },
        {
            "id": 12,
            "question": "What will be printed?\n\ndef func(a, b=[]):\n    b.append(a)\n    return b\n\nprint(func(1))\nprint(func(2))",
            "options": ["[1]\n[2]", "[1]\n[1, 2]", "[1, 2]\n[1, 2]", "Error"],
            "correct": 1
        },
        {
            "id": 13,
            "question": "What is the output?\n\nx = 'hello'\nresult = x[1:4]\nprint(result)",
            "options": ["hel", "ell", "ello", "hell"],
            "correct": 1
        },
        {
            "id": 14,
            "question": "What will this code print?\n\nfor i in range(3):\n    for j in range(2):\n        if i == j:\n            break\n    print(i, j)",
            "options": ["0 0\n1 0\n2 0", "0 1\n1 1\n2 1", "0 0\n1 1\n2 1", "Error"],
            "correct": 2
        },
        {
            "id": 15,
            "question": "What is the result?\n\nd = {'a': 1, 'b': 2}\nresult = d.get('c', 0) + d.get('a', 0)\nprint(result)",
            "options": ["0", "1", "2", "Error"],
            "correct": 1
        },
        {
            "id": 16,
            "question": "What will be the output?\n\nclass A:\n    x = 1\n\na = A()\nb = A()\na.x = 2\nprint(A.x, a.x, b.x)",
            "options": ["1 2 1", "2 2 2", "1 1 1", "2 2 1"],
            "correct": 0
        },
        {
            "id": 17,
            "question": "What does this code output?\n\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    result = 'Error'\nfinally:\n    print('Done')\nprint(result)",
            "options": ["Done\nError", "Error\nDone", "Done", "Error"],
            "correct": 0
        },
        {
            "id": 18,
            "question": "What is the output?\n\nlst = [1, 2, 3, 4, 5]\nprint(lst[::2])",
            "options": ["[1, 2, 3]", "[1, 3, 5]", "[2, 4]", "[5, 4, 3, 2, 1]"],
            "correct": 1
        },
        {
            "id": 19,
            "question": "What will this print?\n\ndef outer():\n    x = 1\n    def inner():\n        nonlocal x\n        x = 2\n    inner()\n    return x\n\nprint(outer())",
            "options": ["1", "2", "None", "Error"],
            "correct": 1
        },
        {
            "id": 20,
            "question": "What is the result?\n\ndata = [1, 2, 3]\nresult = list(map(lambda x: x * 2, data))\nprint(result)",
            "options": ["[1, 2, 3]", "[2, 4, 6]", "[1, 4, 9]", "Error"],
            "correct": 1
        },
        {
            "id": 21,
            "question": "What will be printed?\n\nx = [1, 2, 3]\ny = [*x, 4, 5]\nprint(len(y))",
            "options": ["3", "4", "5", "Error"],
            "correct": 2
        },
        {
            "id": 22,
            "question": "What is the output?\n\nclass Parent:\n    def method(self):\n        return 'Parent'\n\nclass Child(Parent):\n    def method(self):\n        return 'Child'\n\nc = Child()\nprint(c.method())",
            "options": ["Parent", "Child", "Both", "Error"],
            "correct": 1
        },
        {
            "id": 23,
            "question": "What does this code print?\n\nset1 = {1, 2, 3}\nset2 = {3, 4, 5}\nresult = set1 & set2\nprint(result)",
            "options": ["{1, 2, 3, 4, 5}", "{3}", "{1, 2}", "{4, 5}"],
            "correct": 1
        },
        {
            "id": 24,
            "question": "What will be the output?\n\nfrom functools import reduce\nnumbers = [1, 2, 3, 4]\nresult = reduce(lambda x, y: x + y, numbers)\nprint(result)",
            "options": ["[1, 2, 3, 4]", "10", "24", "Error"],
            "correct": 1
        },
        {
            "id": 25,
            "question": "What is the result?\n\ndef generator():\n    yield 1\n    yield 2\n    yield 3\n\ng = generator()\nprint(next(g), next(g))",
            "options": ["1 1", "1 2", "2 3", "Error"],
            "correct": 1
        }
    ],
    "python_libraries": [
        {
            "id": 26,
            "question": "What is the output of this NumPy code?\n\nimport numpy as np\narr = np.array([1, 2, 3, 4])\nresult = arr[arr > 2]\nprint(result)",
            "options": ["[1 2]", "[3 4]", "[True False]", "[1 2 3 4]"],
            "correct": 1
        },
        {
            "id": 27,
            "question": "What does this Pandas code output?\n\nimport pandas as pd\ndf = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})\nprint(df.shape)",
            "options": ["(3, 2)", "(2, 3)", "6", "(3,)"],
            "correct": 0
        },
        {
            "id": 28,
            "question": "What is the result of this NumPy operation?\n\nimport numpy as np\na = np.array([[1, 2], [3, 4]])\nb = np.array([[5, 6], [7, 8]])\nresult = a * b\nprint(result[0, 0])",
            "options": ["5", "6", "26", "19"],
            "correct": 0
        },
        {
            "id": 29,
            "question": "What will this Pandas code print?\n\nimport pandas as pd\ns = pd.Series([1, 2, 3, 4, 5])\nresult = s[s > 3]\nprint(len(result))",
            "options": ["2", "3", "4", "5"],
            "correct": 0
        },
        {
            "id": 30,
            "question": "What is the output?\n\nimport numpy as np\narr = np.arange(6).reshape(2, 3)\nprint(arr.sum(axis=0))",
            "options": ["[3 5 7]", "[3 12]", "15", "[0 1 2]"],
            "correct": 0
        },
        {
            "id": 31,
            "question": "What does this Pandas code return?\n\nimport pandas as pd\ndf = pd.DataFrame({'A': [1, 2, None], 'B': [4, None, 6]})\nresult = df.dropna()\nprint(len(result))",
            "options": ["0", "1", "2", "3"],
            "correct": 1
        },
        {
            "id": 32,
            "question": "What is the result of this NumPy code?\n\nimport numpy as np\narr = np.array([1, 2, 3, 4, 5])\nresult = np.where(arr > 3, arr, 0)\nprint(result)",
            "options": ["[1 2 3 4 5]", "[0 0 0 4 5]", "[4 5]", "[0 0 0 1 1]"],
            "correct": 1
        },
        {
            "id": 33,
            "question": "What will this Pandas code output?\n\nimport pandas as pd\ndf = pd.DataFrame({'A': [1, 2, 3], 'B': [1, 2, 3]})\nresult = df['A'] + df['B']\nprint(result.iloc[1])",
            "options": ["2", "3", "4", "5"],
            "correct": 2
        },
        {
            "id": 34,
            "question": "What does this NumPy code print?\n\nimport numpy as np\na = np.array([1, 2, 3])\nb = np.array([4, 5, 6])\nresult = np.dot(a, b)\nprint(result)",
            "options": ["[4 10 18]", "32", "21", "[5 7 9]"],
            "correct": 1
        },
        {
            "id": 35,
            "question": "What is the output of this Pandas code?\n\nimport pandas as pd\ndf = pd.DataFrame({'A': [1, 2, 2, 3]})\nresult = df['A'].value_counts()\nprint(result.iloc[0])",
            "options": ["1", "2", "3", "4"],
            "correct": 1
        },
        {
            "id": 36,
            "question": "What does this NumPy code return?\n\nimport numpy as np\narr = np.array([[1, 2, 3], [4, 5, 6]])\nresult = arr.flatten()\nprint(len(result))",
            "options": ["2", "3", "6", "9"],
            "correct": 2
        },
        {
            "id": 37,
            "question": "What will this Pandas code print?\n\nimport pandas as pd\ndf = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})\nresult = df.iloc[1, 1]\nprint(result)",
            "options": ["2", "4", "5", "6"],
            "correct": 2
        },
        {
            "id": 38,
            "question": "What is the result?\n\nimport numpy as np\narr = np.array([1, 2, 3, 4])\nresult = arr.reshape(2, 2)\nprint(result[1, 0])",
            "options": ["1", "2", "3", "4"],
            "correct": 2
        },
        {
            "id": 39,
            "question": "What does this Pandas code output?\n\nimport pandas as pd\ndf = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})\nresult = df.mean()\nprint(result['A'])",
            "options": ["1.0", "2.0", "3.0", "6.0"],
            "correct": 1
        },
        {
            "id": 40,
            "question": "What is the output?\n\nimport numpy as np\na = np.array([1, 2, 3])\nb = a.copy()\nb[0] = 10\nprint(a[0])",
            "options": ["1", "10", "3", "Error"],
            "correct": 0
        },
        {
            "id": 41,
            "question": "What will this Pandas code print?\n\nimport pandas as pd\ndf = pd.DataFrame({'A': [1, 2, 3]})\ndf['B'] = df['A'] * 2\nprint(df.columns.tolist())",
            "options": ["['A']", "['B']", "['A', 'B']", "Error"],
            "correct": 2
        },
        {
            "id": 42,
            "question": "What does this NumPy code return?\n\nimport numpy as np\narr = np.array([1, 2, 3, 4, 5])\nresult = arr[::2]\nprint(result)",
            "options": ["[1 2 3]", "[1 3 5]", "[2 4]", "[5 3 1]"],
            "correct": 1
        },
        {
            "id": 43,
            "question": "What is the output of this Pandas code?\n\nimport pandas as pd\ndf = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})\nresult = df.T\nprint(result.shape)",
            "options": ["(3, 2)", "(2, 3)", "(6,)", "(1, 6)"],
            "correct": 1
        },
        {
            "id": 44,
            "question": "What does this NumPy code print?\n\nimport numpy as np\narr = np.array([1, 2, 3])\nresult = np.append(arr, [4, 5])\nprint(len(result))",
            "options": ["3", "4", "5", "2"],
            "correct": 2
        },
        {
            "id": 45,
            "question": "What will this Pandas code output?\n\nimport pandas as pd\ndf = pd.DataFrame({'A': [1, 2, 3]})\ndf.loc[3] = [4]\nprint(len(df))",
            "options": ["3", "4", "1", "Error"],
            "correct": 1
        },
        {
            "id": 46,
            "question": "What is the result?\n\nimport numpy as np\na = np.array([1, 2, 3])\nb = np.array([1, 0, 1])\nresult = a[b.astype(bool)]\nprint(result)",
            "options": ["[1 3]", "[1 2 3]", "[2]", "[0 1]"],
            "correct": 0
        },
        {
            "id": 47,
            "question": "What does this Pandas code return?\n\nimport pandas as pd\ns1 = pd.Series([1, 2, 3])\ns2 = pd.Series([4, 5, 6])\nresult = s1 + s2\nprint(result.iloc[0])",
            "options": ["1", "4", "5", "7"],
            "correct": 2
        },
        {
            "id": 48,
            "question": "What is the output?\n\nimport numpy as np\narr = np.array([[1, 2], [3, 4]])\nresult = arr.max(axis=1)\nprint(result)",
            "options": ["[1 3]", "[2 4]", "[3 4]", "4"],
            "correct": 1
        },
        {
            "id": 49,
            "question": "What will this Pandas code print?\n\nimport pandas as pd\ndf = pd.DataFrame({'A': [1, 2, 1], 'B': [3, 4, 3]})\nresult = df.drop_duplicates()\nprint(len(result))",
            "options": ["1", "2", "3", "4"],
            "correct": 1
        },
        {
            "id": 50,
            "question": "What does this NumPy code output?\n\nimport numpy as np\narr = np.array([1, 2, 3, 4, 5])\nresult = np.split(arr, [2, 4])\nprint(len(result))",
            "options": ["2", "3", "4", "5"],
            "correct": 1
        }
    ]
}

@app.route('/')
def index():
    return render_template('index_simple.html')

@app.route('/register', methods=['POST'])
def register_student():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        prn = data.get('prn', '').strip()
        
        if not name or not prn:
            return jsonify({'error': 'Name and PRN are required'}), 400
        
        # Generate unique student ID
        student_id = str(uuid.uuid4())        # Store student data persistently
        students_data[student_id] = {
            'id': student_id,
            'name': name,
            'prn': prn,
            'total_score': 0,
            'registration_time': datetime.now().isoformat(),
            'responses': {}
        }
          # Save to file
        save_students_data(students_data)
        
        return jsonify({
            'success': True, 
            'student_id': student_id,
            'name': name,
            'prn': prn
        })
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed. Please try again.'}), 500

@app.route('/questions')
def get_questions():
    return jsonify(QUIZ_QUESTIONS)

@app.route('/submit', methods=['POST'])
def submit_quiz():
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        responses = data.get('responses', {})
        auto_submit = data.get('auto_submit', False)
        time_taken = data.get('time_taken', 0)  # Optional timing data for records
        
        if not student_id or student_id not in students_data:
            return jsonify({'error': 'Invalid student session'}), 400
        
        student = students_data[student_id]
        # Check if already submitted
        if 'final_submission_time' in student:
            return jsonify({'error': 'Quiz already submitted'}), 400
          # Log submission details
        print(f"Submission received - Time taken: {time_taken} seconds, Auto-submit: {auto_submit}")
        
        # Validate response format
        for question_id, response in responses.items():
            if not isinstance(response, int) or response < 0 or response > 3:
                return jsonify({'error': 'Invalid response format detected'}), 400
        
        total_score = 0
        
        # Process each section
        for section, questions in QUIZ_QUESTIONS.items():
            for question in questions:
                question_id = str(question['id'])
                correct_answer = question['correct']
                
                if question_id in responses:
                    selected_option = responses[question_id]
                    is_correct = selected_option == correct_answer
                    
                    if is_correct:
                        total_score += 2  # Each question carries 2 marks
                      # Store response
                    student['responses'][question_id] = {
                        'selected_option': selected_option,
                        'is_correct': is_correct,
                        'section': section
                    }
        
        # Update student's final submission data
        student['total_score'] = total_score
        student['final_submission_time'] = datetime.now().isoformat()
        student['time_taken_seconds'] = time_taken
        student['auto_submitted'] = auto_submit
        
        # Save updated student data persistently
        save_students_data(students_data)
        
        # Calculate time taken in minutes for display
        time_minutes = round(time_taken / 60, 1)
        
        return jsonify({
            'success': True,
            'total_score': total_score,
            'percentage': (total_score / 100) * 100,
            'student_name': student['name'],
            'prn': student['prn'],
            'time_taken_minutes': time_minutes,
            'auto_submitted': auto_submit
        })
        
    except Exception as e:
        print(f"Submission error: {str(e)}")
        return jsonify({'error': 'Submission failed. Please try again.'}), 500

@app.route('/results')
def results():
    return render_template('results.html')

# Admin routes for viewing and downloading quiz results
@app.route('/admin')
def admin_login():
    """Admin login page"""
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard to view quiz results"""
    # Simple authentication check
    auth = request.authorization
    if not auth or auth.username != ADMIN_USERNAME or auth.password != ADMIN_PASSWORD:
        # Return a 401 with WWW-Authenticate header to trigger browser auth
        response = jsonify({'error': 'Authentication required'})
        response.status_code = 401
        response.headers['WWW-Authenticate'] = 'Basic realm="Admin Area"'
        return response
    
    # Load current data
    current_students = load_students_data()
    
    # Prepare summary statistics
    total_students = len(current_students)
    completed_students = len([s for s in current_students.values() if s.get('final_submission_time')])
    average_score = 0
    if completed_students > 0:
        total_scores = sum(s.get('total_score', 0) for s in current_students.values() if s.get('final_submission_time'))
        average_score = round(total_scores / completed_students, 2)
    
    stats = {
        'total_students': total_students,
        'completed_students': completed_students,
        'average_score': average_score,
        'last_updated': datetime.now().isoformat()
    }
    
    return render_template('admin_dashboard.html', students=current_students, stats=stats)

@app.route('/admin/api/students')
def admin_api_students():
    """API endpoint to get students data (with authentication)"""
    auth = request.authorization
    if not auth or auth.username != ADMIN_USERNAME or auth.password != ADMIN_PASSWORD:
        return jsonify({'error': 'Authentication required'}), 401
    
    return jsonify(load_students_data())

@app.route('/admin/download/csv')
def download_csv():
    """Download quiz results as CSV"""
    auth = request.authorization
    if not auth or auth.username != ADMIN_USERNAME or auth.password != ADMIN_PASSWORD:
        response = jsonify({'error': 'Authentication required'})
        response.status_code = 401
        response.headers['WWW-Authenticate'] = 'Basic realm="Admin Area"'
        return response
    
    # Load current data
    current_students = load_students_data()
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Student ID', 'Name', 'PRN', 'Total Score', 'Percentage', 
        'Registration Time', 'Submission Time', 'Time Taken (minutes)', 
        'Auto Submitted', 'Status'
    ])
    
    # Write student data
    for student in current_students.values():
        time_taken_minutes = ''
        if student.get('time_taken_seconds'):
            time_taken_minutes = round(student['time_taken_seconds'] / 60, 1)
        
        status = 'Completed' if student.get('final_submission_time') else 'Registered'
        percentage = round((student.get('total_score', 0) / 100) * 100, 1)
        
        writer.writerow([
            student.get('id', ''),
            student.get('name', ''),
            student.get('prn', ''),
            student.get('total_score', 0),
            f"{percentage}%",
            student.get('registration_time', ''),
            student.get('final_submission_time', ''),
            time_taken_minutes,
            'Yes' if student.get('auto_submitted') else 'No',
            status
        ])
    
    output.seek(0)
    
    # Create response with CSV file
    response = send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'quiz_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )
    
    return response

@app.route('/admin/download/json')
def download_json():
    """Download quiz results as JSON"""
    auth = request.authorization
    if not auth or auth.username != ADMIN_USERNAME or auth.password != ADMIN_PASSWORD:
        response = jsonify({'error': 'Authentication required'})
        response.status_code = 401
        response.headers['WWW-Authenticate'] = 'Basic realm="Admin Area"'
        return response
    
    # Load current data
    current_students = load_students_data()
    
    # Create JSON response
    response_data = {
        'export_time': datetime.now().isoformat(),
        'total_students': len(current_students),
        'students': current_students
    }
    
    response = send_file(
        io.BytesIO(json.dumps(response_data, indent=2).encode('utf-8')),
        mimetype='application/json',
        as_attachment=True,
        download_name=f'quiz_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    )
    
    return response

# Health check for serverless platforms
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
