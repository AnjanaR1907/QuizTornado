from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>QuizTornado</title>
    <style>
        body {
            background: linear-gradient(120deg, #ff9a9e, #fad0c4);
            font-family: 'Segoe UI', sans-serif;
            text-align: center;
            padding-top: 50px;
        }
        h1 {
            color: #ffffff;
            text-shadow: 2px 2px #333;
        }
        form {
            background: white;
            padding: 30px;
            margin: auto;
            display: inline-block;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
        }
        input[type="text"] {
            padding: 10px;
            font-size: 18px;
            width: 300px;
        }
        button {
            padding: 10px 20px;
            font-size: 18px;
            background-color: #ff6f61;
            color: white;
            border: none;
            border-radius: 8px;
            margin-top: 10px;
        }
        .question {
            background: #f5f5f5;
            margin: 10px auto;
            padding: 20px;
            border-radius: 10px;
            width: 70%;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>🌀 QuizTornado</h1>
    <form method="POST">
        <input type="text" name="topic" placeholder="Enter quiz topic (e.g. Python, Space)" required>
        <br>
        <button type="submit">Generate Quiz</button>
    </form>

    {% if questions %}
        <h2>Quiz on "{{ topic }}"</h2>
        {% for q in questions %}
            <div class="question">
                <b>Q{{ loop.index }}:</b> {{ q['question'] }}<br><br>
                {% for opt in q['options'] %}
                    - {{ opt }}<br>
                {% endfor %}
            </div>
        {% endfor %}
    {% endif %}
</body>
</html>
"""

# Sample generator for mock quizzes (replace with AI later)
def generate_quiz(topic):
    sample_questions = [
        {
            "question": f"What is {topic} best known for?",
            "options": [
                f"A concept in {topic}",
                f"A person related to {topic}",
                f"An example of {topic}",
                f"An application of {topic}"
            ]
        },
        {
            "question": f"Which of the following relates to {topic}?",
            "options": [
                f"{topic} Fact A",
                f"{topic} Fact B",
                f"{topic} Fact C",
                f"{topic} Fact D"
            ]
        },
        {
            "question": f"What is a common use of {topic}?",
            "options": [
                f"Use A of {topic}",
                f"Use B of {topic}",
                f"Use C of {topic}",
                f"Use D of {topic}"
            ]
        }
    ]
    random.shuffle(sample_questions)
    return sample_questions

@app.route('/', methods=['GET', 'POST'])
def index():
    questions = []
    topic = ""
    if request.method == 'POST':
        topic = request.form['topic']
        questions = generate_quiz(topic)
    return render_template_string(HTML_TEMPLATE, questions=questions, topic=topic)

if __name__ == '__main__':
    app.run(debug=True)
