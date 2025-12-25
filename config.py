import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# القناة المطلوب الاشتراك بها
REQUIRED_CHANNEL = "@RISK_VIR"

if not TELEGRAM_TOKEN:
    print("Warning: TELEGRAM_TOKEN is not set in environment variables.")

if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY is not set in environment variables.")
