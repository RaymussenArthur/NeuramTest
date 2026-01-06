import httpx
import os
import logging
from dotenv import load_dotenv

load_dotenv() 

async def search_tavily_news(query: str):
    api_key = os.getenv("TAVILY_API_KEY")
    
    # DEBUG: Cek apakah API Key terbaca
    if not api_key:
        print("CRITICAL ERROR: TAVILY_API_KEY tidak ditemukan di environment!")
        return []

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "smart",
        "topic": "news", # Gunakan topik news
        "max_results": 5
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=10.0)
            
            # Print untuk melihat status code (200, 401, atau 403?)
            print(f"Tavily Status Code: {response.status_code}")
            
            data = response.json()
            
            # Jika ada error dari Tavily (misal API Key salah)
            if response.status_code != 200:
                print(f"Tavily API Error: {data}")
                return []

            results = data.get("results", [])
            articles = []
            for result in results:
                articles.append({
                    "title": result.get("title", "No Title"),
                    "summary": result.get("content", "No Description"),
                    "source": result.get("url", "N/A"),
                    "date": result.get("published_date", "N/A")
                })
            return articles
            
        except Exception as e:
            print(f"Exception saat memanggil Tavily: {e}")
            return []