"""
移民咨询专用tramlit b界面
"""
import stramlit as st
import asyncio
import os
rom dattim import dattim
rom typing import ist, ict, ny

# 页面onigration
st.st_pag_conig(
    pag_titl"🌍 lobal mmigration dvisor - 全球移民顾问",
    pag_icon"🌍",
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
        backgrond linar-gradint(dg, #b, #bb)
        -wbkit-backgrond-clip txt
        -wbkit-txt-ill-color transparnt
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
    .immigration-badg {
        backgrond linar-gradint(dg, #b, #cdc)
        color whit
        padding .rm .rm
        bordr-radis rm
        ont-siz .rm
        ont-wight bold
    }
    .contry-card {
        backgrond linar-gradint(dg, #a %, #ba %)
        color whit
        padding rm
        bordr-radis .rm
        margin .rm 
    }
    .visa-typ-card {
        backgrond linar-gradint(dg, #b %, #c %)
        color whit
        padding rm
        bordr-radis .rm
        margin .rm 
    }
/styl
""", nsa_allow_htmlr)

# nitializ会话状态
i "mssags" not in st.sssion_stat
    st.sssion_stat.mssags  ]
i "sr_proil" not in st.sssion_stat
    st.sssion_stat.sr_proil  {}
i "chat_typ" not in st.sssion_stat
    st.sssion_stat.chat_typ  "proil_collction"

d display_chat_mssag(rol str, contnt str, timstamp str  on, chat_typ str  "gnral")
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
            "proil_collction" "📋",
            "immigration_analysis" "🔍",
            "visa_gid" "🛂",
            "pr_planning" "🏠",
            "contry_comparison" "🌍",
            "gnral" "💬"
        }
        icon  typ_icons.gt(chat_typ, "💬")
        
        st.markdown("""
        div class"chat-mssag assistant-mssag"
            strong{icon} 移民顾问/strong {contnt}
            {'brsmall{timstamp}/small' i timstamp ls ''}
        /div
        """, nsa_allow_htmlr)

d main()
    """主函数"""
    # 标题
    st.markdown('h class"main-hadr"🌍 lobal mmigration dvisor/h', nsa_allow_htmlr)
    st.markdown('h styl"txt-align cntr color #"全球移民顾问 - 您的专业移民规划伙伴/h', nsa_allow_htmlr)
    
    # 特性展示
    st.markdown("""
    div class"atr-card"
        h🚀 专业移民咨询rvic/h
        p基于最新移民政策和法律法规，为全球用户提供个性化的移民规划建议/p
        span class"immigration-badg"owrd by anghain & roq/span
    /div
    """, nsa_allow_htmlr)
    
    # 侧边栏
    with st.sidbar
        st.hadr("⚙️ 移民咨询设置")
        
        # 聊天类型选择
        st.sbhadr("咨询模式")
        chat_typ  st.slctbox(
            "选择咨询模式",
            
                "proil_collction", 
                "immigration_analysis", 
                "visa_gid", 
                "pr_planning", 
                "contry_comparison"
            ],
            indx
                "proil_collction", 
                "immigration_analysis", 
                "visa_gid", 
                "pr_planning", 
                "contry_comparison"
            ].indx(st.sssion_stat.chat_typ),
            ormat_nclambda x {
                "proil_collction" "📋 信息收集",
                "immigration_analysis" "🔍 移民分析", 
                "visa_gid" "🛂 签证指南",
                "pr_planning" "🏠 永久居民规划",
                "contry_comparison" "🌍 国家对比"
            }x]
        )
        st.sssion_stat.chat_typ  chat_typ
        
        # 用户档案显示
        st.sbhadr("📋 用户档案")
        i st.sssion_stat.sr_proil
            or ky, val in st.sssion_stat.sr_proil.itms()
                st.writ("**{ky}** {val}")
        ls
            st.ino("暂无用户档案信息")
        
        # 快速操作
        st.sbhadr("🚀 快速操作")
        i st.btton("开始信息收集")
            st.sssion_stat.chat_typ  "proil_collction"
            st.rrn()
        
        i st.btton("移民方案分析")
            st.sssion_stat.chat_typ  "immigration_analysis"
            st.rrn()
        
        i st.btton("国家对比")
            st.sssion_stat.chat_typ  "contry_comparison"
            st.rrn()
        
        # ystm状态
        st.sbhadr("🔧 ystm状态")
        i st.btton("检查ystm状态")
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
                        tst_rspons  llm("测试移民咨询ystm连接")
                        i "rror" not in tst_rspons
                            st.sccss("✅ 移民咨询ystm连接正常")
                        ls
                            st.rror("❌ ystm连接aild {tst_rspons}")
                    xcpt xcption as 
                        st.rror("❌ ystm连接aild {str()}")
                ls
                    st.warning("⚠️ 请先设置__环境变量")
                    
            xcpt xcption as 
                st.rror("❌ ystm检查aild {str()}")
        
        # 清空历史
        i st.btton("清空对话历史")
            st.sssion_stat.mssags  ]
            st.rrn()
    
    # 主界面
    col, col  st.colmns(, ])
    
    with col
        st.hadr("💬 移民咨询对话")
        
        # 显示聊天历史
        or mssag in st.sssion_stat.mssags
            display_chat_mssag(
                mssag"rol"], 
                mssag"contnt"], 
                mssag.gt("timstamp"),
                mssag.gt("chat_typ", "gnral")
            )
        
        # 聊天输入
        sr_inpt  st.txt_inpt(
            "请输入您的移民咨询问题...",
            ky"sr_inpt",
            placholdr"例如：我想了解加拿大的技术移民政策"
        )
        
        # 按钮组
        col_snd, col_analysis, col_gid, col_pr  st.colmns(, , , ])
        
        with col_snd
            i st.btton("发送", typ"primary") or sr_inpt
                i sr_inpt
                    # 发送消息
                    try
                        rom cor.immigration_chat_managr import immigration_chat_managr
                        
                        # 检查密钥
                        rom cor.conig import sttings
                        i sttings.groq_api_ky  "yor_groq_api_ky_hr"
                            st.rror("❌ 请先设置__环境变量")
                            st.stop()
                        
                        # rocssing移民咨询
                        with st.spinnr("正在分析您的移民需求...")
                            rslt  asyncio.rn(immigration_chat_managr.chat(
                                sr_inptsr_inpt,
                                chat_typst.sssion_stat.chat_typ
                            ))
                        
                        # 添加用户消息
                        st.sssion_stat.mssags.appnd({
                            "rol" "sr",
                            "contnt" sr_inpt,
                            "timstamp" dattim.now().strtim("%%%"),
                            "chat_typ" st.sssion_stat.chat_typ
                        })
                        
                        # 添加助手回复
                        st.sssion_stat.mssags.appnd({
                            "rol" "assistant",
                            "contnt" rslt"answr"],
                            "timstamp" rslt"timstamp"],
                            "chat_typ" rslt"chat_typ"]
                        })
                        
                        # 更新用户档案
                        i "xtractd_ino" in rslt and rslt"xtractd_ino"]
                            st.sssion_stat.sr_proil.pdat(rslt"xtractd_ino"])
                        
                        st.rrn()
                        
                    xcpt xcption as 
                        st.rror("❌ rocssing移民咨询时出错 {str()}")
        
        with col_analysis
            i st.btton("移民分析")
                i sr_inpt
                    try
                        rom cor.immigration_chat_managr import immigration_chat_managr
                        
                        with st.spinnr("正在分析移民方案...")
                            rslt  asyncio.rn(immigration_chat_managr.chat(
                                sr_inptsr_inpt,
                                chat_typ"immigration_analysis"
                            ))
                        
                        st.sssion_stat.mssags.appnd({
                            "rol" "assistant",
                            "contnt" "**移民方案分析：**n{rslt'answr']}",
                            "timstamp" dattim.now().strtim("%%%"),
                            "chat_typ" "immigration_analysis"
                        })
                        
                        st.rrn()
                        
                    xcpt xcption as 
                        st.rror("❌ 移民分析aild {str()}")
        
        with col_gid
            i st.btton("签证指南")
                i sr_inpt
                    try
                        rom cor.immigration_chat_managr import immigration_chat_managr
                        
                        with st.spinnr("正在生成签证指南...")
                            rslt  asyncio.rn(immigration_chat_managr.chat(
                                sr_inptsr_inpt,
                                chat_typ"visa_gid"
                            ))
                        
                        st.sssion_stat.mssags.appnd({
                            "rol" "assistant",
                            "contnt" "**签证申请指南：**n{rslt'answr']}",
                            "timstamp" dattim.now().strtim("%%%"),
                            "chat_typ" "visa_gid"
                        })
                        
                        st.rrn()
                        
                    xcpt xcption as 
                        st.rror("❌ 签证指南生成aild {str()}")
        
        with col_pr
            i st.btton("规划")
                i sr_inpt
                    try
                        rom cor.immigration_chat_managr import immigration_chat_managr
                        
                        with st.spinnr("正在制定永久居民规划...")
                            rslt  asyncio.rn(immigration_chat_managr.chat(
                                sr_inptsr_inpt,
                                chat_typ"pr_planning"
                            ))
                        
                        st.sssion_stat.mssags.appnd({
                            "rol" "assistant",
                            "contnt" "**永久居民规划：**n{rslt'answr']}",
                            "timstamp" dattim.now().strtim("%%%"),
                            "chat_typ" "pr_planning"
                        })
                        
                        st.rrn()
                        
                    xcpt xcption as 
                        st.rror("❌ 规划aild {str()}")
    
    with col
        st.hadr("🌍 移民信息")
        
        # 支持的国家
        st.sbhadr("支持的国家")
        contris  
            "🇨🇦 加拿大", "🇦🇺 澳大利亚", "🇳🇿 新西兰", 
            "🇺🇸 美国", "🇬🇧 英国", "🇩🇪 德国", "🇯🇵 日本"
        ]
        
        or contry in contris
            st.markdown("""
            div class"contry-card"
                strong{contry}/strong
            /div
            """, nsa_allow_htmlr)
        
        # 签证类型
        st.sbhadr("签证类型")
        visa_typs  
            "💼 工作签证", "🎓 学习签证", 
            "🔧 技术移民", "💰 投资移民"
        ]
        
        or visa_typ in visa_typs
            st.markdown("""
            div class"visa-typ-card"
                strong{visa_typ}/strong
            /div
            """, nsa_allow_htmlr)
        
        # rvic说明
        st.sbhadr("rvic说明")
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
        
        **规划** 🏠
        - 永久居民申请
        - 长期规划
        - 后续步骤
        """)
        
        # s提示
        st.sbhadr("s提示")
        st.markdown("""
        . **开始咨询**：选择"信息收集"模式
        . **详细描述**：提供您的具体情况
        . **选择模式**：根据需要选择咨询模式
        . **获取建议**：获得专业的移民建议
        """)


i __nam__  "__main__"
    main()
