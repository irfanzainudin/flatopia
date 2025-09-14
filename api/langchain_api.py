"""
Based on LangChain的APIInterface
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio

from ..core.langchain_chat_manager import langchain_chat_manager
from ..core.document_processor import document_processor
from ..core.langchain_config import langchain_config


# 创建FastAPIApplication
app = FastAPI(
    title="Flatopia LangChain API",
    description="Based on LangChain和Groq API的智能Q问答A机器人",
    version="2.0.0"
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
    chat_type: str = "basic"  # basic, rag, analysis, creative
    use_rag: bool = True


class DocumentRequest(BaseModel):
    documents: List[str]
    metadatas: Optional[List[Dict[str, Any]]] = None


class SearchRequest(BaseModel):
    query: str
    k: int = 5


class FileUploadRequest(BaseModel):
    file_paths: List[str]
    add_to_vectorstore: bool = True


# 响应Model
class ChatResponse(BaseModel):
    answer: str
    timestamp: str
    chat_type: str
    used_rag: bool
    success: bool
    source_documents: Optional[List[Dict[str, Any]]] = None
    chat_history: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


class DocumentResponse(BaseModel):
    success: bool
    documents_added: int
    message: str


class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total_found: int


# API路由
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎UseFlatopia LangChain API",
        "version": "2.0.0",
        "features": [
            "LangChain集成",
            "多种聊天模式",
            "文档Processing",
            "向量搜索",
            "Memory management"
        ],
        "docs": "/docs"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """聊天Interface"""
    try:
        result = await langchain_chat_manager.chat(
            user_input=request.message,
            use_rag=request.use_rag,
            chat_type=request.chat_type
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history")
async def get_chat_history():
    """获取聊天历史"""
    return {
        "history": langchain_chat_manager.get_conversation_history(),
        "summary": langchain_chat_manager.get_history_summary()
    }


@app.delete("/chat/history")
async def clear_chat_history():
    """清空聊天历史"""
    langchain_chat_manager.clear_history()
    return {"message": "聊天历史已清空"}


@app.post("/documents", response_model=DocumentResponse)
async def add_documents(request: DocumentRequest):
    """添加文档到知识库"""
    try:
        result = await langchain_chat_manager.add_documents(
            documents=request.documents,
            metadatas=request.metadatas
        )
        return DocumentResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/upload", response_model=DocumentResponse)
async def upload_documents(request: FileUploadRequest):
    """上传并Processing文档File"""
    try:
        result = document_processor.batch_process(
            file_paths=request.file_paths,
            add_to_vectorstore=request.add_to_vectorstore
        )
        
        return DocumentResponse(
            success=result["successful_files"] > 0,
            documents_added=result["processed_documents"],
            message=f"SuccessProcessing {result['successful_files']}/{result['total_files']} 个File"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """搜索文档"""
    try:
        results = await langchain_chat_manager.search_knowledge_base(
            query=request.query,
            k=request.k
        )
        return SearchResponse(
            results=results,
            total_found=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/knowledge/info")
async def get_knowledge_info():
    """获取知识库信息"""
    try:
        # 获取Vector storage信息
        collection = langchain_config.vectorstore._collection
        count = collection.count()
        
        return {
            "document_count": count,
            "collection_name": "knowledge_base",
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "chunk_size": langchain_config.text_splitter._chunk_size,
            "chunk_overlap": langchain_config.text_splitter._chunk_overlap
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models")
async def get_available_models():
    """获取可用Model列表"""
    return {
        "llm_models": [
            "llama3-8b-8192",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        ],
        "embedding_models": [
            "sentence-transformers/all-MiniLM-L6-v2",
            "sentence-transformers/all-mpnet-base-v2"
        ],
        "current_llm": langchain_config.llm.model_name,
        "current_embedding": "sentence-transformers/all-MiniLM-L6-v2"
    }


@app.get("/memory/info")
async def get_memory_info():
    """获取内存信息"""
    try:
        memory_info = langchain_config.get_memory_summary()
        return memory_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/analysis")
async def analyze_query(request: SearchRequest):
    """分析查询"""
    try:
        result = await langchain_chat_manager.chat(
            user_input=request.query,
            chat_type="analysis"
        )
        return {"analysis": result["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/creative")
async def get_creative_response(request: SearchRequest):
    """获取创意回复"""
    try:
        result = await langchain_chat_manager.chat(
            user_input=request.query,
            chat_type="creative"
        )
        return {"response": result["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def get_available_tools():
    """获取可用工具列表"""
    try:
        tools_info = []
        for tool in langchain_config.tools:
            tools_info.append({
                "name": tool.name,
                "description": tool.description
            })
        
        return {
            "tools": tools_info,
            "total_tools": len(tools_info)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent/run")
async def run_agent(request: SearchRequest):
    """运行代理"""
    try:
        result = langchain_config.get_agent_response(request.query)
        return {"response": result["answer"], "success": result["success"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
