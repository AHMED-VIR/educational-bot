import os
from google import genai
from config import GEMINI_API_KEY
from dotenv import load_dotenv

load_dotenv()

models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.5-pro-001",
    "gemini-1.0-pro",
    "gemini-pro"
]

print("Starting model check...")

if not GEMINI_API_KEY:
    print("No API Key")
    exit()

client = genai.Client(api_key=GEMINI_API_KEY)

for model in models_to_test:
    print(f"--- Testing {model} ---")
    try:
        response = client.models.generate_content(
            model=model,
            contents="Hello"
        )
        print(f"SUCCESS with {model}!")
        break
    except Exception as e:
        print(f"Failed {model}")
