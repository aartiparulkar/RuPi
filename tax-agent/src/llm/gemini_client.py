import os
import google.generativeai as genai

class GeminiClient:
    def __init__(self, model_name="gemini-1.5-flash"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
