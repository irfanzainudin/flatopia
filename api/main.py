"""
FastAPI Main Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio

from ..core.chat_manager import chat_manager
from ..core.rag_system import rag_system
from ..core.groq_client import groq_client


# Create FastAPI Application
app = FastAPI(
    title="Flatopia Q&A Bot API",
    description="Intelligent Q&A Bot based on Groq API and RAG technology",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Models
class ChatRequest(BaseModel):
    message: str
    use_rag: bool = True
    model: Optional[str] = None


class DocumentRequest(BaseModel):
    documents: List[str]
    metadatas: Optional[List[Dict[str, Any]]] = None


class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = None


# Response Models
class ChatResponse(BaseModel):
    response: str
    timestamp: str
    model: str
    used_rag: bool
    success: bool
    error: Optional[str] = None


class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]


# API Routes
@app.get("/")
async def root():
    """Root path"""
    return {
        "message": "Welcome to Flatopia Q&A Bot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat Interface"""
    try:
        result = await chat_manager.chat(
            user_input=request.message,
            use_rag=request.use_rag,
            model=request.model
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history")
async def get_chat_history():
    """Get chat history"""
    return {
        "history": chat_manager.get_conversation_history(),
        "summary": chat_manager.get_history_summary()
    }


@app.delete("/chat/history")
async def clear_chat_history():
    """Clear chat history"""
    chat_manager.clear_history()
    return {"message": "Chat history cleared"}


@app.post("/documents")
async def add_documents(request: DocumentRequest):
    """Add documents to knowledge base"""
    try:
        rag_system.add_documents(
            documents=request.documents,
            metadatas=request.metadatas
        )
        return {"message": f"Successfully added {len(request.documents)} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """Search documents"""
    try:
        results = rag_system.search(
            query=request.query,
            top_k=request.top_k
        )
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/knowledge/info")
async def get_knowledge_info():
    """Get knowledge base info"""
    try:
        info = rag_system.get_collection_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models")
async def get_available_models():
    """Get available model list"""
    return {
        "models": groq_client.get_available_models(),
        "default": groq_client.model
    }


@app.post("/analyze")
async def analyze_query(request: SearchRequest):
    """Analyze query"""
    try:
        analysis = await chat_manager.analyze_query(request.query)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/creative")
async def get_creative_response(request: SearchRequest):
    """Get creative response"""
    try:
        response = await chat_manager.get_creative_response(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
