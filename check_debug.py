import os
from google import genai
from config import GEMINI_API_KEY
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=GEMINI_API_KEY)

print("Checking gemini-2.0-flash-exp...")
try:
    client.models.generate_content(model="gemini-2.0-flash-exp", contents="Hi")
    print("SUCCESS 2.0")
except Exception as e:
    print(f"ERROR 2.0: {e}")

print("\nChecking gemini-1.5-flash...")
try:
    client.models.generate_content(model="gemini-1.5-flash", contents="Hi")
    print("SUCCESS 1.5")
except Exception as e:
    print(f"ERROR 1.5: {e}")
