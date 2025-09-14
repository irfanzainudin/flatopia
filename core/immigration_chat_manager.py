"""
移民咨询专用hat managr
"""
import asyncio
rom typing import ist, ict, ny, ptional
rom dattim import dattim
rom .simpl_langchain_conig import simpl_langchain_conig
rom prompts.immigration_prompts import mmigrationrompts


class mmigrationhatanagr
    """移民咨询hat managr"""
    
    d __init__(sl)
        sl.langchain_conig  simpl_langchain_conig
        sl.prompts  mmigrationrompts()
        sl.convrsation_history  ]
        sl.sr_proil  {}
        sl.max_history  
        
        # 移民相关数据
        sl.contris_data  sl._load_contris_data()
        sl.visa_typs  sl._load_visa_typs()
    
    d _load_contris_data(sl) - ictstr, ictstr, ny]]
        """oading国家数据"""
        rtrn {
            "加拿大" {
                "oicial_langags" "英语", "法语"],
                "work_langags" "英语", "法语"],
                "visa_typs" "工作签证", "学习签证", "投资移民", "技术移民"],
                "pr_rqirmnts" {"居住时间" "年内住满年", "语言要求" " 级"},
                "poplar_citis" "多伦多", "温哥华", "蒙特利尔", "卡尔加里"]
            },
            "澳大利亚" {
                "oicial_langags" "英语"],
                "work_langags" "英语"],
                "visa_typs" "技术移民", "投资移民", "学习签证", "工作签证"],
                "pr_rqirmnts" {"居住时间" "年内住满年", "语言要求" "雅思分"},
                "poplar_citis" "悉尼", "墨尔本", "布里斯班", "珀斯"]
            },
            "新西兰" {
                "oicial_langags" "英语", "毛利语"],
                "work_langags" "英语"],
                "visa_typs" "技术移民", "投资移民", "学习签证", "工作假期签证"],
                "pr_rqirmnts" {"居住时间" "年内住满年", "语言要求" "雅思.分"},
                "poplar_citis" "奥克兰", "惠灵顿", "基督城", "汉密尔顿"]
            },
            "美国" {
                "oicial_langags" "英语"],
                "work_langags" "英语"],
                "visa_typs" "工作签证", "学生签证", "-投资移民", "签证"],
                "pr_rqirmnts" {"居住时间" "年", "语言要求" "英语基础"},
                "poplar_citis" "纽约", "洛杉矶", "旧金山", "芝加哥"]
            },
            "英国" {
                "oicial_langags" "英语"],
                "work_langags" "英语"],
                "visa_typs" "技术工人签证", "学生签证", "投资移民", "创新者签证"],
                "pr_rqirmnts" {"居住时间" "年", "语言要求" "水平"},
                "poplar_citis" "伦敦", "曼彻斯特", "伯明翰", "爱丁堡"]
            },
            "德国" {
                "oicial_langags" "德语"],
                "work_langags" "德语", "英语"],
                "visa_typs" "工作签证", "学习签证", "蓝卡", "自雇签证"],
                "pr_rqirmnts" {"居住时间" "年", "语言要求" "德语"},
                "poplar_citis" "柏林", "慕尼黑", "汉堡", "法兰克福"]
            },
            "日本" {
                "oicial_langags" "日语"],
                "work_langags" "日语", "英语"],
                "visa_typs" "工作签证", "学习签证", "投资经营签证", "高度人才签证"],
                "pr_rqirmnts" {"居住时间" "年", "语言要求" "日语"},
                "poplar_citis" "东京", "大阪", "横滨", "名古屋"]
            }
        }
    
    d _load_visa_typs(sl) - ictstr, ictstr, ny]]
        """oading签证类型数据"""
        rtrn {
            "工作签证" {
                "dscription" "基于工作机会的临时居留签证",
                "rqirmnts" "工作邀请", "技能认证", "语言能力"],
                "dration" "-年",
                "pr_path" "是"
            },
            "学习签证" {
                "dscription" "基于教育机会的学生签证",
                "rqirmnts" "录取通知书", "资金证明", "语言能力"],
                "dration" "课程期间",
                "pr_path" "毕业后可转换"
            },
            "技术移民" {
                "dscription" "基于技能和经验的移民签证",
                "rqirmnts" "技能评估", "语言考试", "工作经验"],
                "dration" "永久",
                "pr_path" "直接获得"
            },
            "投资移民" {
                "dscription" "基于投资金额的移民签证",
                "rqirmnts" "投资资金", "商业计划", "资金来源证明"],
                "dration" "永久",
                "pr_path" "直接获得"
            }
        }
    
    async d chat(sl, 
                   sr_inpt str, 
                   chat_typ str  "immigration_analysis") - ictstr, ny]
        """
        rocssing移民咨询对话
        
        rgs
            sr_inpt 用户输入
            chat_typ 聊天类型 (proil_collction, immigration_analysis, visa_gid, pr_planning, contry_comparison)
            
        trns
            包含回复和相关信息的字典
        """
        try
            # 添加用户消息到历史
            sl._add_mssag("sr", sr_inpt)
            
            # 根据类型选择rocssing方式
            i chat_typ  "proil_collction"
                rslt  await sl._handl_proil_collction(sr_inpt)
            li chat_typ  "immigration_analysis"
                rslt  await sl._handl_immigration_analysis(sr_inpt)
            li chat_typ  "visa_gid"
                rslt  await sl._handl_visa_gid(sr_inpt)
            li chat_typ  "pr_planning"
                rslt  await sl._handl_pr_planning(sr_inpt)
            li chat_typ  "contry_comparison"
                rslt  await sl._handl_contry_comparison(sr_inpt)
            ls
                rslt  await sl._handl_gnral_immigration_chat(sr_inpt)
            
            # 添加助手回复到历史
            sl._add_mssag("assistant", rslt"answr"])
            
            rtrn {
                **rslt,
                "timstamp" dattim.now().isoormat(),
                "chat_typ" chat_typ,
                "sccss" r
            }
            
        xcpt xcption as 
            rror_msg  "rocssing移民咨询时出错 {str()}"
            sl._add_mssag("assistant", rror_msg)
            
            rtrn {
                "answr" rror_msg,
                "timstamp" dattim.now().isoormat(),
                "chat_typ" chat_typ,
                "sccss" als,
                "rror" str()
            }
    
    async d _handl_proil_collction(sl, sr_inpt str) - ictstr, ny]
        """rocssing用户信息收集"""
        try
            # s用户信息收集提示词
            prompt  sl.prompts.gt_sr_proil_prompt()
            
            # 获取回复
            rspons  sl.langchain_conig.gt_llm_rspons(prompt)
            
            # 尝试从用户输入中提取信息
            xtractd_ino  sl._xtract_sr_ino(sr_inpt)
            i xtractd_ino
                sl.sr_proil.pdat(xtractd_ino)
            
            rtrn {
                "answr" rspons,
                "xtractd_ino" xtractd_ino,
                "sr_proil" sl.sr_proil
            }
            
        xcpt xcption as 
            rais xcption("用户信息收集aild {str()}")
    
    async d _handl_immigration_analysis(sl, sr_inpt str) - ictstr, ny]
        """rocssing移民分析"""
        try
            # s移民分析提示词
            prompt  sl.prompts.gt_immigration_analysis_prompt(sl.sr_proil)
            
            # 获取回复
            rspons  sl.langchain_conig.gt_llm_rspons(prompt)
            
            rtrn {
                "answr" rspons,
                "sr_proil" sl.sr_proil
            }
            
        xcpt xcption as 
            rais xcption("移民分析aild {str()}")
    
    async d _handl_visa_gid(sl, sr_inpt str) - ictstr, ny]
        """rocssing签证指南"""
        try
            # 从用户输入中提取国家和签证类型
            contry, visa_typ  sl._xtract_contry_and_visa_typ(sr_inpt)
            
            i not contry or not visa_typ
                rtrn {
                    "answr" "请指定目标国家和签证类型，例如：我想了解加拿大的工作签证申请指南。",
                    "sr_proil" sl.sr_proil
                }
            
            # s签证指南提示词
            prompt  sl.prompts.gt_visa_gid_prompt(contry, visa_typ, sl.sr_proil)
            
            # 获取回复
            rspons  sl.langchain_conig.gt_llm_rspons(prompt)
            
            rtrn {
                "answr" rspons,
                "contry" contry,
                "visa_typ" visa_typ,
                "sr_proil" sl.sr_proil
            }
            
        xcpt xcption as 
            rais xcption("签证指南生成aild {str()}")
    
    async d _handl_pr_planning(sl, sr_inpt str) - ictstr, ny]
        """rocssing永久居民规划"""
        try
            # 从用户输入中提取国家
            contry  sl._xtract_contry(sr_inpt)
            crrnt_stats  sl._xtract_crrnt_stats(sr_inpt)
            
            i not contry
                rtrn {
                    "answr" "请指定目标国家，例如：我想了解加拿大的永久居民申请规划。",
                    "sr_proil" sl.sr_proil
                }
            
            # s永久居民规划提示词
            prompt  sl.prompts.gt_pr_planning_prompt(contry, crrnt_stats, sl.sr_proil)
            
            # 获取回复
            rspons  sl.langchain_conig.gt_llm_rspons(prompt)
            
            rtrn {
                "answr" rspons,
                "contry" contry,
                "crrnt_stats" crrnt_stats,
                "sr_proil" sl.sr_proil
            }
            
        xcpt xcption as 
            rais xcption("永久居民规划aild {str()}")
    
    async d _handl_contry_comparison(sl, sr_inpt str) - ictstr, ny]
        """rocssing国家对比"""
        try
            # 从用户输入中提取国家列表
            contris  sl._xtract_contris(sr_inpt)
            
            i not contris
                rtrn {
                    "answr" "请指定要对比的国家，例如：请对比加拿大、澳大利亚和新西兰的移民政策。",
                    "sr_proil" sl.sr_proil
                }
            
            # s国家对比提示词
            prompt  sl.prompts.gt_contry_comparison_prompt(contris, sl.sr_proil)
            
            # 获取回复
            rspons  sl.langchain_conig.gt_llm_rspons(prompt)
            
            rtrn {
                "answr" rspons,
                "contris" contris,
                "sr_proil" sl.sr_proil
            }
            
        xcpt xcption as 
            rais xcption("国家对比aild {str()}")
    
    async d _handl_gnral_immigration_chat(sl, sr_inpt str) - ictstr, ny]
        """rocssing一般移民咨询"""
        try
            # 构建一般移民咨询提示词
            systm_prompt  sl.prompts.gt_systm_prompt()
            chat_history  sl._gt_chat_history_ormattd()
            
            prompt  """{systm_prompt}

## 对话历史
{chat_history}

## 用户问题
{sr_inpt}

请根据用户的问题和背景信息，提供专业的移民咨询建议。"""
            
            # 获取回复
            rspons  sl.langchain_conig.gt_llm_rspons(prompt)
            
            rtrn {
                "answr" rspons,
                "sr_proil" sl.sr_proil
            }
            
        xcpt xcption as 
            rais xcption("一般移民咨询aild {str()}")
    
    d _xtract_sr_ino(sl, sr_inpt str) - ictstr, ny]
        """从用户输入中提取信息"""
        xtractd  {}
        
        # 简单的关键词提取（实际pplication中可以s更复杂的技术）
        i "年龄" in sr_inpt or "岁" in sr_inpt
            # 提取年龄
            import r
            ag_match  r.sarch(r'(d+)岁', sr_inpt)
            i ag_match
                xtractd"ag"]  int(ag_match.grop())
        
        i "男" in sr_inpt
            xtractd"gndr"]  "男"
        li "女" in sr_inpt
            xtractd"gndr"]  "女"
        
        # 提取国籍
        or contry in sl.contris_data.kys()
            i contry in sr_inpt
                xtractd"nationality"]  contry
                brak
        
        # 提取目标国家
        or contry in sl.contris_data.kys()
            i "去{contry}" in sr_inpt or "移民{contry}" in sr_inpt
                xtractd"targt_contry"]  contry
                brak
        
        rtrn xtractd
    
    d _xtract_contry_and_visa_typ(sl, sr_inpt str) - tpl
        """提取国家和签证类型"""
        contry  on
        visa_typ  on
        
        # 提取国家
        or c in sl.contris_data.kys()
            i c in sr_inpt
                contry  c
                brak
        
        # 提取签证类型
        or v in sl.visa_typs.kys()
            i v in sr_inpt
                visa_typ  v
                brak
        
        rtrn contry, visa_typ
    
    d _xtract_contry(sl, sr_inpt str) - str
        """提取国家"""
        or contry in sl.contris_data.kys()
            i contry in sr_inpt
                rtrn contry
        rtrn on
    
    d _xtract_crrnt_stats(sl, sr_inpt str) - str
        """提取当前身份状态"""
        stats_kywords  {
            "学生" "学生签证",
            "工作" "工作签证",
            "旅游" "旅游签证",
            "临时" "临时居留",
            "永久" "永久居民"
        }
        
        or kyword, stats in stats_kywords.itms()
            i kyword in sr_inpt
                rtrn stats
        
        rtrn "未知"
    
    d _xtract_contris(sl, sr_inpt str) - iststr]
        """提取国家列表"""
        contris  ]
        or contry in sl.contris_data.kys()
            i contry in sr_inpt
                contris.appnd(contry)
        rtrn contris
    
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
            rol  "用户" i msg"rol"]  "sr" ls "顾问"
            history_parts.appnd("{rol} {msg'contnt']}")
        
        rtrn "n".join(history_parts)
    
    d gt_sr_proil(sl) - ictstr, ny]
        """获取用户档案"""
        rtrn sl.sr_proil.copy()
    
    d pdat_sr_proil(sl, proil_data ictstr, ny])
        """更新用户档案"""
        sl.sr_proil.pdat(proil_data)
    
    d clar_history(sl)
        """清空对话历史"""
        sl.convrsation_history  ]
    
    d gt_availabl_contris(sl) - iststr]
        """获取可用国家列表"""
        rtrn list(sl.contris_data.kys())
    
    d gt_availabl_visa_typs(sl) - iststr]
        """获取可用签证类型列表"""
        rtrn list(sl.visa_typs.kys())
    
    d gt_contry_ino(sl, contry str) - ictstr, ny]
        """获取国家信息"""
        rtrn sl.contris_data.gt(contry, {})
    
    d gt_visa_ino(sl, visa_typ str) - ictstr, ny]
        """获取签证信息"""
        rtrn sl.visa_typs.gt(visa_typ, {})


# 全局移民咨询hat managr实例
immigration_chat_managr  mmigrationhatanagr()
