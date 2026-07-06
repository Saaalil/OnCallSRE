import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Ensure we use the API key from the environment
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

def ask_gemini(system_instruction: str, prompt: str) -> str:
    """
    Helper function to query Gemini 2.5 Pro.
    """
    if not client:
        return "[MOCK RESPONSE - API KEY MISSING] " + prompt
        
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=f"System Instruction: {system_instruction}\n\nUser Input: {prompt}"
    )
    return response.text
