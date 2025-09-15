"""
Flatopia Q&A System - Streamlit Web Interface
"""
import streamlit as st
import asyncio
import os
from datetime import datetime
from typing import List, Dict, Any

# Page configuration
st.set_page_config(
    page_title="Flatopia - Your AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #1f77b4, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        max-width: 80%;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: auto;
    }
    .assistant-message {
        background-color: #f5f5f5;
        margin-right: auto;
    }
    .system-badge {
        background: linear-gradient(45deg, #1f77b4, #4ecdc4);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

def display_chat_message(role: str, content: str, timestamp: str = None):
    """Display chat message"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            {content}
            {f'<br><small>{timestamp}</small>' if timestamp else ''}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            {content}
            {f'<br><small>{timestamp}</small>' if timestamp else ''}
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main function"""
    # Title
    st.markdown('<h1 class="main-header">🤖 Flatopia</h1>', unsafe_allow_html=True)
    
    # Welcome message when no chat history
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border: 1px solid #dee2e6; border-radius: 15px; color: #495057; margin: 1rem 0 1rem 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); min-height: 400px; display: flex; flex-direction: column; justify-content: center;">
            <h2 style="margin-bottom: 1rem; color: #212529;">👋 Hello! I'm Flatopia</h2>
            <p style="font-size: 1.1rem; margin-bottom: 1.5rem; color: #6c757d;">Your AI Immigration & Study Abroad Advisor</p>
            <div style="background: rgba(108,117,125,0.1); padding: 1.2rem; border-radius: 10px; margin: 1.2rem 0; border: 1px solid #dee2e6;">
                <h4 style="margin-bottom: 0.8rem; color: #212529;">🎯 What I can help you with:</h4>
                <ul style="text-align: left; margin: 0; color: #495057; line-height: 1.5;">
                    <li>Immigration planning and visa guidance</li>
                    <li>Study abroad opportunities</li>
                    <li>Work migration advice</li>
                    <li>Country-specific recommendations</li>
                    <li>University and program suggestions</li>
                </ul>
            </div>
            <p style="font-size: 0.9rem; color: #6c757d;">Start by telling me your name and what you're looking for!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("💬 Chat Controls")
        
        # Clear history
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            # Reset chat manager
            from core.flatopia_chat_manager import flatopia_chat_manager
            flatopia_chat_manager.reset_conversation()
            st.rerun()
        
        # API Status
        st.subheader("🔧 API Status")
        if st.button("Check APIs"):
            try:
                from core.multi_api_llm import MultiAPILLM
                from llm_config import GROQ_API_KEY, OPENAI_API_KEY, PRIMARY_API, MODEL_NAME, MAX_TOKENS, TEMPERATURE
                
                # Create multi-API client
                llm = MultiAPILLM(
                    groq_api_key=GROQ_API_KEY,
                    openai_api_key=OPENAI_API_KEY,
                    primary_api=PRIMARY_API,
                    model=MODEL_NAME,
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE
                )
                
                # Display configuration information
                st.info(f"**Primary API**: {PRIMARY_API.upper()}")
                st.info(f"**Model**: {MODEL_NAME}")
                
                # Test API connections
                with st.spinner("Testing APIs..."):
                    test_results = llm.test_apis()
                    
                    # Display test results
                    if test_results.get("groq", False):
                        st.success("✅ Groq API - Available")
                    else:
                        st.error("❌ Groq API - Unavailable")
                    
                    if test_results.get("openai", False):
                        st.success("✅ OpenAI API - Available")
                    else:
                        st.error("❌ OpenAI API - Unavailable")
                    
                    # Test actual response
                    if any(test_results.values()):
                        test_response = llm("Test connection - respond with 'API test successful'")
                        if "Error:" not in test_response:
                            st.success("✅ System connection normal")
                        else:
                            st.error(f"❌ System connection failed: {test_response}")
                    else:
                        st.error("❌ All APIs unavailable")
                    
            except Exception as e:
                st.error(f"❌ System check failed: {str(e)}")
        
        # Usage tips
        st.subheader("💡 Usage Tips")
        st.markdown("""
        **How to use:**
        1. Start by telling me your age and basic info
        2. Share your family situation and profession
        3. Tell me your priorities for destination country
        4. I'll analyze your profile and suggest countries
        5. Ask detailed questions about specific countries
        
        **Example questions:**
        - What is artificial intelligence?
        - How does machine learning work?
        - Explain quantum computing
        - What are the benefits of renewable energy?
        """)
    
    # Main chat interface
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    
    with col2:
        # Display chat history
        for message in st.session_state.messages:
            display_chat_message(
                message["role"], 
                message["content"], 
                message.get("timestamp")
            )
    
    # Chat input - always visible
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize input key if not exists
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0
    
    user_input = st.text_input(
        "Ask me anything about immigration, study abroad, or work opportunities...",
        key=f"user_input_{st.session_state.input_key}",
        placeholder="e.g., Hi! I'm John, 25 years old from India, looking to study abroad..."
    )
    
    # Send button
    col1, col2 = st.columns([1, 4])
    
    with col1:
        send_clicked = st.button("Send", type="primary")
    
    with col2:
        pass
    
    # Process message when button is clicked or Enter is pressed
    if (send_clicked or user_input) and user_input.strip():
        # Check if this is a duplicate message
        if st.session_state.messages and st.session_state.messages[-1]["content"] == user_input:
            st.warning("Please wait for the previous response to complete.")
        else:
            # Send message
            try:
                from core.simple_langchain_config import GroqLLM
                from core.config import settings
                
                # Check API key
                if settings.groq_api_key == "your_groq_api_key_here":
                    st.error("❌ Please set GROQ_API_KEY environment variable first")
                    st.stop()
                
                # Process question
                with st.spinner("Flatopia is thinking..."):
                    from core.flatopia_chat_manager import flatopia_chat_manager
                    from core.multi_api_llm import MultiAPILLM
                    from llm_config import GROQ_API_KEY, OPENAI_API_KEY, PRIMARY_API, MODEL_NAME, MAX_TOKENS, TEMPERATURE
                    
                    # Use multi-API support
                    flatopia_chat_manager.llm = MultiAPILLM(
                        groq_api_key=GROQ_API_KEY,
                        openai_api_key=OPENAI_API_KEY,
                        primary_api=PRIMARY_API,
                        model=MODEL_NAME,
                        max_tokens=MAX_TOKENS,
                        temperature=TEMPERATURE
                    )
                    result = asyncio.run(flatopia_chat_manager.chat(user_input))
                    response = result["answer"]
                
                # Add user message
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_input,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
                # Add assistant reply
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
                # Clear the input by incrementing the key
                st.session_state.input_key += 1
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error processing question: {str(e)}")

if __name__ == "__main__":
    main()
