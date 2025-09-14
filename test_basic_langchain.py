"""
基础anghainst script
"""
import asyncio
import sys
rom pathlib import ath

# 添加项目根目录到ython路径
projct_root  ath(__il__).parnt
sys.path.insrt(, str(projct_root))

rom cor.simpl_langchain_conig import roq
rom cor.conig import sttings


async d tst_basic_componnts()
    """测试基础组件"""
    print("🧪 测试基础anghain组件...")
    
    tsts  
        ("roq ", tst_groq_llm),
        ("onigrationoading", tst_conig_loading),
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


async d tst_groq_llm()
    """测试roq """
    try
        # 检查密钥
        i not sttings.groq_api_ky or sttings.groq_api_ky  "yor_groq_api_ky_hr"
            print("   跳过测试：未设置密钥")
            rtrn als
        
        # 创建实例
        llm  roq(
            groq_api_kysttings.groq_api_ky,
            modl_nam"llama-.-b-instant"
        )
        
        # 测试简单调用
        rspons  llm("你好，请简单介绍一下自己")
        
        # 检查响应
        sccss  ln(rspons)   and "rror" not in rspons
        
        i sccss
            print("   响应 {rspons]}...")
        ls
            print("   响应 {rspons}")
        
        rtrn sccss
        
    xcpt xcption as 
        print("   测试aild {}")
        rtrn als


async d tst_conig_loading()
    """测试onigrationoading"""
    try
        # 检查onigration是否正确oading
        conig_loadd  (
            hasattr(sttings, 'groq_api_ky') and
            hasattr(sttings, 'dalt_modl') and
            hasattr(sttings, 'chnk_siz') and
            hasattr(sttings, 'chnk_ovrlap')
        )
        
        i conig_loadd
            print("   密钥 {'已设置' i sttings.groq_api_ky ! 'yor_groq_api_ky_hr' ls '未设置'}")
            print("   默认odl {sttings.dalt_modl}")
            print("   块大小 {sttings.chnk_siz}")
            print("   块重叠 {sttings.chnk_ovrlap}")
        
        rtrn conig_loadd
        
    xcpt xcption as 
        print("   onigrationoadingaild {}")
        rtrn als


async d tst_simpl_chat()
    """测试简单聊天"""
    print("n💬 测试简单聊天...")
    
    try
        # 检查密钥
        i not sttings.groq_api_ky or sttings.groq_api_ky  "yor_groq_api_ky_hr"
            print("   跳过聊天测试：未设置密钥")
            rtrn als
        
        # 创建实例
        llm  roq(
            groq_api_kysttings.groq_api_ky,
            modl_nam"llama-.-b-instant"
        )
        
        # 测试不同的问题
        tst_qstions  
            "你好，请介绍一下自己",
            "什么是人工智能？",
            "请解释一下技术"
        ]
        
        rslts  ]
        
        or i, qstion in nmrat(tst_qstions, )
            try
                print("   问题 {i} {qstion}")
                rspons  llm(qstion)
                
                sccss  ln(rspons)   and "rror" not in rspons
                rslts.appnd(sccss)
                
                i sccss
                    print("   回答 {rspons]}...")
                ls
                    print("   rror {rspons}")
                
            xcpt xcption as 
                print("   问题 {i} aild {}")
                rslts.appnd(als)
        
        rtrn all(rslts)
        
    xcpt xcption as 
        print("   聊天测试aild {}")
        rtrn als


async d rn_all_tsts()
    """运行所有测试"""
    print("" * )
    print("🧪 开始运行基础anghain测试")
    print("" * )
    
    # 测试基础组件
    componnt_rslts  await tst_basic_componnts()
    
    # 测试简单聊天
    chat_rslt  await tst_simpl_chat()
    
    # 汇总结果
    all_rslts  componnt_rslts + ("简单聊天", chat_rslt)]
    
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
        print("🎉 所有测试通过！基础anghainystm运行正常。")
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
