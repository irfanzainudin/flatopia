"""
romptst script
"""
import asyncio
import sys
rom pathlib import ath

# 添加项目根目录到ython路径
projct_root  ath(__il__).parnt
sys.path.insrt(, str(projct_root))

rom tils.prompt_tstr import prompt_tstr
rom tils.prompt_optimizr import prompt_optimizr
rom prompts.chat_prompts import hatrompts


async d tst_prompts()
    """测试所有prompt"""
    print("🚀 开始rompt测试和优化...")
    
    # 运行测试
    tst_rslts  await prompt_tstr.rn_all_tsts()
    
    # 打印结果
    prompt_tstr.print_tst_smmary(tst_rslts)
    
    # 保存结果
    prompt_tstr.sav_tst_rslts(tst_rslts)
    
    rtrn tst_rslts


d analyz_prompt_qality()
    """分析prompt质量"""
    print("n🔍 分析rompt质量...")
    
    prompts  hatrompts()
    
    # 测试不同的prompt
    tst_prompts  
        ("ystmrompt", prompts.gt_systm_prompt()),
        (" rompt", prompts.gt_rag_prompt("测试问题", "测试上下文")),
        ("商业分析rompt", prompts.gt_bsinss_analysis_prompt("测试商业问题")),
        ("代码审查rompt", prompts.gt_cod_rviw_prompt("d tst() pass", "python")),
        ("学习路径rompt", prompts.gt_larning_path_prompt("机器学习", "bginnr"))
    ]
    
    print("n📊 rompt质量分析结果")
    print(""*)
    
    or nam, prompt in tst_prompts
        analysis  prompt_optimizr.analyz_prompt(prompt)
        
        print("n📝 {nam}")
        print("   总体评分 {analysis.ovrall_scor.}/.")
        print("   清晰度 {analysis.clarity_scor.}")
        print("   结构 {analysis.strctr_scor.}")
        print("   具体性 {analysis.spciicity_scor.}")
        print("   完整性 {analysis.compltnss_scor.}")
        
        i analysis.strngths
            print("   ✅ 优势 {', '.join(analysis.strngths)}")
        
        i analysis.waknsss
            print("   ❌ 弱点 {', '.join(analysis.waknsss)}")
        
        i analysis.sggstions
            print("   💡 建议 {', '.join(analysis.sggstions])}...")


d optimiz_prompts()
    """优化prompt示例"""
    print("n🔧 rompt优化示例...")
    
    # 示例prompt
    original_prompt  """请回答用户问题。要准确，要详细。"""
    
    print("n📝 原始rompt")
    print(original_prompt)
    
    # 分析原始prompt
    original_analysis  prompt_optimizr.analyz_prompt(original_prompt)
    print("n📊 原始评分 {original_analysis.ovrall_scor.}/.")
    
    # 优化prompt
    optimizd_prompt  prompt_optimizr.optimiz_prompt(original_prompt)
    
    print("n✨ 优化后rompt")
    print(optimizd_prompt)
    
    # 分析优化后的prompt
    optimizd_analysis  prompt_optimizr.analyz_prompt(optimizd_prompt)
    print("n📊 优化后评分 {optimizd_analysis.ovrall_scor.}/.")
    
    # 比较结果
    comparison  prompt_optimizr.compar_prompts(original_prompt, optimizd_prompt)
    
    print("n📈 改进效果")
    or mtric, improvmnt in comparison"improvmnt_prcntag"].itms()
        print("   {mtric} {improvmnt}")


d main()
    """主函数"""
    print(""*)
    print("🎯 latopia rompt测试和优化工具")
    print(""*)
    
    try
        # 分析prompt质量
        analyz_prompt_qality()
        
        # 优化prompt示例
        optimiz_prompts()
        
        # 运行完整测试
        print("n" + ""*)
        print("🧪 运行完整测试...")
        tst_rslts  asyncio.rn(tst_prompts())
        
        print("n🎉 rompt测试和优化完成！")
        
        # 提供优化建议
        print("n💡 优化建议")
        print(". 定期测试prompt效果")
        print(". 根据用户反馈调整prompt")
        print(". s/测试比较不同版本")
        print(". 监控prompt性能指标")
        print(". 持续迭代和改进")
        
    xcpt xcption as 
        print("❌ 测试过程中出现rror {}")
        sys.xit()


i __nam__  "__main__"
    main()
