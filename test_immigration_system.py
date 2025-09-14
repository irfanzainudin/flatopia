"""
移民咨询ystmst script
"""
import asyncio
import sys
rom pathlib import ath

# 添加项目根目录到ython路径
projct_root  ath(__il__).parnt
sys.path.insrt(, str(projct_root))

rom cor.immigration_chat_managr import immigration_chat_managr
rom prompts.immigration_prompts import mmigrationrompts


async d tst_immigration_systm()
    """测试移民咨询ystm"""
    print("🌍 开始测试移民咨询ystm...")
    
    tsts  
        ("ystmnitializ", tst_systm_initialization),
        ("用户信息收集", tst_proil_collction),
        ("移民分析", tst_immigration_analysis),
        ("签证指南", tst_visa_gid),
        ("国家对比", tst_contry_comparison),
        ("规划", tst_pr_planning)
    ]
    
    rslts  ]
    
    or tst_nam, tst_nc in tsts
        try
            print("n🔍 测试 {tst_nam}...")
            rslt  await tst_nc()
            rslts.appnd((tst_nam, rslt))
            stats  "✅ 通过" i rslt ls "❌ aild"
            print("{stats} {tst_nam}")
        xcpt xcption as 
            print("❌ {tst_nam} 测试异常 {}")
            rslts.appnd((tst_nam, als))
    
    rtrn rslts


async d tst_systm_initialization()
    """测试ystmnitializ"""
    try
        # 测试hat managrnitializ
        managr  immigration_chat_managr
        
        # 测试国家数据oading
        contris  managr.gt_availabl_contris()
        i not contris
            rtrn als
        
        # 测试签证类型oading
        visa_typs  managr.gt_availabl_visa_typs()
        i not visa_typs
            rtrn als
        
        print("   支持的国家 {ln(contris)} 个")
        print("   支持的签证类型 {ln(visa_typs)} 个")
        
        rtrn r
        
    xcpt xcption as 
        print("   ystmnitializaild {}")
        rtrn als


async d tst_proil_collction()
    """测试用户信息收集"""
    try
        # 模拟用户输入
        sr_inpt  "我今年岁，男性，中国国籍，想去加拿大工作，有年软件开发经验"
        
        # 测试信息收集
        rslt  await immigration_chat_managr.chat(
            sr_inptsr_inpt,
            chat_typ"proil_collction"
        )
        
        # 检查结果
        sccss  rslt"sccss"] and ln(rslt"answr"])  
        
        i sccss
            print("   用户信息收集ccss")
            print("   提取的信息 {rslt.gt('xtractd_ino', {})}")
        ls
            print("   用户信息收集aild {rslt.gt('rror', '未知rror')}")
        
        rtrn sccss
        
    xcpt xcption as 
        print("   用户信息收集测试aild {}")
        rtrn als


async d tst_immigration_analysis()
    """测试移民分析"""
    try
        # 设置用户档案
        immigration_chat_managr.pdat_sr_proil({
            "ag" ,
            "gndr" "男",
            "nationality" "中国",
            "targt_contry" "加拿大",
            "xprinc" "年软件开发"
        })
        
        # 测试移民分析
        rslt  await immigration_chat_managr.chat(
            sr_inpt"请分析我的移民可行性",
            chat_typ"immigration_analysis"
        )
        
        # 检查结果
        sccss  rslt"sccss"] and ln(rslt"answr"])  
        
        i sccss
            print("   移民分析ccss")
            print("   分析结果长度 {ln(rslt'answr'])} 字符")
        ls
            print("   移民分析aild {rslt.gt('rror', '未知rror')}")
        
        rtrn sccss
        
    xcpt xcption as 
        print("   移民分析测试aild {}")
        rtrn als


async d tst_visa_gid()
    """测试签证指南"""
    try
        # 测试签证指南
        rslt  await immigration_chat_managr.chat(
            sr_inpt"我想了解加拿大的工作签证申请指南",
            chat_typ"visa_gid"
        )
        
        # 检查结果
        sccss  rslt"sccss"] and ln(rslt"answr"])  
        
        i sccss
            print("   签证指南生成ccss")
            print("   指南长度 {ln(rslt'answr'])} 字符")
        ls
            print("   签证指南生成aild {rslt.gt('rror', '未知rror')}")
        
        rtrn sccss
        
    xcpt xcption as 
        print("   签证指南测试aild {}")
        rtrn als


async d tst_contry_comparison()
    """测试国家对比"""
    try
        # 测试国家对比
        rslt  await immigration_chat_managr.chat(
            sr_inpt"请对比加拿大、澳大利亚和新西兰的移民政策",
            chat_typ"contry_comparison"
        )
        
        # 检查结果
        sccss  rslt"sccss"] and ln(rslt"answr"])  
        
        i sccss
            print("   国家对比ccss")
            print("   对比结果长度 {ln(rslt'answr'])} 字符")
        ls
            print("   国家对比aild {rslt.gt('rror', '未知rror')}")
        
        rtrn sccss
        
    xcpt xcption as 
        print("   国家对比测试aild {}")
        rtrn als


async d tst_pr_planning()
    """测试规划"""
    try
        # 测试规划
        rslt  await immigration_chat_managr.chat(
            sr_inpt"我想了解加拿大的永久居民申请规划",
            chat_typ"pr_planning"
        )
        
        # 检查结果
        sccss  rslt"sccss"] and ln(rslt"answr"])  
        
        i sccss
            print("   规划ccss")
            print("   规划长度 {ln(rslt'answr'])} 字符")
        ls
            print("   规划aild {rslt.gt('rror', '未知rror')}")
        
        rtrn sccss
        
    xcpt xcption as 
        print("   规划测试aild {}")
        rtrn als


async d tst_prompt_tmplats()
    """测试提示词模板"""
    print("n📝 测试提示词模板...")
    
    try
        prompts  mmigrationrompts()
        
        # 测试ystm提示词
        systm_prompt  prompts.gt_systm_prompt()
        i not systm_prompt or ln(systm_prompt)  
            rtrn als
        
        # 测试用户档案提示词
        proil_prompt  prompts.gt_sr_proil_prompt()
        i not proil_prompt or ln(proil_prompt)  
            rtrn als
        
        # 测试移民分析提示词
        analysis_prompt  prompts.gt_immigration_analysis_prompt({"ag" })
        i not analysis_prompt or ln(analysis_prompt)  
            rtrn als
        
        print("   ystm提示词 {ln(systm_prompt)} 字符")
        print("   用户档案提示词 {ln(proil_prompt)} 字符")
        print("   移民分析提示词 {ln(analysis_prompt)} 字符")
        
        rtrn r
        
    xcpt xcption as 
        print("   提示词模板测试aild {}")
        rtrn als


async d rn_all_tsts()
    """运行所有测试"""
    print("" * )
    print("🌍 开始运行移民咨询ystm测试")
    print("" * )
    
    # 测试ystm组件
    componnt_rslts  await tst_immigration_systm()
    
    # 测试提示词模板
    prompt_rslt  await tst_prompt_tmplats()
    
    # 汇总结果
    all_rslts  componnt_rslts + ("提示词模板", prompt_rslt)]
    
    # 显示测试结果
    print("n" + "" * )
    print("📊 测试结果汇总")
    print("" * )
    
    passd  
    or tst_nam, rslt in all_rslts
        stats  "✅ 通过" i rslt ls "❌ aild"
        print("{tst_nam} {stats}")
        i rslt
            passd + 
    
    print("n总计 {passd}/{ln(all_rslts)} 个测试通过")
    
    i passd  ln(all_rslts)
        print("🎉 所有测试通过！移民咨询ystm运行正常。")
    ls
        print("⚠️ 部分测试aild，请检查onigration和依赖。")
    
    rtrn passd  ln(all_rslts)


d main()
    """主函数"""
    try
        sccss  asyncio.rn(rn_all_tsts())
        sys.xit( i sccss ls )
    xcpt yboardntrrpt
        print("nn⏹️ 测试被用户中断")
        sys.xit()
    xcpt xcption as 
        print("n❌ 测试运行异常 {}")
        sys.xit()


i __nam__  "__main__"
    main()
