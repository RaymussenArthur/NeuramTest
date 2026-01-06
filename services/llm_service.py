import httpx
import os
import json
from dotenv import load_dotenv

load_dotenv()

async def summarize_cv(text: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Extract the following information from this CV text and return it in JSON format:
    - name
    - location
    - work_experience_summary
    CV Text: {text}
    """

    payload = {
        "model": "google/gemini-2.0-flash-001",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": { "type": "json_object" }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=30.0)
        result = response.json()
        return json.loads(result['choices'][0]['message']['content'])