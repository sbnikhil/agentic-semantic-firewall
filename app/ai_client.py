import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(prompt: str):
    """Sends redacted text to Groq and returns the answer."""
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Do not mention that data was redacted."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content
