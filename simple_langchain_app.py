"""
简化的LangChain Streamlit Web界面
"""
import streamlit as st
import asyncio
import os
from datetime import datetime
from typing import List, Dict, Any

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
if "chat_type" not in st.session_state:
    st.session_state.chat_type = "basic"

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
        <h3>🚀 LangChain Simplified version</h3>
        <p>Based on LangChain框架和Groq API的智能Q问答A助手，提供基础对话功能</p>
        <span class="langchain-badge">Powered by LangChain</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 设置")
        
        # 聊天类型选择
        st.subheader("聊天模式")
        chat_type = st.selectbox(
            "选择聊天模式",
            ["basic", "rag", "analysis", "creative"],
            index=["basic", "rag", "analysis", "creative"].index(st.session_state.chat_type),
            help="basic: 基础对话, rag: 检索增强, analysis: 问题分析, creative: 创意内容"
        )
        st.session_state.chat_type = chat_type
        
        # System状态
        st.subheader("System状态")
        if st.button("检查状态"):
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
                        test_response = llm("测试连接")
                        if "Error:" not in test_response:
                            st.success("✅ LLM连接正常")
                        else:
                            st.error(f"❌ LLM连接Failed: {test_response}")
                    except Exception as e:
                        st.error(f"❌ LLM连接Failed: {str(e)}")
                else:
                    st.warning("⚠️ 请先设置API密钥")
                    
            except Exception as e:
                st.error(f"❌ System检查Failed: {str(e)}")
        
        # 清空历史
        if st.button("清空对话历史"):
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
        col_send, col_analysis, col_creative = st.columns([1, 1, 1])
        
        with col_send:
            if st.button("发送", type="primary") or user_input:
                if user_input:
                    # 发送消息
                    try:
                        from core.simple_langchain_config import GroqLLM
                        from core.config import settings
                        
                        # 检查API密钥
                        if settings.groq_api_key == "your_groq_api_key_here":
                            st.error("❌ 请先设置GROQ_API_KEY环境变量")
                            st.stop()
                        
                        # 创建LLM实例
                        llm = GroqLLM(
                            groq_api_key=settings.groq_api_key,
                            model_name="llama-3.1-8b-instant"
                        )
                        
                        # 添加用户消息
                        st.session_state.messages.append({
                            "role": "user",
                            "content": user_input,
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "chat_type": st.session_state.chat_type
                        })
                        
                        # 根据聊天类型生成回复
                        with st.spinner("正在思考..."):
                            if st.session_state.chat_type == "basic":
                                # 基础对话
                                chat_history = "\n".join([
                                    f"{'用户' if msg['role'] == 'user' else '助手'}: {msg['content']}"
                                    for msg in st.session_state.messages[-10:]
                                ])
                                
                                prompt = f"""# Flatopia - 您的智能Q问答A助手

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
{user_input}

请根据用户的问题和对话历史，提供最有价值的回答。记住：你的目标是成为用户最信赖的技术顾问。"""
                                
                                response = llm(prompt)
                                
                            elif st.session_state.chat_type == "analysis":
                                # 分析对话
                                analysis_prompt = f"""# 问题分析任务

## 用户问题
{user_input}

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
                                
                                response = llm(analysis_prompt)
                                
                            elif st.session_state.chat_type == "creative":
                                # 创意对话
                                creative_prompt = f"""# 创意内容生成

## 主题
{user_input}

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
                                
                                response = llm(creative_prompt)
                            
                            else:
                                # RAG对话（简化版）
                                response = llm(f"基于你的知识回答这个问题：{user_input}")
                        
                        # 添加助手回复
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "chat_type": st.session_state.chat_type
                        })
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Processing消息时出错: {str(e)}")
        
        with col_analysis:
            if st.button("分析问题"):
                if user_input:
                    try:
                        from core.simple_langchain_config import GroqLLM
                        from core.config import settings
                        
                        if settings.groq_api_key == "your_groq_api_key_here":
                            st.error("❌ 请先设置GROQ_API_KEY环境变量")
                            return
                        
                        llm = GroqLLM(
                            groq_api_key=settings.groq_api_key,
                            model_name="llama-3.1-8b-instant"
                        )
                        
                        with st.spinner("正在分析..."):
                            analysis_prompt = f"""# 问题分析任务

## 用户问题
{user_input}

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
                            
                            response = llm(analysis_prompt)
                            
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": f"**问题分析：**\n{response}",
                                "timestamp": datetime.now().strftime("%H:%M:%S"),
                                "chat_type": "analysis"
                            })
                            
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"❌ 分析Failed: {str(e)}")
        
        with col_creative:
            if st.button("创意回复"):
                if user_input:
                    try:
                        from core.simple_langchain_config import GroqLLM
                        from core.config import settings
                        
                        if settings.groq_api_key == "your_groq_api_key_here":
                            st.error("❌ 请先设置GROQ_API_KEY环境变量")
                            return
                        
                        llm = GroqLLM(
                            groq_api_key=settings.groq_api_key,
                            model_name="llama-3.1-8b-instant"
                        )
                        
                        with st.spinner("正在生成创意内容..."):
                            creative_prompt = f"""# 创意内容生成

## 主题
{user_input}

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
                            
                            response = llm(creative_prompt)
                            
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": f"**创意内容：**\n{response}",
                                "timestamp": datetime.now().strftime("%H:%M:%S"),
                                "chat_type": "creative"
                            })
                            
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"❌ 创意生成Failed: {str(e)}")
    
    with col2:
        st.header("📚 System信息")
        
        # 功能说明
        st.subheader("功能说明")
        st.markdown("""
        **基础对话** 💬
        - 智能Q问答A
        - 上下文理解
        - 专业建议
        
        **问题分析** 📊
        - 深度分析
        - 结构化报告
        - 风险评估
        
        **创意内容** ✨
        - 创新思维
        - 实用建议
        - 启发思考
        """)
        
        # Usage instructions
        st.subheader("Usage instructions")
        st.markdown("""
        1. **设置API密钥**：在侧边栏检查System状态
        2. **选择模式**：选择适合的聊天模式
        3. **输入问题**：在输入框中输入您的问题
        4. **获取回答**：点击发送或Use特殊功能按钮
        """)
        
        # 技术信息
        st.subheader("技术信息")
        st.markdown("""
        - **框架**：LangChain + Streamlit
        - **LLM**：Groq API (llama-3.1-8b-instant)
        - **版本**：简化版 v1.0
        - **状态**：基础功能可用
        """)


if __name__ == "__main__":
    main()
