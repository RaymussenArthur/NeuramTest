# PDF Processing and News Search API

This project provides a FastAPI-based service for processing PDF resumes using LLMs and fetching industry-specific news.

## Features

- Task 1: Extracts text from PDF files and uses OpenRouter (Gemini 2.0 Flash) to generate a structured JSON summary (Name, Location, Work Experience).
- Task 2: Integrates Tavily API to search for relevant news articles based on a configurable area.

## Prerequisites

- Python 3.9+
- OpenRouter API Key
- Tavily API Key

## Setup Instructions

1. Clone the repository and enter the project folder.
2. Make .env
   ```
   OPENROUTER_API_KEY=your_key
   TAVILY_API_KEY=your_key
4. Install libraries
   ```pip install fastapi uvicorn pymupdf httpx python-dotenv```
5. Run
   ```python main.py```
