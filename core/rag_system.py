"""
RAG（检索增强生成）System
"""
import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from .config import settings


class RAGSystem:
    """RAGSystem实现"""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
        self.top_k = settings.top_k
        
        # InitializeChromaDB
        self._init_vector_db()
    
    def _init_vector_db(self):
        """Initialize向量数据库"""
        try:
            # 确保数据目录存在
            os.makedirs(settings.vector_db_path, exist_ok=True)
            
            # InitializeChromaDB客户端
            self.chroma_client = chromadb.PersistentClient(
                path=settings.vector_db_path,
                settings=ChromaSettings(anonymized_telemetry=False)
            )
            
            # 获取或创建集合
            self.collection = self.chroma_client.get_or_create_collection(
                name="knowledge_base",
                metadata={"hnsw:space": "cosine"}
            )
            
        except Exception as e:
            print(f"Initialize向量数据库Failed: {e}")
            raise
    
    def add_documents(self, documents: List[str], metadatas: Optional[List[Dict]] = None):
        """
        添加文档到知识库
        
        Args:
            documents: 文档列表
            metadatas: 元数据列表（可选）
        """
        try:
            # 分块Processing文档
            chunks = self._chunk_documents(documents)
            
            # 生成嵌入
            embeddings = self.embedding_model.encode(chunks).tolist()
            
            # 准备元数据
            if metadatas is None:
                metadatas = [{"source": f"doc_{i}"} for i in range(len(chunks))]
            
            # 生成ID
            ids = [f"chunk_{i}" for i in range(len(chunks))]
            
            # 添加到集合
            self.collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"Success添加 {len(chunks)} 个文档块到知识库")
            
        except Exception as e:
            print(f"添加文档Failed: {e}")
            raise
    
    def _chunk_documents(self, documents: List[str]) -> List[str]:
        """
        将文档分块
        
        Args:
            documents: 原始文档列表
            
        Returns:
            分块后的文档列表
        """
        chunks = []
        
        for doc in documents:
            # 简单的分块策略（可以优化为更智能的分块）
            words = doc.split()
            
            for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
                chunk = " ".join(words[i:i + self.chunk_size])
                if chunk.strip():
                    chunks.append(chunk.strip())
        
        return chunks
    
    def search(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        搜索相关文档
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        try:
            # 生成查询嵌入
            query_embedding = self.embedding_model.encode([query]).tolist()[0]
            
            # 搜索
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k or self.top_k
            )
            
            # 格式化结果
            search_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    search_results.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else 0.0
                    })
            
            return search_results
            
        except Exception as e:
            print(f"搜索Failed: {e}")
            return []
    
    def get_context(self, query: str, top_k: Optional[int] = None) -> str:
        """
        获取查询的上下文
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            合并的上下文文本
        """
        results = self.search(query, top_k)
        
        if not results:
            return ""
        
        # 合并搜索结果
        context_parts = []
        for result in results:
            context_parts.append(result['content'])
        
        return "\n\n".join(context_parts)
    
    def get_collection_info(self) -> Dict[str, Any]:
        """获取集合信息"""
        try:
            count = self.collection.count()
            return {
                "document_count": count,
                "collection_name": self.collection.name
            }
        except Exception as e:
            return {"error": str(e)}


# 全局RAGSystem实例
rag_system = RAGSystem()
