"""
FastAPI主Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio

from ..core.chat_manager import chat_manager
from ..core.rag_system import rag_system
from ..core.groq_client import groq_client


# 创建FastAPIApplication
app = FastAPI(
    title="FlatopiaQ问答A机器人API",
    description="基于Groq API和RAG技术的智能Q问答A机器人",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求Model
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


# 响应Model
class ChatResponse(BaseModel):
    response: str
    timestamp: str
    model: str
    used_rag: bool
    success: bool
    error: Optional[str] = None


class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]


# API路由
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎UseFlatopiaQ问答A机器人API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """聊天Interface"""
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
    """获取聊天历史"""
    return {
        "history": chat_manager.get_conversation_history(),
        "summary": chat_manager.get_history_summary()
    }


@app.delete("/chat/history")
async def clear_chat_history():
    """清空聊天历史"""
    chat_manager.clear_history()
    return {"message": "聊天历史已清空"}


@app.post("/documents")
async def add_documents(request: DocumentRequest):
    """添加文档到知识库"""
    try:
        rag_system.add_documents(
            documents=request.documents,
            metadatas=request.metadatas
        )
        return {"message": f"Success添加 {len(request.documents)} 个文档"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """搜索文档"""
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
    """获取知识库信息"""
    try:
        info = rag_system.get_collection_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models")
async def get_available_models():
    """获取可用Model列表"""
    return {
        "models": groq_client.get_available_models(),
        "default": groq_client.model
    }


@app.post("/analyze")
async def analyze_query(request: SearchRequest):
    """分析查询"""
    try:
        analysis = await chat_manager.analyze_query(request.query)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/creative")
async def get_creative_response(request: SearchRequest):
    """获取创意回复"""
    try:
        response = await chat_manager.get_creative_response(request.query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
