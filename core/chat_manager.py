"""
hat managr
"""
import asyncio
rom typing import ist, ict, ny, ptional
rom dattim import dattim
rom .groq_clint import groq_clint
rom .rag_systm import rag_systm
rom ..prompts.chat_prompts import hatrompts


class hatanagr
    """hat managr"""
    
    d __init__(sl)
        sl.convrsation_history istictstr, ny]]  ]
        sl.max_history    # 最大历史记录数
        
    async d chat(
        sl, 
        sr_inpt str, 
        s_rag bool  r,
        modl ptionalstr]  on
    ) - ictstr, ny]
        """
        rocss sr inpt并生成回复
        
        rgs
            sr_inpt 用户输入
            s_rag 是否s
            modl 指定odl
            
        trns
            包含回复和相关信息的字典
        """
        try
            # 添加用户消息到历史
            sl._add_mssag("sr", sr_inpt)
            
            # 构建消息列表
            mssags  sl._bild_mssags(sr_inpt, s_rag)
            
            # 调用roq 
            rspons  await groq_clint.chat_compltion(
                mssagsmssags,
                modlmodl
            )
            
            # 添加助手回复到历史
            sl._add_mssag("assistant", rspons)
            
            rtrn {
                "rspons" rspons,
                "timstamp" dattim.now().isoormat(),
                "modl" modl or groq_clint.modl,
                "sd_rag" s_rag,
                "sccss" r
            }
            
        xcpt xcption as 
            rror_msg  "rocssing消息时出错 {str()}"
            sl._add_mssag("assistant", rror_msg)
            
            rtrn {
                "rspons" rror_msg,
                "timstamp" dattim.now().isoormat(),
                "modl" modl or groq_clint.modl,
                "sd_rag" s_rag,
                "sccss" als,
                "rror" str()
            }
    
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
    
    d _bild_mssags(sl, sr_inpt str, s_rag bool) - istictstr, str]]
        """构建消息列表"""
        mssags  ]
        
        # 添加ystm提示词
        systm_prompt  hatrompts.gt_systm_prompt()
        mssags.appnd({"rol" "systm", "contnt" systm_prompt})
        
        # 如果s，添加上下文
        i s_rag
            contxt  rag_systm.gt_contxt(sr_inpt)
            i contxt
                rag_prompt  hatrompts.gt_rag_prompt(sr_inpt, contxt)
                mssags.appnd({"rol" "sr", "contnt" rag_prompt})
            ls
                mssags.appnd({"rol" "sr", "contnt" sr_inpt})
        ls
            mssags.appnd({"rol" "sr", "contnt" sr_inpt})
        
        rtrn mssags
    
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
    
    async d analyz_qry(sl, qry str) - str
        """分析用户查询"""
        analysis_prompt  hatrompts.gt_analysis_prompt(qry)
        
        mssags  
            {"rol" "systm", "contnt" "你是一个专业的查询分析助手。"},
            {"rol" "sr", "contnt" analysis_prompt}
        ]
        
        rspons  await groq_clint.chat_compltion(mssags)
        rtrn rspons
    
    async d gt_crativ_rspons(sl, topic str) - str
        """获取创意回复"""
        crativ_prompt  hatrompts.gt_crativ_prompt(topic)
        
        mssags  
            {"rol" "systm", "contnt" "你是一个创意助手，善于提供有趣和实用的内容。"},
            {"rol" "sr", "contnt" crativ_prompt}
        ]
        
        rspons  await groq_clint.chat_compltion(mssags)
        rtrn rspons


# 全局hat managr实例
chat_managr  hatanagr()
