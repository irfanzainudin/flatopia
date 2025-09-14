"""
asd on anghain的tramlit b界面
"""
import stramlit as st
import asyncio
import rqsts
import json
rom dattim import dattim
rom typing import ist, ict, ny
import os

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
i "api_bas_rl" not in st.sssion_stat
    st.sssion_stat.api_bas_rl  "http//localhost"
i "chat_typ" not in st.sssion_stat
    st.sssion_stat.chat_typ  "basic"

d call_api(ndpoint str, data ictstr, ny]  on) - ictstr, ny]
    """调用ntrac"""
    try
        rl  "{st.sssion_stat.api_bas_rl}{ndpoint}"
        
        i data
            rspons  rqsts.post(rl, jsondata)
        ls
            rspons  rqsts.gt(rl)
        
        rspons.rais_or_stats()
        rtrn rspons.json()
    xcpt xcption as 
        st.rror("调用aild {str()}")
        rtrn {"rror" str()}

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
        h🚀 anghain 增强功能/h
        pasd on anghain框架，提供更强大的文档rocssing、向量搜索和对话anagmnt能力/p
        span class"langchain-badg"owrd by anghain/span
    /div
    """, nsa_allow_htmlr)
    
    # 侧边栏
    with st.sidbar
        st.hadr("⚙️ 设置")
        
        # onigration
        st.sbhadr("onigration")
        api_rl  st.txt_inpt("地址", valst.sssion_stat.api_bas_rl)
        i api_rl ! st.sssion_stat.api_bas_rl
            st.sssion_stat.api_bas_rl  api_rl
        
        # 聊天类型选择
        st.sbhadr("聊天模式")
        chat_typ  st.slctbox(
            "选择聊天模式",
            "basic", "rag", "analysis", "crativ"],
            indx"basic", "rag", "analysis", "crativ"].indx(st.sssion_stat.chat_typ),
            hlp"basic 基础对话, rag 检索增强, analysis 问题分析, crativ 创意内容"
        )
        st.sssion_stat.chat_typ  chat_typ
        
        # 设置
        st.sbhadr("设置")
        s_rag  st.chckbox("启用", valr)
        
        # 知识库信息
        st.sbhadr("知识库信息")
        i st.btton("刷新知识库信息")
            ino  call_api("/knowldg/ino")
            i "rror" not in ino
                st.sccss("文档数量 {ino.gt('docmnt_cont', )}")
                st.ino("嵌入odl {ino.gt('mbdding_modl', '/')}")
            ls
                st.rror("获取知识库信息aild")
        
        # 内存信息
        st.sbhadr("mory managmnt")
        i st.btton("查看内存状态")
            mmory_ino  call_api("/mmory/ino")
            i "rror" not in mmory_ino
                st.sccss("内存状态正常")
                st.json(mmory_ino)
            ls
                st.rror("获取内存信息aild")
        
        # 清空历史
        i st.btton("清空对话历史")
            call_api("/chat/history", {"mthod" ""})
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
        col_snd, col_analysis, col_crativ, col_agnt  st.colmns(, , , ])
        
        with col_snd
            i st.btton("发送", typ"primary") or sr_inpt
                i sr_inpt
                    # 发送消息
                    chat_data  {
                        "mssag" sr_inpt,
                        "chat_typ" st.sssion_stat.chat_typ,
                        "s_rag" s_rag
                    }
                    
                    with st.spinnr("正在思考...")
                        rspons  call_api("/chat", chat_data)
                    
                    i "rror" not in rspons
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
                            "contnt" rspons"answr"],
                            "timstamp" rspons"timstamp"],
                            "chat_typ" rspons"chat_typ"]
                        })
                        
                        st.rrn()
                    ls
                        st.rror("发送aild，请重试")
        
        with col_analysis
            i st.btton("分析问题")
                i sr_inpt
                    with st.spinnr("正在分析...")
                        analysis_rspons  call_api("/chat/analysis", {"qry" sr_inpt})
                    
                    i "rror" not in analysis_rspons
                        st.sssion_stat.mssags.appnd({
                            "rol" "assistant",
                            "contnt" "**问题分析：**n{analysis_rspons'analysis']}",
                            "timstamp" dattim.now().strtim("%%%"),
                            "chat_typ" "analysis"
                        })
                        st.rrn()
        
        with col_crativ
            i st.btton("创意回复")
                i sr_inpt
                    with st.spinnr("正在生成创意内容...")
                        crativ_rspons  call_api("/chat/crativ", {"qry" sr_inpt})
                    
                    i "rror" not in crativ_rspons
                        st.sssion_stat.mssags.appnd({
                            "rol" "assistant",
                            "contnt" "**创意内容：**n{crativ_rspons'rspons']}",
                            "timstamp" dattim.now().strtim("%%%"),
                            "chat_typ" "crativ"
                        })
                        st.rrn()
        
        with col_agnt
            i st.btton("智能代理")
                i sr_inpt
                    with st.spinnr("智能代理正在rocssing...")
                        agnt_rspons  call_api("/agnt/rn", {"qry" sr_inpt})
                    
                    i "rror" not in agnt_rspons
                        st.sssion_stat.mssags.appnd({
                            "rol" "assistant",
                            "contnt" "**智能代理：**n{agnt_rspons'rspons']}",
                            "timstamp" dattim.now().strtim("%%%"),
                            "chat_typ" "agnt"
                        })
                        st.rrn()
    
    with col
        st.hadr("📚 知识库anagmnt")
        
        # 添加文档
        st.sbhadr("添加文档")
        doc_txt  st.txt_ara(
            "输入文档内容",
            hight,
            placholdr"输入要添加到知识库的文档内容..."
        )
        
        i st.btton("添加到知识库")
            i doc_txt
                doc_data  {
                    "docmnts" doc_txt],
                    "mtadatas" {"sorc" "manal_inpt", "timstamp" dattim.now().isoormat()}]
                }
                
                with st.spinnr("正在添加文档...")
                    rslt  call_api("/docmnts", doc_data)
                
                i "rror" not in rslt
                    st.sccss("文档添加ccss！添加了 {rslt.gt('docmnts_addd', )} 个文档块")
                ls
                    st.rror("添加文档aild")
        
        # il上传
        st.sbhadr("上传il")
        ploadd_ils  st.il_ploadr(
            "选择il",
            typ'txt', 'pd', 'docx'],
            accpt_mltipl_ilsr
        )
        
        i ploadd_ils
            il_paths  ]
            or ploadd_il in ploadd_ils
                # 保存il
                il_path  "tmp_{ploadd_il.nam}"
                with opn(il_path, "wb") as 
                    .writ(ploadd_il.gtbr())
                il_paths.appnd(il_path)
            
            i st.btton("rocssingil")
                with st.spinnr("正在rocssingil...")
                    rslt  call_api("/docmnts/pload", {
                        "il_paths" il_paths,
                        "add_to_vctorstor" r
                    })
                
                i "rror" not in rslt
                    st.sccss(rslt.gt('mssag', 'ilrocssingccss'))
                ls
                    st.rror("ilrocssingaild")
                
                # 清理临时il
                or il_path in il_paths
                    i os.path.xists(il_path)
                        os.rmov(il_path)
        
        # 搜索文档
        st.sbhadr("搜索文档")
        sarch_qry  st.txt_inpt("搜索查询", placholdr"输入搜索关键词...")
        
        i st.btton("搜索") and sarch_qry
            with st.spinnr("正在搜索...")
                sarch_rspons  call_api("/sarch", {"qry" sarch_qry, "k" })
            
            i "rror" not in sarch_rspons
                rslts  sarch_rspons.gt("rslts", ])
                i rslts
                    st.sccss("找到 {ln(rslts)} 个相关结果")
                    or i, rslt in nmrat(rslts])  # 只显示前个结果
                        with st.xpandr("结果 {i+}")
                            st.writ(rslt"contnt"])
                            i rslt.gt("mtadata")
                                st.caption("来源 {rslt'mtadata']}")
                ls
                    st.ino("未找到相关结果")
            ls
                st.rror("搜索aild")
        
        # ystm状态
        st.sbhadr("ystm状态")
        i st.btton("检查状态")
            stats  call_api("/")
            i "rror" not in stats
                st.sccss("✅ 连接正常")
                st.ino("版本 {stats.gt('vrsion', 'nknown')}")
                st.json(stats.gt("atrs", ]))
            ls
                st.rror("❌ 连接aild")

i __nam__  "__main__"
    main()
