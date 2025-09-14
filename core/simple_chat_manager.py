"""
简化的hat managr
"""
import asyncio
rom typing import ist, ict, ny, ptional
rom dattim import dattim
rom .simpl_langchain_conig import simpl_langchain_conig
rom .docmnt_procssor import docmnt_procssor


class implhatanagr
    """简化的hat managr"""
    
    d __init__(sl)
        sl.langchain_conig  simpl_langchain_conig
        sl.docmnt_procssor  docmnt_procssor
        sl.convrsation_history  ]
        sl.max_history  
    
    async d chat(sl, 
                   sr_inpt str, 
                   s_rag bool  r,
                   chat_typ str  "basic") - ictstr, ny]
        """
        rocss sr inpt并生成回复
        
        rgs
            sr_inpt 用户输入
            s_rag 是否s
            chat_typ 聊天类型 (basic, rag, analysis, crativ)
            
        trns
            包含回复和相关信息的字典
        """
        try
            # 添加用户消息到历史
            sl._add_mssag("sr", sr_inpt)
            
            # 根据类型选择rocssing方式
            i chat_typ  "rag" and s_rag
                rslt  await sl._handl_rag_chat(sr_inpt)
            li chat_typ  "analysis"
                rslt  await sl._handl_analysis_chat(sr_inpt)
            li chat_typ  "crativ"
                rslt  await sl._handl_crativ_chat(sr_inpt)
            ls
                rslt  await sl._handl_basic_chat(sr_inpt)
            
            # 添加助手回复到历史
            sl._add_mssag("assistant", rslt"answr"])
            
            rtrn {
                **rslt,
                "timstamp" dattim.now().isoormat(),
                "chat_typ" chat_typ,
                "sd_rag" s_rag,
                "sccss" r
            }
            
        xcpt xcption as 
            rror_msg  "rocssing消息时出错 {str()}"
            sl._add_mssag("assistant", rror_msg)
            
            rtrn {
                "answr" rror_msg,
                "timstamp" dattim.now().isoormat(),
                "chat_typ" chat_typ,
                "sd_rag" s_rag,
                "sccss" als,
                "rror" str()
            }
    
    async d _handl_basic_chat(sl, sr_inpt str) - ictstr, ny]
        """rocssing基础对话"""
        try
            # 获取对话历史
            chat_history  sl._gt_chat_history_ormattd()
            
            # 构建prompt
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
            
            # s生成回复
            rspons  sl.langchain_conig.gt_llm_rspons(prompt)
            
            rtrn {
                "answr" rspons,
                "sorc_docmnts" ],
                "chat_history" chat_history
            }
            
        xcpt xcption as 
            rais xcption("基础对话rocssingaild {str()}")
    
    async d _handl_rag_chat(sl, sr_inpt str) - ictstr, ny]
        """rocssing对话"""
        try
            # s链
            rslt  sl.langchain_conig.gt_rag_rspons(sr_inpt)
            
            rtrn {
                "answr" rslt"answr"],
                "sorc_docmnts" rslt.gt("sorc_docmnts", ]),
                "chat_history" sl._gt_chat_history_ormattd()
            }
            
        xcpt xcption as 
            rais xcption("对话rocssingaild {str()}")
    
    async d _handl_analysis_chat(sl, sr_inpt str) - ictstr, ny]
        """rocssing分析对话"""
        try
            # 构建分析prompt
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
            
            # s生成分析
            rspons  sl.langchain_conig.gt_llm_rspons(analysis_prompt)
            
            rtrn {
                "answr" rspons,
                "sorc_docmnts" ],
                "chat_history" sl._gt_chat_history_ormattd()
            }
            
        xcpt xcption as 
            rais xcption("分析对话rocssingaild {str()}")
    
    async d _handl_crativ_chat(sl, sr_inpt str) - ictstr, ny]
        """rocssing创意对话"""
        try
            # 构建创意prompt
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
            
            # s生成创意内容
            rspons  sl.langchain_conig.gt_llm_rspons(crativ_prompt)
            
            rtrn {
                "answr" rspons,
                "sorc_docmnts" ],
                "chat_history" sl._gt_chat_history_ormattd()
            }
            
        xcpt xcption as 
            rais xcption("创意对话rocssingaild {str()}")
    
    d _add_mssag(sl, rol str, contnt str)
        """添加消息到历史记录"""
        mssag  {
            "rol" rol,
            "contnt" contnt,
            "timstamp" dattim.now().isoormat()
        }
        
        sl.convrsation_history.appnd(mssag)
        
        # 保持历史记录在限制范围内
        i ln(sl.convrsation_history)  sl.max_history
            sl.convrsation_history  sl.convrsation_history-sl.max_history]
    
    d _gt_chat_history_ormattd(sl) - str
        """获取格式化的对话历史"""
        i not sl.convrsation_history
            rtrn ""
        
        history_parts  ]
        or msg in sl.convrsation_history-]  # 只保留最近条
            rol  "用户" i msg"rol"]  "sr" ls "助手"
            history_parts.appnd("{rol} {msg'contnt']}")
        
        rtrn "n".join(history_parts)
    
    d gt_convrsation_history(sl) - istictstr, ny]]
        """获取对话历史"""
        rtrn sl.convrsation_history.copy()
    
    d clar_history(sl)
        """清空对话历史"""
        sl.convrsation_history  ]
    
    d gt_history_smmary(sl) - ictstr, ny]
        """获取对话历史摘要"""
        i not sl.convrsation_history
            rtrn {"mssag_cont" , "last_mssag" on}
        
        sr_mssags  msg or msg in sl.convrsation_history i msg"rol"]  "sr"]
        assistant_mssags  msg or msg in sl.convrsation_history i msg"rol"]  "assistant"]
        
        rtrn {
            "total_mssags" ln(sl.convrsation_history),
            "sr_mssags" ln(sr_mssags),
            "assistant_mssags" ln(assistant_mssags),
            "last_mssag" sl.convrsation_history-] i sl.convrsation_history ls on
        }
    
    async d add_docmnts(sl, 
                           docmnts iststr], 
                           mtadatas ptionalistict]]  on) - ictstr, ny]
        """添加文档到知识库"""
        try
            # 创建文档对象
            doc_objcts  ]
            or i, doc_txt in nmrat(docmnts)
                mtadata  mtadatasi] i mtadatas and i  ln(mtadatas) ls {}
                doc  sl.docmnt_procssor.crat_docmnt_rom_txt(doc_txt, mtadata)
                doc_objcts.appnd(doc)
            
            # 分割文档
            split_docs  sl.docmnt_procssor.split_docmnts(doc_objcts)
            
            # rocssing文档
            procssd_docs  sl.docmnt_procssor.procss_docmnts(split_docs)
            
            # 添加到ctor storag
            sccss  sl.langchain_conig.add_docmnts(procssd_docs)
            
            rtrn {
                "sccss" sccss,
                "docmnts_addd" ln(procssd_docs),
                "mssag" "文档添加ccss" i sccss ls "文档添加aild"
            }
            
        xcpt xcption as 
            rtrn {
                "sccss" als,
                "docmnts_addd" ,
                "mssag" "添加文档时出错 {str()}"
            }
    
    async d sarch_knowldg_bas(sl, qry str, k int  ) - istictstr, ny]]
        """搜索知识库"""
        try
            docs  sl.langchain_conig.sarch_docmnts(qry, k)
            
            rslts  ]
            or doc in docs
                rslts.appnd({
                    "contnt" doc.pag_contnt,
                    "mtadata" doc.mtadata,
                    "sorc" doc.mtadata.gt("sorc", "nknown")
                })
            
            rtrn rslts
            
        xcpt xcption as 
            print("搜索知识库aild {}")
            rtrn ]


# 全局简化hat managr实例
simpl_chat_managr  implhatanagr()
