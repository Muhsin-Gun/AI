from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import uvicorn

from ai_client import ai_client

app = FastAPI(title="TradePackage AI", description="Powerful AI Coding Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    text: str
    user_id: Optional[str] = "default"
    context: Optional[str] = None
    max_tokens: Optional[int] = 4096

class CodeRequest(BaseModel):
    code: str
    language: Optional[str] = "auto"

class GenerateRequest(BaseModel):
    description: str
    language: str

class ResearchRequest(BaseModel):
    topic: str

class WebsiteRequest(BaseModel):
    description: str

class ClearHistoryRequest(BaseModel):
    user_id: str

@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "TradePackage AI"}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    response = await ai_client.chat(req.text, req.user_id, req.context, req.max_tokens)
    return {"response": response}

@app.post("/api/analyze")
async def analyze_code(req: CodeRequest):
    response = await ai_client.analyze_code(req.code, req.language)
    return {"analysis": response}

@app.post("/api/generate")
async def generate_code(req: GenerateRequest):
    response = await ai_client.generate_code(req.description, req.language)
    return {"code": response}

@app.post("/api/research")
async def research(req: ResearchRequest):
    response = await ai_client.research(req.topic)
    return {"research": response}

@app.post("/api/website")
async def create_website(req: WebsiteRequest):
    response = await ai_client.create_website(req.description)
    return {"website": response}

@app.post("/api/clear-history")
async def clear_history(req: ClearHistoryRequest):
    ai_client.clear_history(req.user_id)
    return {"status": "cleared"}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
