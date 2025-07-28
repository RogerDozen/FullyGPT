# Relationship Advisor MVP

This minimal web application allows users to describe a relationship situation and receive
analysis from GPT-4 about the behavior involved, the pros and cons of the person in question,
and a suggested plan of action.

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
enter your situation and receive an analysis.
