"""
Multi-API LLM Wrapper
Supports both Groq and OpenAI APIs with automatic failover
"""
import os
from typing import List, Dict, Any, Optional
from groq import Groq
import openai
from .config import settings


class MultiAPILLM:
    """Multi-API LLM wrapper with automatic failover"""
    
    def __init__(
        self,
        groq_api_key: str = None,
        openai_api_key: str = None,
        primary_api: str = "groq",
        model: str = None,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ):
        """
        Initialize Multi-API LLM
        
        Args:
            groq_api_key: Groq API key
            openai_api_key: OpenAI API key
            primary_api: Primary API to use ("groq" or "openai")
            model: Model name
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
        """
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY", settings.groq_api_key)
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY", "your-openai-api-key-here")
        self.primary_api = primary_api
        self.model = model or settings.default_model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # Initialize clients
        self.groq_client = None
        self.openai_client = None
        
        if self.groq_api_key and self.groq_api_key != "your-groq-api-key-here":
            try:
                self.groq_client = Groq(api_key=self.groq_api_key)
            except Exception as e:
                print(f"Failed to initialize Groq client: {e}")
        
        if self.openai_api_key and self.openai_api_key != "your-openai-api-key-here":
            try:
                self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
    
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Send chat completion request with automatic failover
        
        Args:
            messages: List of messages
            model: Model name (optional)
            **kwargs: Additional parameters
            
        Returns:
            Generated response text
        """
        model_name = model or self.model
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        temperature = kwargs.get("temperature", self.temperature)
        
        # Try primary API first
        if self.primary_api == "groq" and self.groq_client:
            try:
                return self._try_groq(messages, model_name, max_tokens, temperature)
            except Exception as e:
                print(f"Groq API failed: {e}")
                # Fallback to OpenAI
                if self.openai_client:
                    try:
                        return self._try_openai(messages, model_name, max_tokens, temperature)
                    except Exception as e2:
                        print(f"OpenAI API also failed: {e2}")
                        return f"Sorry, both APIs are currently unavailable. Error: {str(e)}"
                else:
                    return f"Sorry, Groq API failed and OpenAI is not configured. Error: {str(e)}"
        
        elif self.primary_api == "openai" and self.openai_client:
            try:
                return self._try_openai(messages, model_name, max_tokens, temperature)
            except Exception as e:
                print(f"OpenAI API failed: {e}")
                # Fallback to Groq
                if self.groq_client:
                    try:
                        return self._try_groq(messages, model_name, max_tokens, temperature)
                    except Exception as e2:
                        print(f"Groq API also failed: {e2}")
                        return f"Sorry, both APIs are currently unavailable. Error: {str(e)}"
                else:
                    return f"Sorry, OpenAI API failed and Groq is not configured. Error: {str(e)}"
        
        else:
            return "Sorry, no API clients are properly configured."
    
    def _try_groq(self, messages: List[Dict[str, str]], model: str, max_tokens: int, temperature: float) -> str:
        """Try Groq API"""
        response = self.groq_client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        if hasattr(response, 'choices') and response.choices:
            return response.choices[0].message.content
        else:
            return "Sorry, I couldn't generate a response."
    
    def _try_openai(self, messages: List[Dict[str, str]], model: str, max_tokens: int, temperature: float) -> str:
        """Try OpenAI API"""
        # Map Groq models to OpenAI models if needed
        if model.startswith("openai/"):
            model = model.replace("openai/", "")
        elif model in ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]:
            model = "gpt-3.5-turbo"  # Fallback to GPT-3.5 for unsupported models
        
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        if hasattr(response, 'choices') and response.choices:
            return response.choices[0].message.content
        else:
            return "Sorry, I couldn't generate a response."
    
    def get_available_models(self) -> List[str]:
        """Get available models"""
        models = []
        
        if self.groq_client:
            models.extend([
                "llama3-8b-8192",
                "llama3-70b-8192", 
                "mixtral-8x7b-32768",
                "gemma-7b-it"
            ])
        
        if self.openai_client:
            models.extend([
                "gpt-3.5-turbo",
                "gpt-4",
                "gpt-4-turbo-preview"
            ])
        
        return models
    
    def is_available(self) -> bool:
        """Check if any API is available"""
        return self.groq_client is not None or self.openai_client is not None
    
    def get_status(self) -> Dict[str, Any]:
        """Get API status"""
        return {
            "groq_available": self.groq_client is not None,
            "openai_available": self.openai_client is not None,
            "primary_api": self.primary_api,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
