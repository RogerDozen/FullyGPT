import os
from flask import Flask, render_template_string, request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("OPENAI_API_KEY.env")

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\">
    <title>Relationship Advisor</title>
</head>
<body>
    <h1>Relationship Situation Analyzer</h1>
    <form method=\"post\">
        <textarea name=\"situation\" rows=\"10\" cols=\"60\" placeholder=\"Describe your relationship situation...\" required></textarea><br>
        <button type=\"submit\">Analyze</button>
    </form>
    {% if analysis %}
    <h2>Analysis</h2>
    <pre>{{ analysis }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    analysis = None
    if request.method == "POST":
        situation = request.form.get("situation", "")
        if situation:
            analysis = analyze_relationship(situation)
    return render_template_string(TEMPLATE, analysis=analysis)

def analyze_relationship(text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "You are a relationship advisor for women seeking insight about their crush or boyfriend. "
        "Analyze the behavior described in the following text, list pros and cons of the person, "
        "and provide a concise plan of action for dealing with the situation.\n\n" + text
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    app.run(debug=True)
