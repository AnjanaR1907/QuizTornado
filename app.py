from flask import Flask, request, render_template_string
import openai
import os
import json

app = Flask(__name__)

# Load API key from Render environment
openai.api_key = os.environ.get("OPENAI_API_KEY")

HTML_HOME = """
<!DOCTYPE html>
<html>
<head>
    <title>QuizTornado - AI Quiz Generator</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to right, #74ebd5, #acb6e5);
            text-align: center;
            padding-top: 80px;
            color: #333;
        }
        h1 {
            font-size: 42px;
            margin-bottom: 20px;
            color: #2c3e50;
        }
        form {
            background-color: white;
            display: inline-block;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
        }
        input[type="text"], button {
            font-size: 18px;
            padding: 10px;
            width: 80%;
            margin: 10px 0;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        button:hover {
            background-color: #2980b9;
        }
    </style>
</head>
<body>
    <h1>QuizTornado 🌪️</h1>
    <form action="/quiz" method="POST">
        <input type="text" name="topic" placeholder="Enter a topic (e.g., Space, Microbes)" required>
        <br>
        <button type="submit">Generate Quiz</button>
    </form>
</body>
</html>
"""

HTML_QUIZ = """
<!DOCTYPE html>
<html>
<head>
    <title>Quiz on {{ topic }}</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #fceabb;
            background-image: linear-gradient(315deg, #fceabb 0%, #f8b500 74%);
            text-align: center;
            padding: 50px;
            color: #333;
        }
        form {
            background: white;
            padding: 30px;
            border-radius: 12px;
            display: inline-block;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
            text-align: left;
        }
        .question {
            margin-bottom: 20px;
        }
        h2 {
            text-align: center;
            color: #2c3e50;
        }
        button {
            display: block;
            margin: 20px auto 0;
            padding: 10px 20px;
            font-size: 16px;
            background: #e67e22;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        button:hover {
            background: #d35400;
        }
    </style>
</head>
<body>
    <h2>Quiz on {{ topic }}</h2>
    <form action="/submit" method="POST">
        {% for q in quiz %}
            <div class="question">
                <p><b>Q{{ loop.index }}. {{ q.question }}</b></p>
                {% for opt in q.options %}
                    <label>
                        <input type="radio" name="q{{ loop.parent.index }}" value="{{ opt }}" required> {{ opt }}
                    </label><br>
                {% endfor %}
                <input type="hidden" name="answer{{ loop.index }}" value="{{ q.answer }}">
            </div>
        {% endfor %}
        <input type="hidden" name="topic" value="{{ topic }}">
        <button type="submit">Submit Answers</button>
    </form>
</body>
</html>
"""

HTML_SCORE = """
<!DOCTYPE html>
<html>
<head>
    <title>Quiz Score</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to right, #43e97b, #38f9d7);
            text-align: center;
            padding-top: 100px;
            color: #2c3e50;
        }
        .score-box {
            background: white;
            display: inline-block;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
        }
        h2 {
            font-size: 36px;
        }
    </style>
</head>
<body>
    <div class="score-box">
        <h2>Your Score: {{ score }} / {{ total }}</h2>
        <p>Topic: <strong>{{ topic }}</strong></p>
        <a href="/">Try another quiz</a>
    </div>
</body>
</html>
"""

def generate_quiz(topic):
    prompt = f"""
    Create a multiple-choice quiz with 5 questions about {topic}.
    Each question should have 4 options and one correct answer.
    Format the response as a JSON list like this:
    [
      {{
        "question": "Question text",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "Correct option text"
      }},
      ...
    ]
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    content = response.choices[0].message.content.strip()
    try:
        return json.loads(content)
    except Exception as e:
        return []

@app.route('/')
def home():
    return render_template_string(HTML_HOME)

@app.route('/quiz', methods=['POST'])
def quiz():
    topic = request.form['topic']
    quiz = generate_quiz(topic)
    if not quiz:
        return "Failed to generate quiz. Try again."
    return render_template_string(HTML_QUIZ, quiz=quiz, topic=topic)

@app.route('/submit', methods=['POST'])
def submit():
    topic = request.form['topic']
    score = 0
    total = 0
    for i in range(1, 6):
        user_answer = request.form.get(f'q{i}')
        correct_answer = request.form.get(f'answer{i}')
        if user_answer and correct_answer:
            total += 1
            if user_answer.strip() == correct_answer.strip():
                score += 1
    return render_template_string(HTML_SCORE, score=score, total=total, topic=topic)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
