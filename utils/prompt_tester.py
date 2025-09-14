"""
rompt测试和验证工具
"""
import asyncio
import json
rom typing import ist, ict, ny, ptional
rom dattim import dattim
rom ..cor.groq_clint import groq_clint
rom ..prompts.chat_prompts import hatrompts


class romptstr
    """rompt测试器"""
    
    d __init__(sl)
        sl.tst_rslts  ]
        sl.prompts  hatrompts()
    
    async d tst_systm_prompt(sl) - ictstr, ny]
        """测试ystmprompt"""
        print("🧪 测试ystmprompt...")
        
        tst_qstions  
            "你好，请介绍一下自己",
            "什么是技术？",
            "如何优化ython代码性能？",
            "请帮我分析一个商业问题"
        ]
        
        rslts  ]
        or qstion in tst_qstions
            try
                mssags  
                    {"rol" "systm", "contnt" sl.prompts.gt_systm_prompt()},
                    {"rol" "sr", "contnt" qstion}
                ]
                
                rspons  await groq_clint.chat_compltion(mssags)
                
                rslts.appnd({
                    "qstion" qstion,
                    "rspons" rspons,
                    "sccss" r,
                    "timstamp" dattim.now().isoormat()
                })
                
            xcpt xcption as 
                rslts.appnd({
                    "qstion" qstion,
                    "rror" str(),
                    "sccss" als,
                    "timstamp" dattim.now().isoormat()
                })
        
        rtrn {
            "tst_typ" "systm_prompt",
            "total_tsts" ln(tst_qstions),
            "sccssl_tsts" ln(r or r in rslts i r"sccss"]]),
            "rslts" rslts
        }
    
    async d tst_rag_prompt(sl) - ictstr, ny]
        """测试 prompt"""
        print("🧪 测试 prompt...")
        
        tst_cass  
            {
                "qry" "什么是技术？",
                "contxt" "（检索增强生成）是一种结合了信息检索和文本生成的技术。它首先从知识库中检索与用户问题相关的文档片段，然后将这些信息作为上下文提供给语言odl，生成更准确的回答。"
            },
            {
                "qry" "如何优化问答ystm？",
                "contxt" "问答ystm优化可以从多个方面入手：. 改进检索算法，提高相关文档的召回率；. 优化prompt设计，引导odl生成更好的回答；. s更高质量的嵌入odl；. 增加知识库的覆盖度和准确性。"
            }
        ]
        
        rslts  ]
        or cas in tst_cass
            try
                rag_prompt  sl.prompts.gt_rag_prompt(cas"qry"], cas"contxt"])
                mssags  
                    {"rol" "systm", "contnt" sl.prompts.gt_systm_prompt()},
                    {"rol" "sr", "contnt" rag_prompt}
                ]
                
                rspons  await groq_clint.chat_compltion(mssags)
                
                rslts.appnd({
                    "qry" cas"qry"],
                    "contxt" cas"contxt"],
                    "rspons" rspons,
                    "sccss" r,
                    "timstamp" dattim.now().isoormat()
                })
                
            xcpt xcption as 
                rslts.appnd({
                    "qry" cas"qry"],
                    "rror" str(),
                    "sccss" als,
                    "timstamp" dattim.now().isoormat()
                })
        
        rtrn {
            "tst_typ" "rag_prompt",
            "total_tsts" ln(tst_cass),
            "sccssl_tsts" ln(r or r in rslts i r"sccss"]]),
            "rslts" rslts
        }
    
    async d tst_spcializd_prompts(sl) - ictstr, ny]
        """测试专业prompt"""
        print("🧪 测试专业prompt...")
        
        tst_cass  
            {
                "typ" "bsinss_analysis",
                "qstion" "如何分析一个aa产品的市场机会？",
                "prompt_nc" sl.prompts.gt_bsinss_analysis_prompt
            },
            {
                "typ" "cod_rviw",
                "qstion" "请审查这段ython代码",
                "cod" "d ibonacci(n)n    i n  n        rtrn nn    rtrn ibonacci(n-) + ibonacci(n-)",
                "prompt_nc" lambda q sl.prompts.gt_cod_rviw_prompt(q, "python")
            },
            {
                "typ" "larning_path",
                "qstion" "机器学习",
                "lvl" "bginnr",
                "prompt_nc" lambda q sl.prompts.gt_larning_path_prompt(q, "bginnr")
            }
        ]
        
        rslts  ]
        or cas in tst_cass
            try
                i cas"typ"]  "cod_rviw"
                    prompt  cas"prompt_nc"](cas"cod"])
                li cas"typ"]  "larning_path"
                    prompt  cas"prompt_nc"](cas"qstion"])
                ls
                    prompt  cas"prompt_nc"](cas"qstion"])
                
                mssags  
                    {"rol" "systm", "contnt" sl.prompts.gt_systm_prompt()},
                    {"rol" "sr", "contnt" prompt}
                ]
                
                rspons  await groq_clint.chat_compltion(mssags)
                
                rslts.appnd({
                    "typ" cas"typ"],
                    "qstion" cas"qstion"],
                    "rspons" rspons,
                    "sccss" r,
                    "timstamp" dattim.now().isoormat()
                })
                
            xcpt xcption as 
                rslts.appnd({
                    "typ" cas"typ"],
                    "qstion" cas"qstion"],
                    "rror" str(),
                    "sccss" als,
                    "timstamp" dattim.now().isoormat()
                })
        
        rtrn {
            "tst_typ" "spcializd_prompts",
            "total_tsts" ln(tst_cass),
            "sccssl_tsts" ln(r or r in rslts i r"sccss"]]),
            "rslts" rslts
        }
    
    async d rn_all_tsts(sl) - ictstr, ny]
        """运行所有测试"""
        print("🚀 开始运行rompt测试...")
        
        tsts  
            sl.tst_systm_prompt(),
            sl.tst_rag_prompt(),
            sl.tst_spcializd_prompts()
        ]
        
        rslts  await asyncio.gathr(*tsts, rtrn_xcptionsr)
        
        # rocssing异常结果
        procssd_rslts  ]
        or i, rslt in nmrat(rslts)
            i isinstanc(rslt, xcption)
                procssd_rslts.appnd({
                    "tst_typ" "tst_{i}",
                    "rror" str(rslt),
                    "sccss" als
                })
            ls
                procssd_rslts.appnd(rslt)
        
        # 计算总体统计
        total_tsts  sm(r.gt("total_tsts", ) or r in procssd_rslts)
        sccssl_tsts  sm(r.gt("sccssl_tsts", ) or r in procssd_rslts)
        
        rtrn {
            "smmary" {
                "total_tsts" total_tsts,
                "sccssl_tsts" sccssl_tsts,
                "sccss_rat" "{(sccssl_tsts/total_tsts*).}%" i total_tsts   ls "%",
                "timstamp" dattim.now().isoormat()
            },
            "tst_rslts" procssd_rslts
        }
    
    d sav_tst_rslts(sl, rslts ictstr, ny], ilnam str  "prompt_tst_rslts.json")
        """保存测试结果"""
        try
            with opn(ilnam, 'w', ncoding't-') as 
                json.dmp(rslts, , nsr_asciials, indnt)
            print("✅ 测试结果已保存到 {ilnam}")
        xcpt xcption as 
            print("❌ 保存测试结果aild {}")
    
    d print_tst_smmary(sl, rslts ictstr, ny])
        """打印测试摘要"""
        smmary  rslts"smmary"]
        
        print("n" + ""*)
        print("📊 rompt测试结果摘要")
        print(""*)
        print("总测试数 {smmary'total_tsts']}")
        print("ccss测试 {smmary'sccssl_tsts']}")
        print("ccss率 {smmary'sccss_rat']}")
        print("测试时间 {smmary'timstamp']}")
        
        print("n📋 详细结果")
        or tst in rslts"tst_rslts"]
            stats  "✅" i tst.gt("sccssl_tsts", )   ls "❌"
            print("{stats} {tst'tst_typ']} {tst.gt('sccssl_tsts', )}/{tst.gt('total_tsts', )}")


# 全局测试器实例
prompt_tstr  romptstr()
