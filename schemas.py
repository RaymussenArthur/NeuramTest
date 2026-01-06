from pydantic import BaseModel
from typing import List, Optional

# Task 1: Response dari LLM
class CVSummary(BaseModel):
    name: str
    location: str
    work_experience_summary: str

# Task 2: Format Berita
class NewsArticle(BaseModel):
    title: str
    summary: str
    source: str
    date: Optional[str] = "N/A"

class NewsResponse(BaseModel):
    area: str
    articles: List[NewsArticle]