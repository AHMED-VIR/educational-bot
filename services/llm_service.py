from google import genai
from groq import Groq
from openai import OpenAI
from config import GEMINI_API_KEY, GROQ_API_KEY, PERPLEXITY_API_KEY
import os
import base64
import io

class LLMService:
    def __init__(self):
        self.gemini_client = None
        self.groq_client = None
        self.pplx_client = None
        
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

    def get_response(self, user_text, image=None, context_history=None, subject_context=None):
        system_prompt = self.get_system_prompt()
        contents = []
        full_prompt = f"{system_prompt}\n\nUser: {user_text}"
        
        # 1. Try Gemini (Prioritize for images if available/working)
        # Note: If image is present, Perplexity CANNOT handle it.
        # So if image is present, we skipped PPLX or try it only as fallback for text? No, valid PPLX returns error on image.
        
        # Strategy: 
        # If Image: Gemini -> Groq
        # If Text: Perplexity -> Gemini -> Groq
        
        if image:
             # Logic for Vision
             
             # A. Try Gemini
            if self.gemini_client:
                try:
                    gemini_contents = [full_prompt, image]
                    response = self.gemini_client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=gemini_contents
                    )
                    return response.text
                except:
                    pass
            
            # B. Try Groq
            if self.groq_client:
                try:
                    base64_image = self._encode_image(image)
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": user_text},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ]
                    completion = self.groq_client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=messages,
                        temperature=0.7,
                        max_tokens=1024,
                    )
                    return completion.choices[0].message.content
                except Exception as e:
                    return f"❌ Error processing image with Groq: {e}"
            
            return "⚠️ **عذراً،** ميزة تحليل الصور تحتاج إلى Gemini (الذي انتهت حصته) أو Groq.\nيرجى إضافة مفتاح Groq لتمكين تحليل الصور."

        else:
            # Logic for Text
            
            # A. Try Perplexity (Best quality/Search)
            if self.pplx_client:
                try:
                    messages = [
                        {"role": "system", "content": "Be helpful and concise."},
                        {"role": "user", "content": full_prompt}
                    ]
                    
                    # Using 'sonar' which is the standard model
                    response = self.pplx_client.chat.completions.create(
                        model="sonar",
                        messages=messages,
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    print(f"Perplexity Error: {e}")
                    pass

            # B. Try Gemini
            if self.gemini_client:
                try:
                    response = self.gemini_client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=[full_prompt]
                    )
                    return response.text
                except:
                    pass

            # C. Try Groq
            if self.groq_client:
                try:
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_text}
                    ]
                    completion = self.groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages,
                        temperature=0.7,
                        max_tokens=1024,
                    )
                    return completion.choices[0].message.content
                except Exception as e:
                    return f"❌ Error communicating with Groq: {e}"
        
        return "⚠️ **تنبيه:** لم يتم العثور على أي مفتاح API صالح (Perplexity, Gemini, Groq)."
