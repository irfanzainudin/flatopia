"""
Groq API客户端
"""
import asyncio
from typing import List, Dict, Any, Optional
from groq import Groq
from .config import settings


class GroqClient:
    """Groq API客户端封装"""
    
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.default_model
        self.max_tokens = settings.max_tokens
        self.temperature = settings.temperature
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        发送聊天完成请求
        
        Args:
            messages: 消息列表
            model: Model名称（可选）
            **kwargs: 其他参数
            
        Returns:
            生成的回复文本
        """
        try:
            # Use指定Model或默认Model
            model_name = model or self.model
            
            # 构建请求参数
            request_params = {
                "model": model_name,
                "messages": messages,
                "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                "temperature": kwargs.get("temperature", self.temperature),
                "stream": kwargs.get("stream", False)
            }
            
            # 发送请求
            response = self.client.chat.completions.create(**request_params)
            
            # 提取回复内容
            if hasattr(response, 'choices') and response.choices:
                return response.choices[0].message.content
            else:
                return "抱歉，我无法生成回复。"
                
        except Exception as e:
            print(f"Groq APIError: {e}")
            return f"抱歉，Processing您的请求时出现了Error: {str(e)}"
    
    def get_available_models(self) -> List[str]:
        """获取可用的Model列表"""
        return [
            "llama-3.1-8b-instant",
            "llama-3.1-70b-versatile", 
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        ]
    
    def validate_model(self, model: str) -> bool:
        """验证Model是否可用"""
        return model in self.get_available_models()


# 全局客户端实例
groq_client = GroqClient()
