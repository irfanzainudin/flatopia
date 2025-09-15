"""
简化的LangChainConfiguration
"""
import os
from typing import Optional, Dict, Any, List
from groq import Groq as GroqClient
from langchain.llms.base import LLM
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from .config import settings


class GroqLLM:
    """Groq LLM包装器"""
    
    def __init__(self, groq_api_key: str, model_name: str = "openai/gpt-oss-120b"):
        self.client = GroqClient(api_key=groq_api_key)
        self.model_name = model_name
    
    def __call__(self, prompt: str) -> str:
        """Call LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


class SimpleLangChainConfig:
    """Simplified LangChain configuration management"""
    
    def __init__(self):
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.text_splitter = None
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all components"""
        # Initialize LLM
        self._init_llm()
        
        # Initialize embeddings model
        self._init_embeddings()
        
        # Initialize text splitter
        self._init_text_splitter()
        
        # Initialize vector store
        self._init_vectorstore()
    
    def _init_llm(self):
        """InitializeLLM"""
        self.llm = GroqLLM(
            groq_api_key=settings.groq_api_key,
            model_name=settings.default_model
        )
    
    def _init_embeddings(self):
        """Initialize嵌入Model"""
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
    
    def _init_text_splitter(self):
        """InitializeText splitter"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def _init_vectorstore(self):
        """InitializeVector storage"""
        self.vectorstore = Chroma(
            persist_directory=settings.vector_db_path,
            embedding_function=self.embeddings,
            collection_name="knowledge_base"
        )
    
    def add_documents(self, documents: List[Document], metadatas: Optional[List[Dict]] = None):
        """添加文档到Vector storage"""
        try:
            # 分割文档
            texts = self.text_splitter.split_documents(documents)
            
            # 添加到Vector storage
            self.vectorstore.add_documents(texts, metadatas)
            
            # 持久化
            self.vectorstore.persist()
            
            return True
        except Exception as e:
            print(f"添加文档Failed: {e}")
            return False
    
    def search_documents(self, query: str, k: int = 5) -> List[Document]:
        """搜索文档"""
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return docs
        except Exception as e:
            print(f"搜索文档Failed: {e}")
            return []
    
    def get_llm_response(self, prompt: str) -> str:
        """获取LLM回复"""
        try:
            return self.llm(prompt)
        except Exception as e:
            return f"LLM调用Failed: {str(e)}"
    
    def get_rag_response(self, query: str) -> Dict[str, Any]:
        """获取RAG回复"""
        try:
            # 搜索相关文档
            docs = self.search_documents(query, k=3)
            
            # 构建上下文
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # 构建prompt
            prompt = f"""基于以下上下文信息回答用户问题：

上下文信息：
{context}

用户问题：{query}

请根据上下文信息回答用户问题。如果上下文信息不足以回答问题，请说明并建议用户提供更多信息。"""
            
            # 获取LLM回复
            response = self.get_llm_response(prompt)
            
            return {
                "answer": response,
                "source_documents": docs,
                "success": True
            }
            
        except Exception as e:
            return {
                "answer": f"RAGProcessingFailed: {str(e)}",
                "source_documents": [],
                "success": False
            }


# 全局简化LangChainConfiguration实例
simple_langchain_config = SimpleLangChainConfig()
