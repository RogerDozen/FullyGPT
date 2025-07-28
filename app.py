import os
import json
from flask import Flask, render_template_string, request, session
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("OPENAI_API_KEY.env")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

TEMPLATE = """
<!doctype html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\">
    <title>Relationship Advisor Chat</title>
</head>
<body>
    <h1>Relationship Advisor Chat</h1>
    <div id=\"chat\">
        {% for msg in messages %}
            <p><strong>{{ msg.role.capitalize() }}:</strong> {{ msg.content }}</p>
        {% endfor %}
    </div>
    <form method=\"post\">
        <input type=\"text\" name=\"message\" placeholder=\"Type your message...\" required>
        <button type=\"submit\">Send</button>
    </form>
    {% if pros or cons %}
    <div id=\"pros-cons\">
        <h2>Pros</h2>
        <ul>
        {% for item in pros %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>
        <h2>Cons</h2>
        <ul>
        {% for item in cons %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize chat history in the session
    if "messages" not in session:
        session["messages"] = [
            {
                "role": "system",
                "content": (
                    "You are a relationship advisor for women seeking insight "
                    "about their crush or boyfriend."
                ),
            }
        ]
    if "pros" not in session:
        session["pros"] = []
    if "cons" not in session:
        session["cons"] = []

    if request.method == "POST":
        user_msg = request.form.get("message", "").strip()
        if user_msg:
            session["messages"].append({"role": "user", "content": user_msg})
            response = get_response(session["messages"])
            session["messages"].append({"role": "assistant", "content": response})
            session["pros"], session["cons"] = update_pros_cons(
                session["messages"], session["pros"], session["cons"]
            )

    return render_template_string(
        TEMPLATE,
        messages=session.get("messages", []),
        pros=session.get("pros", []),
        cons=session.get("cons", []),
    )

def get_response(messages):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # Use the accumulated chat history as the prompt
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()


def update_pros_cons(messages, pros, cons):
    """Use GPT to update the pros and cons lists based on the conversation."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    system_prompt = (
        "Update the existing lists of positive and negative facts about the "
        "person of interest based on the conversation. Respond in JSON with "
        "keys 'pros' and 'cons'. Keep previous items if they still apply."
    )
    update_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Current pros: {pros}\nCurrent cons: {cons}"},
    ] + messages

    response = client.chat.completions.create(
        model="gpt-4",
        messages=update_messages,
        temperature=0.3,
        max_tokens=150,
    )
    text = response.choices[0].message.content.strip()
    try:
        data = json.loads(text)
        pros = data.get("pros", pros)
        cons = data.get("cons", cons)
    except json.JSONDecodeError:
        pass
    return pros, cons

if __name__ == "__main__":
    app.run(debug=True)
