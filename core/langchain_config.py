"""
LangChainConfiguration和Initialize
"""
import os
from typing import Optional, Dict, Any
from groq import Groq as GroqClient
from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.schema import BaseMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from .config import settings


class GroqLLM(LLM):
    """Groq LLM包装器"""
    
    def __init__(self, groq_api_key: str, model_name: str = "openai/gpt-oss-120b", **kwargs):
        super().__init__(**kwargs)
        self.client = GroqClient(api_key=groq_api_key)
        self.model_name = model_name
    
    @property
    def _llm_type(self) -> str:
        return "groq"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
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
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"model_name": self.model_name}


class LangChainConfig:
    """LangChainConfigurationManagement"""
    
    def __init__(self):
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.text_splitter = None
        self.memory = None
        self.retrieval_chain = None
        self.conversation_chain = None
        self.agent = None
        self.tools = []
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize所有组件"""
        # InitializeLLM
        self._init_llm()
        
        # Initialize嵌入Model
        self._init_embeddings()
        
        # InitializeText splitter
        self._init_text_splitter()
        
        # InitializeVector storage
        self._init_vectorstore()
        
        # Initialize内存
        self._init_memory()
        
        # Initialize工具
        self._init_tools()
        
        # Initialize链
        self._init_chains()
        
        # Initialize代理
        self._init_agent()
    
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
    
    def _init_memory(self):
        """InitializeMemory management"""
        # 对话窗口内存
        self.memory = ConversationBufferWindowMemory(
            k=10,  # 保留最近10轮对话
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # 可选：摘要内存（用于长对话）
        self.summary_memory = ConversationSummaryMemory(
            llm=self.llm,
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
    
    def _init_tools(self):
        """Initialize工具"""
        # Wikipedia工具
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        
        # 向量搜索工具
        vector_search_tool = Tool(
            name="vector_search",
            description="在知识库中搜索相关信息",
            func=self._vector_search
        )
        
        # 文档摘要工具
        document_summary_tool = Tool(
            name="document_summary",
            description="对文档进行摘要",
            func=self._document_summary
        )
        
        self.tools = [
            wikipedia,
            vector_search_tool,
            document_summary_tool
        ]
    
    def _init_chains(self):
        """Initialize链"""
        # 检索QA链
        self.retrieval_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": settings.top_k}
            ),
            return_source_documents=True
        )
        
        # 对话检索链
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": settings.top_k}
            ),
            memory=self.memory,
            return_source_documents=True,
            verbose=True
        )
    
    def _init_agent(self):
        """Initialize代理"""
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
    
    def _vector_search(self, query: str) -> str:
        """向量搜索工具"""
        try:
            docs = self.vectorstore.similarity_search(query, k=3)
            if docs:
                return "\n".join([doc.page_content for doc in docs])
            return "未找到相关信息"
        except Exception as e:
            return f"搜索出错: {str(e)}"
    
    def _document_summary(self, text: str) -> str:
        """文档摘要工具"""
        try:
            # 简单的摘要实现
            sentences = text.split('.')
            summary = '. '.join(sentences[:3]) + '.'
            return summary
        except Exception as e:
            return f"摘要生成出错: {str(e)}"
    
    def add_documents(self, documents: list, metadatas: Optional[list] = None):
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
    
    def search_documents(self, query: str, k: int = 5) -> list:
        """搜索文档"""
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return docs
        except Exception as e:
            print(f"搜索文档Failed: {e}")
            return []
    
    def get_retrieval_qa_response(self, query: str) -> Dict[str, Any]:
        """获取检索QA回答"""
        try:
            result = self.retrieval_chain({"query": query})
            return {
                "answer": result["result"],
                "source_documents": result["source_documents"],
                "success": True
            }
        except Exception as e:
            return {
                "answer": f"回答生成Failed: {str(e)}",
                "source_documents": [],
                "success": False
            }
    
    def get_conversation_response(self, query: str) -> Dict[str, Any]:
        """获取对话回答"""
        try:
            result = self.conversation_chain({"question": query})
            return {
                "answer": result["answer"],
                "source_documents": result.get("source_documents", []),
                "chat_history": result.get("chat_history", []),
                "success": True
            }
        except Exception as e:
            return {
                "answer": f"对话生成Failed: {str(e)}",
                "source_documents": [],
                "chat_history": [],
                "success": False
            }
    
    def get_agent_response(self, query: str) -> Dict[str, Any]:
        """获取代理回答"""
        try:
            result = self.agent.run(input=query)
            return {
                "answer": result,
                "success": True
            }
        except Exception as e:
            return {
                "answer": f"代理执行Failed: {str(e)}",
                "success": False
            }
    
    def clear_memory(self):
        """清空内存"""
        self.memory.clear()
        if hasattr(self, 'summary_memory'):
            self.summary_memory.clear()
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """获取内存摘要"""
        try:
            return {
                "memory_type": type(self.memory).__name__,
                "memory_variables": self.memory.memory_variables,
                "chat_history_length": len(self.memory.chat_memory.messages) if hasattr(self.memory, 'chat_memory') else 0
            }
        except Exception as e:
            return {"error": str(e)}


# 全局LangChainConfiguration实例
langchain_config = LangChainConfig()
