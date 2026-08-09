import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

class GeminiClient:

    def __init__(self):

        self.keys = [
            os.getenv("GEMINI_API_KEY1"),
            os.getenv("GEMINI_API_KEY2"),
            os.getenv("GEMINI_API_KEY3")
        ]

        self.keys = [k.strip() for k in self.keys if k and k.strip()]

    def generate(self, prompt):

        if not self.keys:
            return None

        for i, key in enumerate(self.keys, start=1):

            client = genai.Client(api_key=key)

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            return response.text

        return None