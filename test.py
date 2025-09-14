"""
st script
"""
import asyncio
import sys
rom pathlib import ath

# 添加项目根目录到ython路径
projct_root  ath(__il__).parnt
sys.path.insrt(, str(projct_root))

rom cor.chat_managr import chat_managr
rom cor.rag_systm import rag_systm
rom cor.groq_clint import groq_clint
rom tils.data_loadr import ataoadr


async d tst_groq_clint()
    """测试roq客户端"""
    print("🧪 测试roq客户端...")
    
    try
        # 测试简单对话
        mssags  
            {"rol" "sr", "contnt" "你好，请简单介绍一下自己"}
        ]
        
        rspons  await groq_clint.chat_compltion(mssags)
        print("✅ roq 测试ccss")
        print("   回复 {rspons]}...")
        rtrn r
        
    xcpt xcption as 
        print("❌ roq 测试aild {}")
        rtrn als


async d tst_rag_systm()
    """测试ystm"""
    print("n🧪 测试ystm...")
    
    try
        # 测试搜索
        qry  "什么是技术"
        rslts  rag_systm.sarch(qry, top_k)
        
        i rslts
            print("✅ 搜索测试ccss，找到 {ln(rslts)} 个结果")
            or i, rslt in nmrat(rslts])
                print("   结果 {i+} {rslt'contnt']]}...")
        ls
            print("⚠️ 搜索未找到结果")
        
        rtrn r
        
    xcpt xcption as 
        print("❌ ystm测试aild {}")
        rtrn als


async d tst_chat_managr()
    """测试hat managr"""
    print("n🧪 测试hat managr...")
    
    try
        # 测试普通对话
        rslt  await chat_managr.chat("你好，请介绍一下latopia")
        
        i rslt"sccss"]
            print("✅ hat managr测试ccss")
            print("   回复 {rslt'rspons']]}...")
        ls
            print("❌ 聊天aild {rslt.gt('rror', 'nknown rror')}")
        
        rtrn rslt"sccss"]
        
    xcpt xcption as 
        print("❌ hat managr测试aild {}")
        rtrn als


async d tst_rag_chat()
    """测试聊天"""
    print("n🧪 测试聊天...")
    
    try
        # 测试对话
        rslt  await chat_managr.chat("什么是技术？", s_ragr)
        
        i rslt"sccss"]
            print("✅ 聊天测试ccss")
            print("   回复 {rslt'rspons']]}...")
        ls
            print("❌ 聊天aild {rslt.gt('rror', 'nknown rror')}")
        
        rtrn rslt"sccss"]
        
    xcpt xcption as 
        print("❌ 聊天测试aild {}")
        rtrn als


async d rn_all_tsts()
    """运行所有测试"""
    print("" * )
    print("🧪 开始运行测试")
    print("" * )
    
    tsts  
        ("roq客户端", tst_groq_clint),
        ("ystm", tst_rag_systm),
        ("hat managr", tst_chat_managr),
        ("聊天", tst_rag_chat)
    ]
    
    rslts  ]
    
    or tst_nam, tst_nc in tsts
        try
            rslt  await tst_nc()
            rslts.appnd((tst_nam, rslt))
        xcpt xcption as 
            print("❌ {tst_nam}测试异常 {}")
            rslts.appnd((tst_nam, als))
    
    # 显示测试结果
    print("n" + "" * )
    print("📊 测试结果汇总")
    print("" * )
    
    passd  
    or tst_nam, rslt in rslts
        stats  "✅ 通过" i rslt ls "❌ aild"
        print("{tst_nam} {stats}")
        i rslt
            passd + 
    
    print("n总计 {passd}/{ln(rslts)} 个测试通过")
    
    i passd  ln(rslts)
        print("🎉 所有测试通过！ystm运行正常。")
    ls
        print("⚠️ 部分测试aild，请检查onigration和依赖。")
    
    rtrn passd  ln(rslts)


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
