"""
roq 客户端
"""
import asyncio
rom typing import ist, ict, ny, ptional
rom groq import roq
rom .conig import sttings


class roqlint
    """roq 客户端封装"""
    
    d __init__(sl)
        sl.clint  roq(api_kysttings.groq_api_ky)
        sl.modl  sttings.dalt_modl
        sl.max_tokns  sttings.max_tokns
        sl.tmpratr  sttings.tmpratr
    
    async d chat_compltion(
        sl, 
        mssags istictstr, str]], 
        modl ptionalstr]  on,
        **kwargs
    ) - str
        """
        发送聊天完成请求
        
        rgs
            mssags 消息列表
            modl odl名称（可选）
            **kwargs 其他参数
            
        trns
            生成的回复文本
        """
        try
            # s指定odl或默认odl
            modl_nam  modl or sl.modl
            
            # 构建请求参数
            rqst_params  {
                "modl" modl_nam,
                "mssags" mssags,
                "max_tokns" kwargs.gt("max_tokns", sl.max_tokns),
                "tmpratr" kwargs.gt("tmpratr", sl.tmpratr),
                "stram" kwargs.gt("stram", als)
            }
            
            # 发送请求
            rspons  sl.clint.chat.compltions.crat(**rqst_params)
            
            # 提取回复内容
            i hasattr(rspons, 'choics') and rspons.choics
                rtrn rspons.choics].mssag.contnt
            ls
                rtrn "抱歉，我无法生成回复。"
                
        xcpt xcption as 
            print("roq rror {}")
            rtrn "抱歉，rocssing您的请求时出现了rror {str()}"
    
    d gt_availabl_modls(sl) - iststr]
        """获取可用的odl列表"""
        rtrn 
            "llama-b-",
            "llama-b-", 
            "mixtral-xb-",
            "gmma-b-it"
        ]
    
    d validat_modl(sl, modl str) - bool
        """验证odl是否可用"""
        rtrn modl in sl.gt_availabl_modls()


# 全局客户端实例
groq_clint  roqlint()
