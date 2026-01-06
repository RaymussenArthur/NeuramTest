import httpx
import os
import logging
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv() 

async def search_tavily_news(query: str):
    # Verify the Tavily API key exists in the environment
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Tavily API key is missing")

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": f"latest news in {query}",
        "search_depth": "smart",
        "topic": "news",
        "max_results": 5
    }

    async with httpx.AsyncClient() as client:
        try:
            # Send the search request to Tavily
            response = await client.post(url, json=payload, timeout=15.0)
            
            # Check if the API request was successful
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Tavily search failed")

            data = response.json()
            results = data.get("results", [])
            
            articles = []
            for result in results:
                # Map the API response to the required output format
                articles.append({
                    "title": result.get("title", "No Title"),
                    "summary": result.get("content", "No Description"),
                    "source": result.get("url", "N/A"),
                    "date": result.get("published_date", "N/A")
                })
            
            return articles
            
        except httpx.RequestError:
            # Handle connection or network-level errors
            raise HTTPException(status_code=503, detail="Tavily service is unreachable")
        except Exception as e:
            # Handle any other unexpected processing errors
            raise HTTPException(status_code=500, detail=f"News search error: {str(e)}")