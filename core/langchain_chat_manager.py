"""
Based on LangChain的Chat manager
"""
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from .langchain_config import langchain_config
from .document_processor import document_processor


class LangChainChatManager:
    """Based on LangChain的Chat manager"""
    
    def __init__(self):
        self.langchain_config = langchain_config
        self.document_processor = document_processor
        self.conversation_history = []
        self.max_history = 20
        
        # Initialize不同的链
        self._init_chains()
    
    def _init_chains(self):
        """Initialize各种链"""
        # 基础Conversation chain
        self._init_basic_chat_chain()
        
        # RAG链
        self._init_rag_chain()
        
        # 分析链
        self._init_analysis_chain()
        
        # 创意链
        self._init_creative_chain()
    
    def _init_basic_chat_chain(self):
        """Initialize基础Conversation chain"""
        template = """# Flatopia - 您的智能Q问答A助手

## 角色定义
你是Flatopia，一个Based on LangChain和Groq API的专业智能Q问答A助手。

### 🎯 核心特质
- **专业权威**：基于最新技术知识提供准确、专业的回答
- **智能理解**：深度理解用户意图，提供精准的解决方案
- **友好互动**：以温暖、专业的语调与用户交流
- **学习适应**：根据对话上下文调整回答风格和深度

### 💬 交互原则
1. **准确性优先**：确保信息准确，不确定时明确说明
2. **结构化回答**：Use清晰的逻辑结构和格式
3. **个性化Service**：根据用户水平调整回答复杂度
4. **持续学习**：从每次对话中学习和改进

### 🎨 回答风格
- Useemoji增强可读性
- 提供具体的代码示例和实现方案
- 给出实用的建议和最佳实践
- 主动提供相关资源和延伸阅读

## 对话历史
{chat_history}

## 用户问题
{question}

请根据用户的问题和对话历史，提供最有价值的回答。记住：你的目标是成为用户最信赖的技术顾问。"""

        prompt = PromptTemplate(
            input_variables=["chat_history", "question"],
            template=template
        )
        
        self.basic_chat_chain = LLMChain(
            llm=self.langchain_config.llm,
            prompt=prompt,
            memory=self.langchain_config.memory
        )
    
    def _init_rag_chain(self):
        """InitializeRAG链"""
        # UseLangChain的检索QA链
        self.rag_chain = self.langchain_config.retrieval_chain
    
    def _init_analysis_chain(self):
        """Initialize分析链"""
        template = """# 问题分析任务

## 用户问题
{question}

## 分析要求
请从以下角度深入分析这个问题：

### 1. 问题类型识别
- 技术问题 vs 业务问题 vs 概念问题
- 复杂度评估（简单/中等/复杂）
- 紧急程度评估

### 2. 关键信息提取
- 核心需求识别
- 约束条件分析
- Success标准定义

### 3. 解决思路
- 可能的解决方向
- 技术方案建议
- 实施步骤规划

### 4. 资源需求
- 所需技能和知识
- 工具和资源推荐
- 时间估算

### 5. 风险评估
- 潜在风险和挑战
- 风险缓解策略
- 备选方案

请提供详细、结构化的分析报告。"""

        prompt = PromptTemplate(
            input_variables=["question"],
            template=template
        )
        
        self.analysis_chain = LLMChain(
            llm=self.langchain_config.llm,
            prompt=prompt
        )
    
    def _init_creative_chain(self):
        """Initialize创意链"""
        template = """# 创意内容生成

## 主题
{topic}

## 创意要求
请围绕这个主题，提供富有创意和实用性的内容：

### 1. 独特视角
- 新颖的观点和角度
- 创新的思考方式
- 独特的解决方案

### 2. 实用建议
- 可操作的方法和技巧
- 具体的实施步骤
- 实用的工具推荐

### 3. 创意案例
- 有趣的例子和故事
- Success案例分享
- Failed经验总结

### 4. 启发思考
- 深度思考问题
- 相关话题延伸
- 未来发展趋势

请用生动、有趣的方式呈现内容，激发读者的思考和行动。"""

        prompt = PromptTemplate(
            input_variables=["topic"],
            template=template
        )
        
        self.creative_chain = LLMChain(
            llm=self.langchain_config.llm,
            prompt=prompt
        )
    
    async def chat(self, 
                   user_input: str, 
                   use_rag: bool = True,
                   chat_type: str = "basic") -> Dict[str, Any]:
        """
        Process user input并生成回复
        
        Args:
            user_input: 用户输入
            use_rag: 是否UseRAG
            chat_type: 聊天类型 (basic, rag, analysis, creative)
            
        Returns:
            包含回复和相关信息的字典
        """
        try:
            # 添加用户消息到历史
            self._add_message("user", user_input)
            
            # 根据类型选择Processing方式
            if chat_type == "rag" and use_rag:
                result = await self._handle_rag_chat(user_input)
            elif chat_type == "analysis":
                result = await self._handle_analysis_chat(user_input)
            elif chat_type == "creative":
                result = await self._handle_creative_chat(user_input)
            else:
                result = await self._handle_basic_chat(user_input)
            
            # 添加助手回复到历史
            self._add_message("assistant", result["answer"])
            
            return {
                **result,
                "timestamp": datetime.now().isoformat(),
                "chat_type": chat_type,
                "used_rag": use_rag,
                "success": True
            }
            
        except Exception as e:
            error_msg = f"Processing消息时出错: {str(e)}"
            self._add_message("assistant", error_msg)
            
            return {
                "answer": error_msg,
                "timestamp": datetime.now().isoformat(),
                "chat_type": chat_type,
                "used_rag": use_rag,
                "success": False,
                "error": str(e)
            }
    
    async def _handle_basic_chat(self, user_input: str) -> Dict[str, Any]:
        """Processing基础对话"""
        try:
            # 获取对话历史
            chat_history = self._get_chat_history_formatted()
            
            # Use基础Conversation chain
            result = self.basic_chat_chain.run(
                question=user_input,
                chat_history=chat_history
            )
            
            return {
                "answer": result,
                "source_documents": [],
                "chat_history": chat_history
            }
            
        except Exception as e:
            raise Exception(f"基础对话ProcessingFailed: {str(e)}")
    
    async def _handle_rag_chat(self, user_input: str) -> Dict[str, Any]:
        """ProcessingRAG对话"""
        try:
            # UseRAG链
            result = self.rag_chain({"query": user_input})
            
            return {
                "answer": result["result"],
                "source_documents": result.get("source_documents", []),
                "chat_history": self._get_chat_history_formatted()
            }
            
        except Exception as e:
            raise Exception(f"RAG对话ProcessingFailed: {str(e)}")
    
    async def _handle_analysis_chat(self, user_input: str) -> Dict[str, Any]:
        """Processing分析对话"""
        try:
            # Use分析链
            result = self.analysis_chain.run(question=user_input)
            
            return {
                "answer": result,
                "source_documents": [],
                "chat_history": self._get_chat_history_formatted()
            }
            
        except Exception as e:
            raise Exception(f"分析对话ProcessingFailed: {str(e)}")
    
    async def _handle_creative_chat(self, user_input: str) -> Dict[str, Any]:
        """Processing创意对话"""
        try:
            # Use创意链
            result = self.creative_chain.run(topic=user_input)
            
            return {
                "answer": result,
                "source_documents": [],
                "chat_history": self._get_chat_history_formatted()
            }
            
        except Exception as e:
            raise Exception(f"创意对话ProcessingFailed: {str(e)}")
    
    def _add_message(self, role: str, content: str):
        """添加消息到历史记录"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.conversation_history.append(message)
        
        # 保持历史记录在限制范围内
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def _get_chat_history_formatted(self) -> str:
        """获取格式化的对话历史"""
        if not self.conversation_history:
            return ""
        
        history_parts = []
        for msg in self.conversation_history[-10:]:  # 只保留最近10条
            role = "用户" if msg["role"] == "user" else "助手"
            history_parts.append(f"{role}: {msg['content']}")
        
        return "\n".join(history_parts)
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """获取对话历史"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        self.langchain_config.clear_memory()
    
    def get_history_summary(self) -> Dict[str, Any]:
        """获取对话历史摘要"""
        if not self.conversation_history:
            return {"message_count": 0, "last_message": None}
        
        user_messages = [msg for msg in self.conversation_history if msg["role"] == "user"]
        assistant_messages = [msg for msg in self.conversation_history if msg["role"] == "assistant"]
        
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "last_message": self.conversation_history[-1] if self.conversation_history else None,
            "memory_info": self.langchain_config.get_memory_summary()
        }
    
    async def add_documents(self, 
                           documents: List[str], 
                           metadatas: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """添加文档到知识库"""
        try:
            # 创建文档对象
            doc_objects = []
            for i, doc_text in enumerate(documents):
                metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
                doc = self.document_processor.create_document_from_text(doc_text, metadata)
                doc_objects.append(doc)
            
            # 分割文档
            split_docs = self.document_processor.split_documents(doc_objects)
            
            # Processing文档
            processed_docs = self.document_processor.process_documents(split_docs)
            
            # 添加到Vector storage
            success = self.langchain_config.add_documents(processed_docs)
            
            return {
                "success": success,
                "documents_added": len(processed_docs),
                "message": "文档添加Success" if success else "文档添加Failed"
            }
            
        except Exception as e:
            return {
                "success": False,
                "documents_added": 0,
                "message": f"添加文档时出错: {str(e)}"
            }
    
    async def search_knowledge_base(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """搜索知识库"""
        try:
            docs = self.langchain_config.search_documents(query, k)
            
            results = []
            for doc in docs:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "source": doc.metadata.get("source", "unknown")
                })
            
            return results
            
        except Exception as e:
            print(f"搜索知识库Failed: {e}")
            return []


# 全局LangChainChat manager实例
langchain_chat_manager = LangChainChatManager()
