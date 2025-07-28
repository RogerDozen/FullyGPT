import os
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

    if request.method == "POST":
        user_msg = request.form.get("message", "").strip()
        if user_msg:
            session["messages"].append({"role": "user", "content": user_msg})
            response = get_response(session["messages"])
            session["messages"].append({"role": "assistant", "content": response})

    return render_template_string(TEMPLATE, messages=session.get("messages", []))

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

if __name__ == "__main__":
    app.run(debug=True)
