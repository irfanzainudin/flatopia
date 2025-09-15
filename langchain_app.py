"""
Based on LangChain的Streamlit Web界面
"""
import streamlit as st
import asyncio
import requests
import json
from datetime import datetime
from typing import List, Dict, Any
import os

# 页面Configuration
st.set_page_config(
    page_title="Flatopia LangChain Q问答A机器人",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
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
    .status-success {
        color: #4caf50;
    }
    .status-error {
        color: #f44336;
    }
    .langchain-badge {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = "http://localhost:8000"
if "chat_type" not in st.session_state:
    st.session_state.chat_type = "basic"

def call_api(endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """调用APIInterface"""
    try:
        url = f"{st.session_state.api_base_url}{endpoint}"
        
        if data:
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API调用Failed: {str(e)}")
        return {"error": str(e)}

def display_chat_message(role: str, content: str, timestamp: str = None, chat_type: str = "basic"):
    """显示聊天消息"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>您:</strong> {content}
            {f'<br><small>{timestamp}</small>' if timestamp else ''}
        </div>
        """, unsafe_allow_html=True)
    else:
        # 根据聊天类型显示不同的图标
        type_icons = {
            "basic": "💬",
            "rag": "🔍",
            "analysis": "📊",
            "creative": "✨"
        }
        icon = type_icons.get(chat_type, "💬")
        
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>{icon} Flatopia:</strong> {content}
            {f'<br><small>{timestamp}</small>' if timestamp else ''}
        </div>
        """, unsafe_allow_html=True)

def main():
    """主函数"""
    # 标题
    st.markdown('<h1 class="main-header">🤖 Flatopia LangChain Q问答A机器人</h1>', unsafe_allow_html=True)
    
    # LangChain特性展示
    st.markdown("""
    <div class="feature-card">
        <h3>🚀 LangChain 增强功能</h3>
        <p>Based on LangChain框架，提供更强大的文档Processing、向量搜索和对话Management能力</p>
        <span class="langchain-badge">Powered by LangChain</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 设置")
        
        # APIConfiguration
        st.subheader("APIConfiguration")
        api_url = st.text_input("API地址", value=st.session_state.api_base_url)
        if api_url != st.session_state.api_base_url:
            st.session_state.api_base_url = api_url
        
        # 聊天类型选择
        st.subheader("聊天模式")
        chat_type = st.selectbox(
            "选择聊天模式",
            ["basic", "rag", "analysis", "creative"],
            index=["basic", "rag", "analysis", "creative"].index(st.session_state.chat_type),
            help="basic: 基础对话, rag: 检索增强, analysis: 问题分析, creative: 创意内容"
        )
        st.session_state.chat_type = chat_type
        
        # RAG设置
        st.subheader("RAG设置")
        use_rag = st.checkbox("启用RAG", value=True)
        
        # 知识库信息
        st.subheader("知识库信息")
        if st.button("刷新知识库信息"):
            info = call_api("/knowledge/info")
            if "error" not in info:
                st.success(f"文档数量: {info.get('document_count', 0)}")
                st.info(f"嵌入Model: {info.get('embedding_model', 'N/A')}")
            else:
                st.error("获取知识库信息Failed")
        
        # 内存信息
        st.subheader("Memory management")
        if st.button("查看内存状态"):
            memory_info = call_api("/memory/info")
            if "error" not in memory_info:
                st.success("内存状态正常")
                st.json(memory_info)
            else:
                st.error("获取内存信息Failed")
        
        # 清空历史
        if st.button("清空对话历史"):
            call_api("/chat/history", {"method": "DELETE"})
            st.session_state.messages = []
            st.rerun()
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 对话")
        
        # 显示聊天历史
        for message in st.session_state.messages:
            display_chat_message(
                message["role"], 
                message["content"], 
                message.get("timestamp"),
                message.get("chat_type", "basic")
            )
        
        # 聊天输入
        user_input = st.text_input(
            "输入您的问题...",
            key="user_input",
            placeholder="请输入您的问题，按Enter发送"
        )
        
        # 按钮组
        col_send, col_analysis, col_creative, col_agent = st.columns([1, 1, 1, 1])
        
        with col_send:
            if st.button("发送", type="primary") or user_input:
                if user_input:
                    # 发送消息
                    chat_data = {
                        "message": user_input,
                        "chat_type": st.session_state.chat_type,
                        "use_rag": use_rag
                    }
                    
                    with st.spinner("正在思考..."):
                        response = call_api("/chat", chat_data)
                    
                    if "error" not in response:
                        # 添加用户消息
                        st.session_state.messages.append({
                            "role": "user",
                            "content": user_input,
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "chat_type": st.session_state.chat_type
                        })
                        
                        # 添加助手回复
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response["answer"],
                            "timestamp": response["timestamp"],
                            "chat_type": response["chat_type"]
                        })
                        
                        st.rerun()
                    else:
                        st.error("发送Failed，请重试")
        
        with col_analysis:
            if st.button("分析问题"):
                if user_input:
                    with st.spinner("正在分析..."):
                        analysis_response = call_api("/chat/analysis", {"query": user_input})
                    
                    if "error" not in analysis_response:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**问题分析：**\n{analysis_response['analysis']}",
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "chat_type": "analysis"
                        })
                        st.rerun()
        
        with col_creative:
            if st.button("创意回复"):
                if user_input:
                    with st.spinner("正在生成创意内容..."):
                        creative_response = call_api("/chat/creative", {"query": user_input})
                    
                    if "error" not in creative_response:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**创意内容：**\n{creative_response['response']}",
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "chat_type": "creative"
                        })
                        st.rerun()
        
        with col_agent:
            if st.button("智能代理"):
                if user_input:
                    with st.spinner("智能代理正在Processing..."):
                        agent_response = call_api("/agent/run", {"query": user_input})
                    
                    if "error" not in agent_response:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**智能代理：**\n{agent_response['response']}",
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "chat_type": "agent"
                        })
                        st.rerun()
    
    with col2:
        st.header("📚 知识库Management")
        
        # 添加文档
        st.subheader("添加文档")
        doc_text = st.text_area(
            "输入文档内容",
            height=200,
            placeholder="输入要添加到知识库的文档内容..."
        )
        
        if st.button("添加到知识库"):
            if doc_text:
                doc_data = {
                    "documents": [doc_text],
                    "metadatas": [{"source": "manual_input", "timestamp": datetime.now().isoformat()}]
                }
                
                with st.spinner("正在添加文档..."):
                    result = call_api("/documents", doc_data)
                
                if "error" not in result:
                    st.success(f"文档添加Success！添加了 {result.get('documents_added', 0)} 个文档块")
                else:
                    st.error("添加文档Failed")
        
        # File上传
        st.subheader("上传File")
        uploaded_files = st.file_uploader(
            "选择File",
            type=['txt', 'pdf', 'docx'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            file_paths = []
            for uploaded_file in uploaded_files:
                # 保存File
                file_path = f"temp_{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_paths.append(file_path)
            
            if st.button("ProcessingFile"):
                with st.spinner("正在ProcessingFile..."):
                    result = call_api("/documents/upload", {
                        "file_paths": file_paths,
                        "add_to_vectorstore": True
                    })
                
                if "error" not in result:
                    st.success(result.get('message', 'FileProcessingSuccess'))
                else:
                    st.error("FileProcessingFailed")
                
                # 清理临时File
                for file_path in file_paths:
                    if os.path.exists(file_path):
                        os.remove(file_path)
        
        # 搜索文档
        st.subheader("搜索文档")
        search_query = st.text_input("搜索查询", placeholder="输入搜索关键词...")
        
        if st.button("搜索") and search_query:
            with st.spinner("正在搜索..."):
                search_response = call_api("/search", {"query": search_query, "k": 5})
            
            if "error" not in search_response:
                results = search_response.get("results", [])
                if results:
                    st.success(f"找到 {len(results)} 个相关结果")
                    for i, result in enumerate(results[:3]):  # 只显示前3个结果
                        with st.expander(f"结果 {i+1}"):
                            st.write(result["content"])
                            if result.get("metadata"):
                                st.caption(f"来源: {result['metadata']}")
                else:
                    st.info("未找到相关结果")
            else:
                st.error("搜索Failed")
        
        # System状态
        st.subheader("System状态")
        if st.button("检查状态"):
            status = call_api("/")
            if "error" not in status:
                st.success("✅ API连接正常")
                st.info(f"版本: {status.get('version', 'Unknown')}")
                st.json(status.get("features", []))
            else:
                st.error("❌ API连接Failed")

if __name__ == "__main__":
    main()
