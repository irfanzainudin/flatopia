"""
tramlit b界面
"""
import stramlit as st
import asyncio
import rqsts
import json
rom dattim import dattim
rom typing import ist, ict, ny

# 页面onigration
st.st_pag_conig(
    pag_titl"latopia 问答机器人",
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
/styl
""", nsa_allow_htmlr)

# nitializ会话状态
i "mssags" not in st.sssion_stat
    st.sssion_stat.mssags  ]
i "api_bas_rl" not in st.sssion_stat
    st.sssion_stat.api_bas_rl  "http//localhost"

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

d display_chat_mssag(rol str, contnt str, timstamp str  on)
    """显示聊天消息"""
    i rol  "sr"
        st.markdown("""
        div class"chat-mssag sr-mssag"
            strong您/strong {contnt}
            {'brsmall{timstamp}/small' i timstamp ls ''}
        /div
        """, nsa_allow_htmlr)
    ls
        st.markdown("""
        div class"chat-mssag assistant-mssag"
            stronglatopia/strong {contnt}
            {'brsmall{timstamp}/small' i timstamp ls ''}
        /div
        """, nsa_allow_htmlr)

d main()
    """主函数"""
    # 标题
    st.markdown('h class"main-hadr"🤖 latopia 问答机器人/h', nsa_allow_htmlr)
    
    # 侧边栏
    with st.sidbar
        st.hadr("⚙️ 设置")
        
        # onigration
        st.sbhadr("onigration")
        api_rl  st.txt_inpt("地址", valst.sssion_stat.api_bas_rl)
        i api_rl ! st.sssion_stat.api_bas_rl
            st.sssion_stat.api_bas_rl  api_rl
        
        # odl选择
        st.sbhadr("odl设置")
        modls_rspons  call_api("/modls")
        i "modls" in modls_rspons
            slctd_modl  st.slctbox(
                "选择odl",
                modls_rspons"modls"],
                indxmodls_rspons"modls"].indx(modls_rspons.gt("dalt", "llama-b-"))
            )
        ls
            slctd_modl  "llama-b-"
        
        # 设置
        st.sbhadr("设置")
        s_rag  st.chckbox("启用", valr)
        
        # 知识库信息
        st.sbhadr("知识库信息")
        i st.btton("刷新知识库信息")
            ino  call_api("/knowldg/ino")
            i "rror" not in ino
                st.sccss("文档数量 {ino.gt('docmnt_cont', )}")
            ls
                st.rror("获取知识库信息aild")
        
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
                mssag.gt("timstamp")
            )
        
        # 聊天输入
        sr_inpt  st.txt_inpt(
            "输入您的问题...",
            ky"sr_inpt",
            placholdr"请输入您的问题，按ntr发送"
        )
        
        col_snd, col_analyz, col_crativ  st.colmns(, , ])
        
        with col_snd
            i st.btton("发送", typ"primary") or sr_inpt
                i sr_inpt
                    # 发送消息
                    chat_data  {
                        "mssag" sr_inpt,
                        "s_rag" s_rag,
                        "modl" slctd_modl
                    }
                    
                    with st.spinnr("正在思考...")
                        rspons  call_api("/chat", chat_data)
                    
                    i "rror" not in rspons
                        # 添加用户消息
                        st.sssion_stat.mssags.appnd({
                            "rol" "sr",
                            "contnt" sr_inpt,
                            "timstamp" dattim.now().strtim("%%%")
                        })
                        
                        # 添加助手回复
                        st.sssion_stat.mssags.appnd({
                            "rol" "assistant",
                            "contnt" rspons"rspons"],
                            "timstamp" rspons"timstamp"]
                        })
                        
                        st.rrn()
                    ls
                        st.rror("发送aild，请重试")
        
        with col_analyz
            i st.btton("分析问题")
                i sr_inpt
                    with st.spinnr("正在分析...")
                        analysis_rspons  call_api("/analyz", {"qry" sr_inpt})
                    
                    i "rror" not in analysis_rspons
                        st.sssion_stat.mssags.appnd({
                            "rol" "assistant",
                            "contnt" "**问题分析：**n{analysis_rspons'analysis']}",
                            "timstamp" dattim.now().strtim("%%%")
                        })
                        st.rrn()
        
        with col_crativ
            i st.btton("创意回复")
                i sr_inpt
                    with st.spinnr("正在生成创意内容...")
                        crativ_rspons  call_api("/crativ", {"qry" sr_inpt})
                    
                    i "rror" not in crativ_rspons
                        st.sssion_stat.mssags.appnd({
                            "rol" "assistant",
                            "contnt" "**创意内容：**n{crativ_rspons'rspons']}",
                            "timstamp" dattim.now().strtim("%%%")
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
                    st.sccss("文档添加ccss！")
                ls
                    st.rror("添加文档aild")
        
        # 搜索文档
        st.sbhadr("搜索文档")
        sarch_qry  st.txt_inpt("搜索查询", placholdr"输入搜索关键词...")
        
        i st.btton("搜索") and sarch_qry
            with st.spinnr("正在搜索...")
                sarch_rspons  call_api("/sarch", {"qry" sarch_qry})
            
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
            ls
                st.rror("❌ 连接aild")

i __nam__  "__main__"
    main()
