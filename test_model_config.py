"""
Test model configuration
"""
from core.simple_langchain_config import GroqLLM
from core.config import settings

def test_model_config():
    """Test model configuration"""
    print("🔧 Testing Model Configuration")
    print("=" * 40)
    
    print(f"Settings default_model: {settings.default_model}")
    
    # Create GroqLLM instance
    llm = GroqLLM(
        groq_api_key=settings.groq_api_key,
        model_name=settings.default_model
    )
    
    print(f"GroqLLM model_name: {llm.model_name}")
    
    # Test a simple call
    try:
        response = llm("Hello, what model are you?")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_model_config()