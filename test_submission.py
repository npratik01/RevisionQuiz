#!/usr/bin/env python3
"""
Quick test script to verify quiz submission works without timing issues
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_quiz_flow():
    """Test the complete quiz flow"""
    print("🧪 Testing Quiz Submission Flow...")
    
    # Step 1: Register a test student
    print("\n1️⃣ Registering test student...")
    register_data = {
        "name": "Test Student",
        "prn": "TEST123"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    if response.status_code == 200:
        result = response.json()
        student_id = result['student_id']
        print(f"✅ Registration successful: {student_id}")
    else:
        print(f"❌ Registration failed: {response.text}")
        return False
    
    # Step 2: Get questions
    print("\n2️⃣ Fetching questions...")
    response = requests.get(f"{BASE_URL}/questions")
    if response.status_code == 200:
        questions = response.json()
        print(f"✅ Got questions: {len(questions['mathematics'])} math, {len(questions['python'])} python, {len(questions['python_libraries'])} libraries")
    else:
        print(f"❌ Failed to get questions: {response.text}")
        return False
    
    # Step 3: Prepare sample responses (answer first few questions)
    print("\n3️⃣ Preparing sample responses...")
    responses = {}
    
    # Answer first 5 questions from each section
    for section_name, section_questions in questions.items():
        for i, question in enumerate(section_questions[:5]):
            responses[str(question['id'])] = 0  # Always choose first option for testing
    
    print(f"✅ Prepared {len(responses)} responses")
    
    # Step 4: Submit with reasonable timing
    print("\n4️⃣ Submitting quiz...")
    time.sleep(2)  # Wait 2 seconds to simulate some quiz time
    
    submit_data = {
        "student_id": student_id,
        "responses": responses,
        "auto_submit": False,
        "time_taken": 120  # 2 minutes
    }
    
    response = requests.post(f"{BASE_URL}/submit", json=submit_data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Submission successful!")
        print(f"   Score: {result['total_score']}/100")
        print(f"   Percentage: {result['percentage']:.1f}%")
        print(f"   Time taken: {result['time_taken_minutes']} minutes")
        return True
    else:
        print(f"❌ Submission failed: {response.text}")
        return False

def test_quick_submission():
    """Test very quick submission to check timing validation"""
    print("\n🚀 Testing Quick Submission (should pass in testing mode)...")
    
    # Register another test student
    register_data = {
        "name": "Quick Test Student",
        "prn": "QUICK123"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    if response.status_code == 200:
        result = response.json()
        student_id = result['student_id']
        print(f"✅ Quick registration successful: {student_id}")
    else:
        print(f"❌ Quick registration failed: {response.text}")
        return False
    
    # Submit immediately with minimal responses
    submit_data = {
        "student_id": student_id,
        "responses": {"1": 0, "2": 1},  # Just answer 2 questions
        "auto_submit": False,
        "time_taken": 5  # Very quick - 5 seconds
    }
    
    response = requests.post(f"{BASE_URL}/submit", json=submit_data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Quick submission successful! (Testing mode is working)")
        print(f"   Score: {result['total_score']}/100")
        return True
    else:
        print(f"❌ Quick submission failed: {response.text}")
        return False

if __name__ == "__main__":
    print("🧪 AI Club Quiz - Submission Testing")
    print("=" * 50)
    
    try:
        # Test normal flow
        success1 = test_quiz_flow()
        
        # Test quick submission
        success2 = test_quick_submission()
        
        print("\n" + "=" * 50)
        if success1 and success2:
            print("🎉 All tests passed! The quiz submission is working correctly.")
            print("💡 The timing validation issue has been resolved.")
        else:
            print("⚠️  Some tests failed. Check the output above for details.")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the Flask app is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
