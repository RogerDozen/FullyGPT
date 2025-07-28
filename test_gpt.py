import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from OPENAI_API_KEY.env file
load_dotenv("OPENAI_API_KEY.env")

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define prompt
prompt = "Say hi!"

# Send request
response = client.chat.completions.create(
   model="gpt-3.5-turbo",
   messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content.strip())