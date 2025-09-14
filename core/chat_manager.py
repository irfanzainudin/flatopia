"""
Chat manager
"""
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from .groq_client import groq_client
from .rag_system import rag_system
from ..prompts.chat_prompts import ChatPrompts


class ChatManager:
    """Chat manager"""
    
    def __init__(self):
        self.conversation_history: List[Dict[str, Any]] = []
        self.max_history = 20  # 最大历史记录数
        
    async def chat(
        self, 
        user_input: str, 
        use_rag: bool = True,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process user input并生成回复
        
        Args:
            user_input: 用户输入
            use_rag: 是否UseRAG
            model: 指定Model
            
        Returns:
            包含回复和相关信息的字典
        """
        try:
            # 添加用户消息到历史
            self._add_message("user", user_input)
            
            # 构建消息列表
            messages = self._build_messages(user_input, use_rag)
            
            # 调用Groq API
            response = await groq_client.chat_completion(
                messages=messages,
                model=model
            )
            
            # 添加助手回复到历史
            self._add_message("assistant", response)
            
            return {
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "model": model or groq_client.model,
                "used_rag": use_rag,
                "success": True
            }
            
        except Exception as e:
            error_msg = f"Processing消息时出错: {str(e)}"
            self._add_message("assistant", error_msg)
            
            return {
                "response": error_msg,
                "timestamp": datetime.now().isoformat(),
                "model": model or groq_client.model,
                "used_rag": use_rag,
                "success": False,
                "error": str(e)
            }
    
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
    
    def _build_messages(self, user_input: str, use_rag: bool) -> List[Dict[str, str]]:
        """构建消息列表"""
        messages = []
        
        # 添加System提示词
        system_prompt = ChatPrompts.get_system_prompt()
        messages.append({"role": "system", "content": system_prompt})
        
        # 如果UseRAG，添加上下文
        if use_rag:
            context = rag_system.get_context(user_input)
            if context:
                rag_prompt = ChatPrompts.get_rag_prompt(user_input, context)
                messages.append({"role": "user", "content": rag_prompt})
            else:
                messages.append({"role": "user", "content": user_input})
        else:
            messages.append({"role": "user", "content": user_input})
        
        return messages
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """获取对话历史"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
    
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
            "last_message": self.conversation_history[-1] if self.conversation_history else None
        }
    
    async def analyze_query(self, query: str) -> str:
        """分析用户查询"""
        analysis_prompt = ChatPrompts.get_analysis_prompt(query)
        
        messages = [
            {"role": "system", "content": "你是一个专业的查询分析助手。"},
            {"role": "user", "content": analysis_prompt}
        ]
        
        response = await groq_client.chat_completion(messages)
        return response
    
    async def get_creative_response(self, topic: str) -> str:
        """获取创意回复"""
        creative_prompt = ChatPrompts.get_creative_prompt(topic)
        
        messages = [
            {"role": "system", "content": "你是一个创意助手，善于提供有趣和实用的内容。"},
            {"role": "user", "content": creative_prompt}
        ]
        
        response = await groq_client.chat_completion(messages)
        return response


# 全局Chat manager实例
chat_manager = ChatManager()
