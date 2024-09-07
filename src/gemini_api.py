## gemini api
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiAPI:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model = genai.GenerativeModel(model_name)

    def generate(
        self, input_prompt, temperature=0.7, top_p=0.95, top_k=40, max_tokens=2048
    ):
        response = self.model.generate_content(
            input_prompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            },
            generation_config=genai.GenerationConfig(
                max_output_tokens=max_tokens,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature,
            ),
        )
        return response.text
