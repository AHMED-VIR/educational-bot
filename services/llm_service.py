from google import genai
from groq import Groq
from openai import OpenAI
from config import GEMINI_API_KEY, GROQ_API_KEY, PERPLEXITY_API_KEY
import os
import base64
import io
import requests

class LLMService:
    def __init__(self):
        self.gemini_client = None
        self.groq_client = None
        self.pplx_client = None
        self.openai_client = None # For Perplexity or OpenAI-compatible
        
        # Initialize Gemini
        if GEMINI_API_KEY and not GEMINI_API_KEY.startswith("pplx"):
            try:
                self.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
            except Exception as e:
                print(f"Error init Gemini: {e}")

        # Initialize Perplexity (OpenAI Compatible)
        if PERPLEXITY_API_KEY:
            try:
                self.pplx_client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")
            except Exception as e:
                print(f"Error init Perplexity: {e}")
                
        # Initialize Groq
        if GROQ_API_KEY:
            try:
                self.groq_client = Groq(api_key=GROQ_API_KEY)
            except Exception as e:
                print(f"Error init Groq: {e}")

    def get_system_prompt(self):
        try:
            prompt_path = os.path.join("data", "system_prompt.md")
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "You are a helpful AI assistant. Answer in the same language as the user's question."

    def _encode_image(self, image):
        """Convert PIL Image to base64 string for Groq"""
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def _get_puter_response(self, prompt, model_name):
        """Call Puter.com API"""
        # Emulating the Puter.js call via REST if possible, 
        # OR using a simplified OpenAI-compatible endpoint if we use a bridge.
        # But since we want to be direct:
        
        # NOTE: Puter's REST API requires a token usually.
        # However, for public/free models, sometimes it works with a generic session.
        # We'll try the backend API endpoint found in research or standard OpenAI format
        # pointing to Puter's gateway if we had one.
        # 
        # Research showed "puter.ai.chat()". 
        # Let's try to hit the backend directly.
        
        url = "https://api.puter.com/v2/ai/chat"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # We might need an 'Authorization' header if the user provides a PUTER_TOKEN.
            # If not, we hope for anonymous tier or fail gracefully.
        }
        
        # Puter token from env if available
        puter_token = os.getenv("PUTER_TOKEN")
        if puter_token:
            headers["Authorization"] = f"Bearer {puter_token}"
            
        data = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=60)
            if response.status_code == 200:
                result = response.json()
                # Assuming standard OpenAI-like response or Puter specific
                # Puter response usually: { "message": { "content": "..." } }
                if "message" in result:
                     return result["message"]["content"]
                elif "choices" in result: # OpenAI format
                     return result["choices"][0]["message"]["content"]
                else:
                    return f"⚠️ Unexpected response format from Puter: {result}"
            else:
                 return f"⚠️ API Error ({model_name}): {response.status_code} - {response.text}"
        except Exception as e:
            return f"❌ Connection Error: {e}"

    def get_response(self, user_text, image=None, context_history=None, subject_context=None, model="gemini-1.5-flash"):
        system_prompt = self.get_system_prompt()
        full_prompt = f"{system_prompt}\n\nUser: {user_text}"
        
        # --- Route based on Model Selection ---
        
        # 1. Puter Models
        if model.startswith("gpt") or model.startswith("claude") or model.startswith("o1") or "deepseek" in model or "grok" in model:
             # Just pass the entire prompt to Puter
             return self._get_puter_response(user_text, model)
             
        # 2. Gemini
        if "gemini" in model:
             if self.gemini_client:
                try:
                    response = self.gemini_client.models.generate_content(
                        model=model, # e.g. gemini-1.5-flash
                        contents=[full_prompt]
                    )
                    return response.text
                except Exception as e:
                    return f"Gemini Error: {e}"
        
        # 3. Groq
        if "groq" in model:
             if self.groq_client:
                try:
                    # Map generic "groq" to a specific model if needed
                    groq_model = "llama-3.3-70b-versatile" if model == "groq" else model
                    
                    completion = self.groq_client.chat.completions.create(
                        model=groq_model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_text}
                        ],
                        temperature=0.7,
                    )
                    return completion.choices[0].message.content
                except Exception as e:
                    return f"Groq Error: {e}"

        # Default / Fallback
        return "⚠️ النموذج المختار غير متاح حالياً أو لم يتم التعرف عليه."
