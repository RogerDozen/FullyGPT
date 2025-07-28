# Relationship Advisor MVP

This minimal web application allows users to chat with a relationship advisor
powered by GPT-4. Simply type questions about your situation and you'll receive
analysis and suggested plans of action in a conversational format.

## Setup

1. Install dependencies (Flask, python-dotenv and openai):
   ```bash
   pip install flask python-dotenv openai
   ```

2. Copy `OPENAI_API_KEY.env.example` to `OPENAI_API_KEY.env` and add your API key:
   ```bash
   cp OPENAI_API_KEY.env.example OPENAI_API_KEY.env
   # edit OPENAI_API_KEY.env and insert your key
   ```
   You can also set the `OPENAI_API_KEY` environment variable directly.

3. Run the application:
   ```bash
   python app.py
   ```

The app will start a local web server (by default on `http://127.0.0.1:5000`) where you can
have a back-and-forth conversation about your relationship questions.
