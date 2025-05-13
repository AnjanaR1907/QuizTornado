from flask import Flask, render_template_string, request
import os
import json
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>QuizTornado</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            text-align: center;
            padding-top: 50px;
        }
        .container {
            background-color: white;
            padding: 30px;
            margin: auto;
            width: 70%;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
        }
        h1 {
            color: #d63384;
        }
        input[type="text"] {
            width: 60%;
            padding: 10px;
            margin-bottom: 20px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #6610f2;
            color: white;
            border: none;
            border-radius: 5px;
        }
        .question {
            margin: 20px 0;
            text-align: left;
        }
        .score {
            font-size: 20px;
            margin-top: 20px;
            color: green;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>QuizTornado 🌪️</h1>
        <form method="POST" action="/quiz">
            <input type="text" name="topic" placeholder="Enter a topic (e.g., Microbes)" required>
            <button type="submit">Generate Quiz</button>
        </form>
        {% if quiz %}
        <form method="POST" action="/score">
            {% for i, q in enumerate(quiz) %}
                <div class="question">
                    <p><b>Q{{ i+1 }}. {{ q.question }}</b></p>
                    {% for option in q.options %}
                        <label>
                            <input type="radio" name="q{{ i }}" value="{{ option }}" required> {{ option }}
                        </label><br>
                    {% endfor %}
                    <input type="hidden" name="a{{ i }}" value="{{ q.answer }}">
                </div>
            {% endfor %}
            <button type="submit">Submit Answers</button>
        </form>
        {% endif %}

        {% if score is not none %}
        <div class="score">
            <p>Your Score: {{ score }}/{{ total }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE)

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
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    content = response.choices[0].message.content.strip()
    try:
        return json.loads(content)
    except Exception as e:
        print("Error parsing quiz:", e)
        return []

@app.route('/quiz', methods=['POST'])
def quiz():
    topic = request.form['topic']
    quiz = generate_quiz(topic)
    return render_template_string(HTML_TEMPLATE, quiz=quiz)

@app.route('/score', methods=['POST'])
def score():
    total = 0
    correct = 0
    for i in range(5):
        selected = request.form.get(f'q{i}')
        answer = request.form.get(f'a{i}')
        if selected == answer:
            correct += 1
        total += 1
    return render_template_string(HTML_TEMPLATE, score=correct, total=total)

if __name__ == '__main__':
    app.run(debug=True)
