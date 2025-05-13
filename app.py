from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>QuizTornado</title>
    <style>
        body {
            background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
            font-family: 'Segoe UI', sans-serif;
            text-align: center;
            padding-top: 30px;
        }
        h1 {
            color: #ffffff;
            text-shadow: 2px 2px #333;
        }
        form {
            background: white;
            padding: 30px;
            border-radius: 12px;
            width: 80%;
            margin: auto;
            max-width: 600px;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
        }
        input[type="text"] {
            padding: 10px;
            width: 80%;
            font-size: 16px;
        }
        button {
            margin-top: 20px;
            padding: 10px 25px;
            font-size: 16px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 8px;
        }
        .question {
            text-align: left;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>🌀 QuizTornado</h1>

    {% if not questions %}
        <form method="POST">
            <input type="text" name="topic" placeholder="Enter quiz topic (e.g. Cybersecurity)" required>
            <br><br>
            <button type="submit">Generate Quiz</button>
        </form>
    {% else %}
        <form method="POST" action="/submit">
            {% for q in questions %}
                <div class="question">
                    <p><b>Q{{ loop.index }}. {{ q['question'] }}</b></p>
                    {% for opt in q['options'] %}
                        <label><input type="radio" name="q{{ loop.index0 }}" value="{{ opt }}" required> {{ opt }}</label><br>
                    {% endfor %}
                </div>
            {% endfor %}
            <input type="hidden" name="topic" value="{{ topic }}">
            <button type="submit">Submit Quiz</button>
        </form>
    {% endif %}
</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>QuizTornado Result</title>
    <style>
        body {
            background-color: #e0f7fa;
            font-family: 'Segoe UI', sans-serif;
            text-align: center;
            padding-top: 50px;
        }
        .result-box {
            background: white;
            padding: 30px;
            margin: auto;
            width: 60%;
            max-width: 500px;
            border-radius: 12px;
            box-shadow: 0 0 12px rgba(0,0,0,0.2);
        }
        h2 {
            color: #333;
        }
        a {
            text-decoration: none;
            color: white;
            background-color: #007BFF;
            padding: 10px 20px;
            border-radius: 8px;
            display: inline-block;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="result-box">
        <h2>Your Score: {{ score }} / {{ total }}</h2>
        <p><b>Topic:</b> {{ topic }}</p>
        <a href="/">Take Another Quiz</a>
    </div>
</body>
</html>
"""

# Dummy quiz generator with correct answers
def generate_quiz(topic):
    if topic.lower() == "cybersecurity":
        return [
            {
                "question": "What is a common goal of cybersecurity?",
                "options": ["Data protection", "File sharing", "Gaming", "Advertising"],
                "answer": "Data protection"
            },
            {
                "question": "Which of the following is a type of cyber attack?",
                "options": ["Phishing", "Fishing", "Wishing", "Typing"],
                "answer": "Phishing"
            },
            {
                "question": "What does a firewall do?",
                "options": ["Blocks unauthorized access", "Heats the CPU", "Cleans malware", "Stores files"],
                "answer": "Blocks unauthorized access"
            },
            {
                "question": "Which of these is a strong password?",
                "options": ["123456", "password", "John2020", "D@t@_S3cUr3!"],
                "answer": "D@t@_S3cUr3!"
            },
            {
                "question": "Which of these is a cybersecurity best practice?",
                "options": ["Using same password everywhere", "Clicking all email links", "Regular software updates", "Ignoring security warnings"],
                "answer": "Regular software updates"
            }
        ]
    else:
        # fallback dummy questions for other topics
        return [
            {
                "question": f"What is {topic} best known for?",
                "options": [f"A concept in {topic}", f"A use of {topic}", f"A fact about {topic}", f"An application of {topic}"],
                "answer": f"A use of {topic}"
            },
            {
                "question": f"What can you learn from {topic}?",
                "options": [f"Insight A", f"Insight B", f"Insight C", f"Insight D"],
                "answer": f"Insight A"
            },
            {
                "question": f"Who is related to {topic}?",
                "options": [f"Person A", f"Person B", f"Person C", f"Person D"],
                "answer": f"Person A"
            },
            {
                "question": f"What is a fact about {topic}?",
                "options": [f"Fact A", f"Fact B", f"Fact C", f"Fact D"],
                "answer": f"Fact A"
            },
            {
                "question": f"Which of the following relates to {topic}?",
                "options": [f"{topic} A", f"{topic} B", f"{topic} C", f"{topic} D"],
                "answer": f"{topic} A"
            }
        ]

# Store questions in session or cache
latest_questions = []
latest_answers = []
latest_topic = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    global latest_questions, latest_answers, latest_topic
    if request.method == 'POST':
        topic = request.form['topic']
        quiz = generate_quiz(topic)
        latest_questions = quiz
        latest_answers = [q['answer'] for q in quiz]
        latest_topic = topic
        return render_template_string(HTML_TEMPLATE, questions=quiz, topic=topic)
    return render_template_string(HTML_TEMPLATE, questions=None, topic="")

@app.route('/submit', methods=['POST'])
def submit():
    global latest_questions, latest_answers, latest_topic
    score = 0
    for i, correct_answer in enumerate(latest_answers):
        user_answer = request.form.get(f'q{i}')
        if user_answer == correct_answer:
            score += 1
    return render_template_string(RESULT_TEMPLATE, score=score, total=len(latest_answers), topic=latest_topic)

if __name__ == '__main__':
    app.run(debug=True)
