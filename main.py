from fastapi import FastAPI, UploadFile, File, HTTPException
from services.pdf_service import extract_text_from_pdf
from services.llm_service import summarize_cv
from services.news_service import search_tavily_news
from schemas import CVSummary, NewsResponse

app = FastAPI(title="Test")

# Task 1
@app.post("/process-cv", response_model=CVSummary)
async def process_cv(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        content = await file.read()
        raw_text = extract_text_from_pdf(content)
        summary = await summarize_cv(raw_text)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Task 2
@app.get("/search-news", response_model=NewsResponse)
async def get_news(area: str = "tech industry"):
    try:
        articles = await search_tavily_news(area)
        return {"area": area, "articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)