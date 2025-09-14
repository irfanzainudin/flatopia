"""
移民咨询专用Streamlit Web界面
"""
import streamlit as st
import asyncio
import os
from datetime import datetime
from typing import List, Dict, Any

# 页面Configuration
st.set_page_config(
    page_title="🌍 Global Immigration Advisor - 全球移民顾问",
    page_icon="🌍",
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
        background: linear-gradient(45deg, #1f77b4, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
    .immigration-badge {
        background: linear-gradient(45deg, #1f77b4, #4ecdc4);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .country-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .visa-type-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
if "chat_type" not in st.session_state:
    st.session_state.chat_type = "profile_collection"

def display_chat_message(role: str, content: str, timestamp: str = None, chat_type: str = "general"):
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
            "profile_collection": "📋",
            "immigration_analysis": "🔍",
            "visa_guide": "🛂",
            "pr_planning": "🏠",
            "country_comparison": "🌍",
            "general": "💬"
        }
        icon = type_icons.get(chat_type, "💬")
        
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>{icon} 移民顾问:</strong> {content}
            {f'<br><small>{timestamp}</small>' if timestamp else ''}
        </div>
        """, unsafe_allow_html=True)

def main():
    """主函数"""
    # 标题
    st.markdown('<h1 class="main-header">🌍 Global Immigration Advisor</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #666;">全球移民顾问 - 您的专业移民规划伙伴</h2>', unsafe_allow_html=True)
    
    # 特性展示
    st.markdown("""
    <div class="feature-card">
        <h3>🚀 专业移民咨询Service</h3>
        <p>基于最新移民政策和法律法规，为全球用户提供个性化的移民规划建议</p>
        <span class="immigration-badge">Powered by LangChain & Groq</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 移民咨询设置")
        
        # 聊天类型选择
        st.subheader("咨询模式")
        chat_type = st.selectbox(
            "选择咨询模式",
            [
                "profile_collection", 
                "immigration_analysis", 
                "visa_guide", 
                "pr_planning", 
                "country_comparison"
            ],
            index=[
                "profile_collection", 
                "immigration_analysis", 
                "visa_guide", 
                "pr_planning", 
                "country_comparison"
            ].index(st.session_state.chat_type),
            format_func=lambda x: {
                "profile_collection": "📋 信息收集",
                "immigration_analysis": "🔍 移民分析", 
                "visa_guide": "🛂 签证指南",
                "pr_planning": "🏠 永久居民规划",
                "country_comparison": "🌍 国家对比"
            }[x]
        )
        st.session_state.chat_type = chat_type
        
        # 用户档案显示
        st.subheader("📋 用户档案")
        if st.session_state.user_profile:
            for key, value in st.session_state.user_profile.items():
                st.write(f"**{key}**: {value}")
        else:
            st.info("暂无用户档案信息")
        
        # 快速操作
        st.subheader("🚀 快速操作")
        if st.button("开始信息收集"):
            st.session_state.chat_type = "profile_collection"
            st.rerun()
        
        if st.button("移民方案分析"):
            st.session_state.chat_type = "immigration_analysis"
            st.rerun()
        
        if st.button("国家对比"):
            st.session_state.chat_type = "country_comparison"
            st.rerun()
        
        # System状态
        st.subheader("🔧 System状态")
        if st.button("检查System状态"):
            try:
                from core.simple_langchain_config import GroqLLM
                from core.config import settings
                
                # 检查API密钥
                api_key_set = settings.groq_api_key != "your_groq_api_key_here"
                st.success("✅ API密钥已设置" if api_key_set else "❌ API密钥未设置")
                
                # 检查Model
                st.info(f"Model: llama-3.1-8b-instant")
                
                # 测试LLM连接
                if api_key_set:
                    try:
                        llm = GroqLLM(
                            groq_api_key=settings.groq_api_key,
                            model_name="llama-3.1-8b-instant"
                        )
                        test_response = llm("测试移民咨询System连接")
                        if "Error:" not in test_response:
                            st.success("✅ 移民咨询System连接正常")
                        else:
                            st.error(f"❌ System连接Failed: {test_response}")
                    except Exception as e:
                        st.error(f"❌ System连接Failed: {str(e)}")
                else:
                    st.warning("⚠️ 请先设置GROQ_API_KEY环境变量")
                    
            except Exception as e:
                st.error(f"❌ System检查Failed: {str(e)}")
        
        # 清空历史
        if st.button("清空对话历史"):
            st.session_state.messages = []
            st.rerun()
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 移民咨询对话")
        
        # 显示聊天历史
        for message in st.session_state.messages:
            display_chat_message(
                message["role"], 
                message["content"], 
                message.get("timestamp"),
                message.get("chat_type", "general")
            )
        
        # 聊天输入
        user_input = st.text_input(
            "请输入您的移民咨询问题...",
            key="user_input",
            placeholder="例如：我想了解加拿大的技术移民政策"
        )
        
        # 按钮组
        col_send, col_analysis, col_guide, col_pr = st.columns([1, 1, 1, 1])
        
        with col_send:
            if st.button("发送", type="primary") or user_input:
                if user_input:
                    # 发送消息
                    try:
                        from core.immigration_chat_manager import immigration_chat_manager
                        
                        # 检查API密钥
                        from core.config import settings
                        if settings.groq_api_key == "your_groq_api_key_here":
                            st.error("❌ 请先设置GROQ_API_KEY环境变量")
                            st.stop()
                        
                        # Processing移民咨询
                        with st.spinner("正在分析您的移民需求..."):
                            result = asyncio.run(immigration_chat_manager.chat(
                                user_input=user_input,
                                chat_type=st.session_state.chat_type
                            ))
                        
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
                            "content": result["answer"],
                            "timestamp": result["timestamp"],
                            "chat_type": result["chat_type"]
                        })
                        
                        # 更新用户档案
                        if "extracted_info" in result and result["extracted_info"]:
                            st.session_state.user_profile.update(result["extracted_info"])
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Processing移民咨询时出错: {str(e)}")
        
        with col_analysis:
            if st.button("移民分析"):
                if user_input:
                    try:
                        from core.immigration_chat_manager import immigration_chat_manager
                        
                        with st.spinner("正在分析移民方案..."):
                            result = asyncio.run(immigration_chat_manager.chat(
                                user_input=user_input,
                                chat_type="immigration_analysis"
                            ))
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**移民方案分析：**\n{result['answer']}",
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "chat_type": "immigration_analysis"
                        })
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ 移民分析Failed: {str(e)}")
        
        with col_guide:
            if st.button("签证指南"):
                if user_input:
                    try:
                        from core.immigration_chat_manager import immigration_chat_manager
                        
                        with st.spinner("正在生成签证指南..."):
                            result = asyncio.run(immigration_chat_manager.chat(
                                user_input=user_input,
                                chat_type="visa_guide"
                            ))
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**签证申请指南：**\n{result['answer']}",
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "chat_type": "visa_guide"
                        })
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ 签证指南生成Failed: {str(e)}")
        
        with col_pr:
            if st.button("PR规划"):
                if user_input:
                    try:
                        from core.immigration_chat_manager import immigration_chat_manager
                        
                        with st.spinner("正在制定永久居民规划..."):
                            result = asyncio.run(immigration_chat_manager.chat(
                                user_input=user_input,
                                chat_type="pr_planning"
                            ))
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"**永久居民规划：**\n{result['answer']}",
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "chat_type": "pr_planning"
                        })
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ PR规划Failed: {str(e)}")
    
    with col2:
        st.header("🌍 移民信息")
        
        # 支持的国家
        st.subheader("支持的国家")
        countries = [
            "🇨🇦 加拿大", "🇦🇺 澳大利亚", "🇳🇿 新西兰", 
            "🇺🇸 美国", "🇬🇧 英国", "🇩🇪 德国", "🇯🇵 日本"
        ]
        
        for country in countries:
            st.markdown(f"""
            <div class="country-card">
                <strong>{country}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # 签证类型
        st.subheader("签证类型")
        visa_types = [
            "💼 工作签证", "🎓 学习签证", 
            "🔧 技术移民", "💰 投资移民"
        ]
        
        for visa_type in visa_types:
            st.markdown(f"""
            <div class="visa-type-card">
                <strong>{visa_type}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Service说明
        st.subheader("Service说明")
        st.markdown("""
        **信息收集** 📋
        - 收集个人背景信息
        - 了解移民目标
        - 评估基本条件
        
        **移民分析** 🔍
        - 可行性评估
        - 路径规划
        - 风险分析
        
        **签证指南** 🛂
        - 申请条件
        - 流程步骤
        - 材料清单
        
        **PR规划** 🏠
        - 永久居民申请
        - 长期规划
        - 后续步骤
        """)
        
        # Use提示
        st.subheader("Use提示")
        st.markdown("""
        1. **开始咨询**：选择"信息收集"模式
        2. **详细描述**：提供您的具体情况
        3. **选择模式**：根据需要选择咨询模式
        4. **获取建议**：获得专业的移民建议
        """)


if __name__ == "__main__":
    main()
