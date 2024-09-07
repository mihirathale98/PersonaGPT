## gemini api
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiAPI:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)

    
    def generate(self, input_prompt, temperature=0.7, top_p=0.95, top_k=40, max_tokens=2048):
        response = self.model.generate_content(input_prompt)
        return response.text
    



