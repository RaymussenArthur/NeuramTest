import httpx
import os
import json
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

async def summarize_cv(text: str):
    # Check if the required API key is present in environment variables
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Configuration error: Missing API Key")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Define instructions for the LLM to extract specific fields
    prompt = f"""
    Extract the following from the CV text and return strictly in JSON format:
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
        try:
            # Execute the request with a timeout to prevent hanging
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            
            # Verify the external API returned a successful status code
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="LLM service error")

            result = response.json()
            
            # Safely navigate the response object to find the content
            if "choices" not in result or not result["choices"]:
                raise HTTPException(status_code=500, detail="Empty response from LLM")

            content = result["choices"][0]["message"]["content"]
            
            # Convert string content into a Python dictionary
            return json.loads(content)

        except httpx.RequestError:
            # Handle networking or connectivity issues
            raise HTTPException(status_code=503, detail="Service connectivity issue")
        except json.JSONDecodeError:
            # Handle cases where LLM output is not valid JSON
            raise HTTPException(status_code=500, detail="Invalid data format returned")
        except Exception as e:
            # Generic catch-all for unexpected runtime errors
            raise HTTPException(status_code=500, detail=f"Internal processing error: {str(e)}")