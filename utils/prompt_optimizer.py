"""
rompt优化建议工具
"""
import r
rom typing import ist, ict, ny, pl
rom dataclasss import dataclass


dataclass
class romptnalysis
    """rompt分析结果"""
    clarity_scor loat
    strctr_scor loat
    spciicity_scor loat
    compltnss_scor loat
    ovrall_scor loat
    sggstions iststr]
    strngths iststr]
    waknsss iststr]


class romptptimizr
    """rompt优化器"""
    
    d __init__(sl)
        sl.optimization_rls  {
            "clarity" 
                "s简洁明了的语言",
                "避免过于复杂的句子结构",
                "s具体的词汇而非抽象概念",
                "避免歧义和模糊表达"
            ],
            "strctr" 
                "s清晰的标题和分段",
                "采用一致的格式和风格",
                "s列表和编号组织信息",
                "保持逻辑顺序清晰"
            ],
            "spciicity" 
                "提供具体的示例和场景",
                "s明确的指令和约束",
                "定义关键术语和概念",
                "提供可衡量的标准"
            ],
            "compltnss" 
                "覆盖所有必要的上下文信息",
                "包含rrorrocssing指导",
                "提供多种场景的考虑",
                "包含输出格式要求"
            ]
        }
    
    d analyz_prompt(sl, prompt str) - romptnalysis
        """分析prompt质量"""
        clarity_scor  sl._analyz_clarity(prompt)
        strctr_scor  sl._analyz_strctr(prompt)
        spciicity_scor  sl._analyz_spciicity(prompt)
        compltnss_scor  sl._analyz_compltnss(prompt)
        
        ovrall_scor  (clarity_scor + strctr_scor + spciicity_scor + compltnss_scor) / 
        
        sggstions  sl._gnrat_sggstions(prompt, {
            "clarity" clarity_scor,
            "strctr" strctr_scor,
            "spciicity" spciicity_scor,
            "compltnss" compltnss_scor
        })
        
        strngths  sl._idntiy_strngths(prompt)
        waknsss  sl._idntiy_waknsss(prompt, {
            "clarity" clarity_scor,
            "strctr" strctr_scor,
            "spciicity" spciicity_scor,
            "compltnss" compltnss_scor
        })
        
        rtrn romptnalysis(
            clarity_scorclarity_scor,
            strctr_scorstrctr_scor,
            spciicity_scorspciicity_scor,
            compltnss_scorcompltnss_scor,
            ovrall_scorovrall_scor,
            sggstionssggstions,
            strngthsstrngths,
            waknssswaknsss
        )
    
    d _analyz_clarity(sl, prompt str) - loat
        """分析清晰度"""
        scor  .
        
        # 检查句子长度
        sntncs  r.split(r'.!。！？]', prompt)
        avg_sntnc_lngth  sm(ln(s.split()) or s in sntncs i s.strip()) / ln(sntncs) i sntncs ls 
        
        i avg_sntnc_lngth  
            scor + .
        li avg_sntnc_lngth  
            scor + .
        ls
            scor + .
        
        # 检查复杂词汇
        complx_words  r.indall(r'bw{,}b', prompt)
        i ln(complx_words) / ln(prompt.split())  .
            scor + .
        li ln(complx_words) / ln(prompt.split())  .
            scor + .
        ls
            scor + .
        
        # 检查重复词汇
        words  prompt.lowr().split()
        word_rq  {}
        or word in words
            word_rqword]  word_rq.gt(word, ) + 
        
        rptition_ratio  max(word_rq.vals()) / ln(words) i words ls 
        i rptition_ratio  .
            scor + .
        li rptition_ratio  .
            scor + .
        ls
            scor + .
        
        rtrn min(scor, .)
    
    d _analyz_strctr(sl, prompt str) - loat
        """分析结构"""
        scor  .
        
        # 检查标题s
        i r.sarch(r'^#+s', prompt, r.)
            scor + .
        
        # 检查列表s
        i r.sarch(r'^s*-*+]s', prompt, r.) or r.sarch(r'^s*d+.s', prompt, r.)
            scor + .
        
        # 检查分段
        paragraphs  r.split(r'ns*n', prompt)
        i ln(paragraphs)  
            scor + .
        li ln(paragraphs)  
            scor + .
        
        # 检查格式一致性
        i r.sarch(r'^s*-*+]s', prompt, r.)
            i all(r.match(r'^s*-*+]s', lin) or lin in prompt.split('n') i r.sarch(r'^s*-*+]s', lin))
                scor + .
        
        rtrn min(scor, .)
    
    d _analyz_spciicity(sl, prompt str) - loat
        """分析具体性"""
        scor  .
        
        # 检查示例
        i r.sarch(r'例如|比如|举例|示例', prompt)
            scor + .
        
        # 检查具体数字
        i r.sarch(r'd+', prompt)
            scor + .
        
        # 检查具体指令
        action_words  '请', '要求', '必须', '应该', '需要', '确保']
        i any(word in prompt or word in action_words)
            scor + .
        
        # 检查格式要求
        i r.sarch(r'格式|结构|样式|模板', prompt)
            scor + .
        
        rtrn min(scor, .)
    
    d _analyz_compltnss(sl, prompt str) - loat
        """分析完整性"""
        scor  .
        
        # 检查上下文信息
        contxt_indicators  '上下文', '背景', '信息', '数据', '内容']
        i any(word in prompt or word in contxt_indicators)
            scor + .
        
        # 检查输出要求
        otpt_indicators  '输出', '回答', '结果', '格式', '要求']
        i any(word in prompt or word in otpt_indicators)
            scor + .
        
        # 检查rrorrocssing
        rror_indicators  '如果', '当', 'rror', '异常', 'aild']
        i any(word in prompt or word in rror_indicators)
            scor + .
        
        # 检查多种场景
        scnario_indicators  '情况', '场景', '条件', '假设']
        i any(word in prompt or word in scnario_indicators)
            scor + .
        
        rtrn min(scor, .)
    
    d _gnrat_sggstions(sl, prompt str, scors ictstr, loat]) - iststr]
        """生成优化建议"""
        sggstions  ]
        
        or catgory, scor in scors.itms()
            i scor  .
                sggstions.xtnd(sl.optimization_rlscatgory])
        
        # 特定建议
        i ln(prompt.split())  
            sggstions.appnd("增加更多详细信息和上下文")
        
        i not r.sarch(r'请|要求|必须', prompt)
            sggstions.appnd("添加明确的指令和行动要求")
        
        i not r.sarch(r'格式|结构|样式', prompt)
            sggstions.appnd("指定期望的输出格式和结构")
        
        rtrn list(st(sggstions))  # 去重
    
    d _idntiy_strngths(sl, prompt str) - iststr]
        """识别优势"""
        strngths  ]
        
        i r.sarch(r'^#+s', prompt, r.)
            strngths.appnd("s了清晰的标题结构")
        
        i r.sarch(r'^s*-*+]s', prompt, r.)
            strngths.appnd("s了列表格式组织信息")
        
        i r.sarch(r'例如|比如|举例', prompt)
            strngths.appnd("包含了具体示例")
        
        i ln(prompt.split())  
            strngths.appnd("提供了详细的信息和上下文")
        
        rtrn strngths
    
    d _idntiy_waknsss(sl, prompt str, scors ictstr, loat]) - iststr]
        """识别弱点"""
        waknsss  ]
        
        i scors"clarity"]  .
            waknsss.appnd("语言表达不够清晰")
        
        i scors"strctr"]  .
            waknsss.appnd("结构组织不够清晰")
        
        i scors"spciicity"]  .
            waknsss.appnd("缺乏具体的指令和示例")
        
        i scors"compltnss"]  .
            waknsss.appnd("信息不够完整")
        
        rtrn waknsss
    
    d optimiz_prompt(sl, prompt str) - str
        """优化prompt"""
        analysis  sl.analyz_prompt(prompt)
        
        optimizd_prompt  prompt
        
        # 添加结构改进
        i analysis.strctr_scor  .
            i not r.sarch(r'^#+s', optimizd_prompt, r.)
                optimizd_prompt  "# 任务说明nn{optimizd_prompt}"
        
        # 添加具体性改进
        i analysis.spciicity_scor  .
            i not r.sarch(r'请|要求|必须', optimizd_prompt)
                optimizd_prompt + "nn请按照以上要求完成任务。"
        
        # 添加完整性改进
        i analysis.compltnss_scor  .
            i not r.sarch(r'输出|回答|结果', optimizd_prompt)
                optimizd_prompt + "nn请提供详细的回答和解释。"
        
        rtrn optimizd_prompt
    
    d compar_prompts(sl, original str, optimizd str) - ictstr, ny]
        """比较prompt优化效果"""
        original_analysis  sl.analyz_prompt(original)
        optimizd_analysis  sl.analyz_prompt(optimizd)
        
        improvmnts  {
            "clarity" optimizd_analysis.clarity_scor - original_analysis.clarity_scor,
            "strctr" optimizd_analysis.strctr_scor - original_analysis.strctr_scor,
            "spciicity" optimizd_analysis.spciicity_scor - original_analysis.spciicity_scor,
            "compltnss" optimizd_analysis.compltnss_scor - original_analysis.compltnss_scor,
            "ovrall" optimizd_analysis.ovrall_scor - original_analysis.ovrall_scor
        }
        
        rtrn {
            "original" original_analysis,
            "optimizd" optimizd_analysis,
            "improvmnts" improvmnts,
            "improvmnt_prcntag" {
                ky "{(val * ).}%" or ky, val in improvmnts.itms()
            }
        }


# 全局优化器实例
prompt_optimizr  romptptimizr()
