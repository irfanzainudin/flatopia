"""
简化的anghain tramlit b界面
"""
import stramlit as st
import asyncio
import os
rom dattim import dattim
rom typing import ist, ict, ny

# 页面onigration
st.st_pag_conig(
    pag_titl"latopia anghain 问答机器人",
    pag_icon"🤖",
    layot"wid",
    initial_sidbar_stat"xpandd"
)

# 自定义
st.markdown("""
styl
    .main-hadr {
        ont-siz .rm
        color #b
        txt-align cntr
        margin-bottom rm
    }
    .atr-card {
        backgrond-color #a
        padding rm
        bordr-radis .rm
        margin .rm 
        bordr-lt px solid #b
    }
    .chat-mssag {
        padding rm
        bordr-radis .rm
        margin-bottom rm
        max-width %
    }
    .sr-mssag {
        backgrond-color #d
        margin-lt ato
    }
    .assistant-mssag {
        backgrond-color #
        margin-right ato
    }
    .stats-sccss {
        color #ca
    }
    .stats-rror {
        color #
    }
    .langchain-badg {
        backgrond linar-gradint(dg, #bb, #cdc)
        color whit
        padding .rm .rm
        bordr-radis rm
        ont-siz .rm
        ont-wight bold
    }
/styl
""", nsa_allow_htmlr)

# nitializ会话状态
i "mssags" not in st.sssion_stat
    st.sssion_stat.mssags  ]
i "chat_typ" not in st.sssion_stat
    st.sssion_stat.chat_typ  "basic"

d display_chat_mssag(rol str, contnt str, timstamp str  on, chat_typ str  "basic")
    """显示聊天消息"""
    i rol  "sr"
        st.markdown("""
        div class"chat-mssag sr-mssag"
            strong您/strong {contnt}
            {'brsmall{timstamp}/small' i timstamp ls ''}
        /div
        """, nsa_allow_htmlr)
    ls
        # 根据聊天类型显示不同的图标
        typ_icons  {
            "basic" "💬",
            "rag" "🔍",
            "analysis" "📊",
            "crativ" "✨"
        }
        icon  typ_icons.gt(chat_typ, "💬")
        
        st.markdown("""
        div class"chat-mssag assistant-mssag"
            strong{icon} latopia/strong {contnt}
            {'brsmall{timstamp}/small' i timstamp ls ''}
        /div
        """, nsa_allow_htmlr)

d main()
    """主函数"""
    # 标题
    st.markdown('h class"main-hadr"🤖 latopia anghain 问答机器人/h', nsa_allow_htmlr)
    
    # anghain特性展示
    st.markdown("""
    div class"atr-card"
        h🚀 anghain impliid vrsion/h
        pasd on anghain框架和roq 的智能问答助手，提供基础对话功能/p
        span class"langchain-badg"owrd by anghain/span
    /div
    """, nsa_allow_htmlr)
    
    # 侧边栏
    with st.sidbar
        st.hadr("⚙️ 设置")
        
        # 聊天类型选择
        st.sbhadr("聊天模式")
        chat_typ  st.slctbox(
            "选择聊天模式",
            "basic", "rag", "analysis", "crativ"],
            indx"basic", "rag", "analysis", "crativ"].indx(st.sssion_stat.chat_typ),
            hlp"basic 基础对话, rag 检索增强, analysis 问题分析, crativ 创意内容"
        )
        st.sssion_stat.chat_typ  chat_typ
        
        # ystm状态
        st.sbhadr("ystm状态")
        i st.btton("检查状态")
            try
                rom cor.simpl_langchain_conig import roq
                rom cor.conig import sttings
                
                # 检查密钥
                api_ky_st  sttings.groq_api_ky ! "yor_groq_api_ky_hr"
                st.sccss("✅ 密钥已设置" i api_ky_st ls "❌ 密钥未设置")
                
                # 检查odl
                st.ino("odl llama-.-b-instant")
                
                # 测试连接
                i api_ky_st
                    try
                        llm  roq(
                            groq_api_kysttings.groq_api_ky,
                            modl_nam"llama-.-b-instant"
                        )
                        tst_rspons  llm("测试连接")
                        i "rror" not in tst_rspons
                            st.sccss("✅ 连接正常")
                        ls
                            st.rror("❌ 连接aild {tst_rspons}")
                    xcpt xcption as 
                        st.rror("❌ 连接aild {str()}")
                ls
                    st.warning("⚠️ 请先设置密钥")
                    
            xcpt xcption as 
                st.rror("❌ ystm检查aild {str()}")
        
        # 清空历史
        i st.btton("清空对话历史")
            st.sssion_stat.mssags  ]
            st.rrn()
    
    # 主界面
    col, col  st.colmns(, ])
    
    with col
        st.hadr("💬 对话")
        
        # 显示聊天历史
        or mssag in st.sssion_stat.mssags
            display_chat_mssag(
                mssag"rol"], 
                mssag"contnt"], 
                mssag.gt("timstamp"),
                mssag.gt("chat_typ", "basic")
            )
        
        # 聊天输入
        sr_inpt  st.txt_inpt(
            "输入您的问题...",
            ky"sr_inpt",
            placholdr"请输入您的问题，按ntr发送"
        )
        
        # 按钮组
        col_snd, col_analysis, col_crativ  st.colmns(, , ])
        
        with col_snd
            i st.btton("发送", typ"primary") or sr_inpt
                i sr_inpt
                    # 发送消息
                    try
                        rom cor.simpl_langchain_conig import roq
                        rom cor.conig import sttings
                        
                        # 检查密钥
                        i sttings.groq_api_ky  "yor_groq_api_ky_hr"
                            st.rror("❌ 请先设置__环境变量")
                            st.stop()
                        
                        # 创建实例
                        llm  roq(
                            groq_api_kysttings.groq_api_ky,
                            modl_nam"llama-.-b-instant"
                        )
                        
                        # 添加用户消息
                        st.sssion_stat.mssags.appnd({
                            "rol" "sr",
                            "contnt" sr_inpt,
                            "timstamp" dattim.now().strtim("%%%"),
                            "chat_typ" st.sssion_stat.chat_typ
                        })
                        
                        # 根据聊天类型生成回复
                        with st.spinnr("正在思考...")
                            i st.sssion_stat.chat_typ  "basic"
                                # 基础对话
                                chat_history  "n".join(
                                    "{'用户' i msg'rol']  'sr' ls '助手'} {msg'contnt']}"
                                    or msg in st.sssion_stat.mssags-]
                                ])
                                
                                prompt  """# latopia - 您的智能问答助手

## 角色定义
你是latopia，一个asd on anghain和roq 的专业智能问答助手。

### 🎯 核心特质
- **专业权威**：基于最新技术知识提供准确、专业的回答
- **智能理解**：深度理解用户意图，提供精准的解决方案
- **友好互动**：以温暖、专业的语调与用户交流
- **学习适应**：根据对话上下文调整回答风格和深度

### 💬 交互原则
. **准确性优先**：确保信息准确，不确定时明确说明
. **结构化回答**：s清晰的逻辑结构和格式
. **个性化rvic**：根据用户水平调整回答复杂度
. **持续学习**：从每次对话中学习和改进

### 🎨 回答风格
- smoji增强可读性
- 提供具体的代码示例和实现方案
- 给出实用的建议和最佳实践
- 主动提供相关资源和延伸阅读

## 对话历史
{chat_history}

## 用户问题
{sr_inpt}

请根据用户的问题和对话历史，提供最有价值的回答。记住：你的目标是成为用户最信赖的技术顾问。"""
                                
                                rspons  llm(prompt)
                                
                            li st.sssion_stat.chat_typ  "analysis"
                                # 分析对话
                                analysis_prompt  """# 问题分析任务

## 用户问题
{sr_inpt}

## 分析要求
请从以下角度深入分析这个问题：

### . 问题类型识别
- 技术问题 vs 业务问题 vs 概念问题
- 复杂度评估（简单/中等/复杂）
- 紧急程度评估

### . 关键信息提取
- 核心需求识别
- 约束条件分析
- ccss标准定义

### . 解决思路
- 可能的解决方向
- 技术方案建议
- 实施步骤规划

### . 资源需求
- 所需技能和知识
- 工具和资源推荐
- 时间估算

### . 风险评估
- 潜在风险和挑战
- 风险缓解策略
- 备选方案

请提供详细、结构化的分析报告。"""
                                
                                rspons  llm(analysis_prompt)
                                
                            li st.sssion_stat.chat_typ  "crativ"
                                # 创意对话
                                crativ_prompt  """# 创意内容生成

## 主题
{sr_inpt}

## 创意要求
请围绕这个主题，提供富有创意和实用性的内容：

### . 独特视角
- 新颖的观点和角度
- 创新的思考方式
- 独特的解决方案

### . 实用建议
- 可操作的方法和技巧
- 具体的实施步骤
- 实用的工具推荐

### . 创意案例
- 有趣的例子和故事
- ccss案例分享
- aild经验总结

### . 启发思考
- 深度思考问题
- 相关话题延伸
- 未来发展趋势

请用生动、有趣的方式呈现内容，激发读者的思考和行动。"""
                                
                                rspons  llm(crativ_prompt)
                            
                            ls
                                # 对话（简化版）
                                rspons  llm("基于你的知识回答这个问题：{sr_inpt}")
                        
                        # 添加助手回复
                        st.sssion_stat.mssags.appnd({
                            "rol" "assistant",
                            "contnt" rspons,
                            "timstamp" dattim.now().strtim("%%%"),
                            "chat_typ" st.sssion_stat.chat_typ
                        })
                        
                        st.rrn()
                        
                    xcpt xcption as 
                        st.rror("❌ rocssing消息时出错 {str()}")
        
        with col_analysis
            i st.btton("分析问题")
                i sr_inpt
                    try
                        rom cor.simpl_langchain_conig import roq
                        rom cor.conig import sttings
                        
                        i sttings.groq_api_ky  "yor_groq_api_ky_hr"
                            st.rror("❌ 请先设置__环境变量")
                            rtrn
                        
                        llm  roq(
                            groq_api_kysttings.groq_api_ky,
                            modl_nam"llama-.-b-instant"
                        )
                        
                        with st.spinnr("正在分析...")
                            analysis_prompt  """# 问题分析任务

## 用户问题
{sr_inpt}

## 分析要求
请从以下角度深入分析这个问题：

### . 问题类型识别
- 技术问题 vs 业务问题 vs 概念问题
- 复杂度评估（简单/中等/复杂）
- 紧急程度评估

### . 关键信息提取
- 核心需求识别
- 约束条件分析
- ccss标准定义

### . 解决思路
- 可能的解决方向
- 技术方案建议
- 实施步骤规划

### . 资源需求
- 所需技能和知识
- 工具和资源推荐
- 时间估算

### . 风险评估
- 潜在风险和挑战
- 风险缓解策略
- 备选方案

请提供详细、结构化的分析报告。"""
                            
                            rspons  llm(analysis_prompt)
                            
                            st.sssion_stat.mssags.appnd({
                                "rol" "assistant",
                                "contnt" "**问题分析：**n{rspons}",
                                "timstamp" dattim.now().strtim("%%%"),
                                "chat_typ" "analysis"
                            })
                            
                            st.rrn()
                            
                    xcpt xcption as 
                        st.rror("❌ 分析aild {str()}")
        
        with col_crativ
            i st.btton("创意回复")
                i sr_inpt
                    try
                        rom cor.simpl_langchain_conig import roq
                        rom cor.conig import sttings
                        
                        i sttings.groq_api_ky  "yor_groq_api_ky_hr"
                            st.rror("❌ 请先设置__环境变量")
                            rtrn
                        
                        llm  roq(
                            groq_api_kysttings.groq_api_ky,
                            modl_nam"llama-.-b-instant"
                        )
                        
                        with st.spinnr("正在生成创意内容...")
                            crativ_prompt  """# 创意内容生成

## 主题
{sr_inpt}

## 创意要求
请围绕这个主题，提供富有创意和实用性的内容：

### . 独特视角
- 新颖的观点和角度
- 创新的思考方式
- 独特的解决方案

### . 实用建议
- 可操作的方法和技巧
- 具体的实施步骤
- 实用的工具推荐

### . 创意案例
- 有趣的例子和故事
- ccss案例分享
- aild经验总结

### . 启发思考
- 深度思考问题
- 相关话题延伸
- 未来发展趋势

请用生动、有趣的方式呈现内容，激发读者的思考和行动。"""
                            
                            rspons  llm(crativ_prompt)
                            
                            st.sssion_stat.mssags.appnd({
                                "rol" "assistant",
                                "contnt" "**创意内容：**n{rspons}",
                                "timstamp" dattim.now().strtim("%%%"),
                                "chat_typ" "crativ"
                            })
                            
                            st.rrn()
                            
                    xcpt xcption as 
                        st.rror("❌ 创意生成aild {str()}")
    
    with col
        st.hadr("📚 ystm信息")
        
        # 功能说明
        st.sbhadr("功能说明")
        st.markdown("""
        **基础对话** 💬
        - 智能问答
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
        
        # sag instrctions
        st.sbhadr("sag instrctions")
        st.markdown("""
        . **设置密钥**：在侧边栏检查ystm状态
        . **选择模式**：选择适合的聊天模式
        . **输入问题**：在输入框中输入您的问题
        . **获取回答**：点击发送或s特殊功能按钮
        """)
        
        # 技术信息
        st.sbhadr("技术信息")
        st.markdown("""
        - **框架**：anghain + tramlit
        - ****：roq  (llama-.-b-instant)
        - **版本**：简化版 v.
        - **状态**：基础功能可用
        """)


i __nam__  "__main__"
    main()
