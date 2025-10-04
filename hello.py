import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Available models that support 'generateContent':")

# List all models and filter for the ones that can generate content
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)