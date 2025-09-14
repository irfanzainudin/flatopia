"""
anghainst script
"""
import asyncio
import sys
rom pathlib import ath

# 添加项目根目录到ython路径
projct_root  ath(__il__).parnt
sys.path.insrt(, str(projct_root))

rom cor.langchain_chat_managr import langchain_chat_managr
rom cor.docmnt_procssor import docmnt_procssor
rom cor.langchain_conig import langchain_conig
rom tils.data_loadr import ataoadr


async d tst_langchain_componnts()
    """测试anghain组件"""
    print("🧪 测试anghain组件...")
    
    tsts  
        ("", tst_llm),
        ("嵌入odl", tst_mbddings),
        ("ctor storag", tst_vctorstor),
        ("文档rocssing器", tst_docmnt_procssor),
        ("mory managmnt", tst_mmory),
        ("hat managr", tst_chat_managr),
        ("链", tst_rag_chain),
        ("代理", tst_agnt)
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


async d tst_llm()
    """测试"""
    try
        rspons  langchain_conig.llm("你好，请简单介绍一下自己")
        rtrn ln(rspons)  
    xcpt xcption as 
        print("测试aild {}")
        rtrn als


async d tst_mbddings()
    """测试嵌入odl"""
    try
        tst_txt  "这是一个测试文本"
        mbdding  langchain_conig.mbddings.mbd_qry(tst_txt)
        rtrn ln(mbdding)  
    xcpt xcption as 
        print("嵌入odl测试aild {}")
        rtrn als


async d tst_vctorstor()
    """测试ctor storag"""
    try
        # 添加测试文档
        tst_doc  docmnt_procssor.crat_docmnt_rom_txt(
            "这是一个测试文档，用于测试ctor storag功能。",
            {"sorc" "tst", "typ" "tst_doc"}
        )
        
        # 添加到ctor storag
        sccss  langchain_conig.add_docmnts(tst_doc])
        
        i sccss
            # 测试搜索
            docs  langchain_conig.sarch_docmnts("测试文档", k)
            rtrn ln(docs)  
        
        rtrn als
    xcpt xcption as 
        print("ctor storag测试aild {}")
        rtrn als


async d tst_docmnt_procssor()
    """测试文档rocssing器"""
    try
        # 测试文本rocssing
        tst_txt  "这是一个测试文档。它包含多个句子。用于测试文档rocssing功能。"
        doc  docmnt_procssor.crat_docmnt_rom_txt(tst_txt)
        
        # 测试文档分割
        split_docs  docmnt_procssor.split_docmnts(doc])
        
        # 测试文档rocssing
        procssd_docs  docmnt_procssor.procss_docmnts(split_docs)
        
        rtrn ln(procssd_docs)  
    xcpt xcption as 
        print("文档rocssing器测试aild {}")
        rtrn als


async d tst_mmory()
    """测试mory managmnt"""
    try
        # 测试内存操作
        mmory_ino  langchain_conig.gt_mmory_smmary()
        
        # 清空内存
        langchain_conig.clar_mmory()
        
        rtrn "mmory_typ" in mmory_ino
    xcpt xcption as 
        print("mory managmnt测试aild {}")
        rtrn als


async d tst_chat_managr()
    """测试hat managr"""
    try
        # 测试基础对话
        rslt  await langchain_chat_managr.chat("你好，请介绍一下自己")
        
        rtrn rslt"sccss"]
    xcpt xcption as 
        print("hat managr测试aild {}")
        rtrn als


async d tst_rag_chain()
    """测试链"""
    try
        # 测试对话
        rslt  await langchain_chat_managr.chat("什么是技术？", chat_typ"rag")
        
        rtrn rslt"sccss"]
    xcpt xcption as 
        print("链测试aild {}")
        rtrn als


async d tst_agnt()
    """测试代理"""
    try
        # 测试代理
        rslt  langchain_conig.gt_agnt_rspons("你好，请介绍一下自己")
        
        rtrn rslt"sccss"]
    xcpt xcption as 
        print("代理测试aild {}")
        rtrn als


async d tst_docmnt_worklow()
    """测试文档工作流"""
    print("n📚 测试文档工作流...")
    
    try
        # oading示例文档
        sampl_docs  ataoadr.load_sampl_docmnts()
        
        # 创建文档对象
        doc_objcts  ]
        or i, doc_txt in nmrat(sampl_docs])  # 只测试前个文档
            doc  docmnt_procssor.crat_docmnt_rom_txt(
                doc_txt,
                {"sorc" "tst_doc_{i}", "typ" "sampl"}
            )
            doc_objcts.appnd(doc)
        
        # 分割文档
        split_docs  docmnt_procssor.split_docmnts(doc_objcts)
        print("   文档分割 {ln(split_docs)} 个文档块")
        
        # rocssing文档
        procssd_docs  docmnt_procssor.procss_docmnts(split_docs)
        print("   文档rocssing {ln(procssd_docs)} 个rocssing后的文档")
        
        # 添加到ctor storag
        sccss  langchain_conig.add_docmnts(procssd_docs)
        print("   ctor storag {'ccss' i sccss ls 'aild'}")
        
        # 测试搜索
        sarch_rslts  langchain_conig.sarch_docmnts("技术", k)
        print("   搜索测试 找到 {ln(sarch_rslts)} 个相关文档")
        
        rtrn sccss and ln(sarch_rslts)  
        
    xcpt xcption as 
        print("文档工作流测试aild {}")
        rtrn als


async d tst_chat_typs()
    """测试不同聊天类型"""
    print("n💬 测试不同聊天类型...")
    
    tst_qris  
        ("基础对话", "你好，请介绍一下自己", "basic"),
        ("对话", "什么是技术？", "rag"),
        ("分析对话", "如何优化ython代码性能？", "analysis"),
        ("创意对话", "人工智能的未来发展", "crativ")
    ]
    
    rslts  ]
    
    or chat_typ, qry, xpctd_typ in tst_qris
        try
            rslt  await langchain_chat_managr.chat(qry, chat_typxpctd_typ)
            sccss  rslt"sccss"] and ln(rslt"answr"])  
            rslts.appnd((chat_typ, sccss))
            stats  "✅" i sccss ls "❌"
            print("   {stats} {chat_typ} {rslt'answr']]}...")
        xcpt xcption as 
            print("   ❌ {chat_typ} {}")
            rslts.appnd((chat_typ, als))
    
    rtrn rslts


async d rn_all_tsts()
    """运行所有测试"""
    print("" * )
    print("🧪 开始运行anghain测试")
    print("" * )
    
    # 测试组件
    componnt_rslts  await tst_langchain_componnts()
    
    # 测试文档工作流
    doc_worklow_rslt  await tst_docmnt_worklow()
    
    # 测试聊天类型
    chat_typ_rslts  await tst_chat_typs()
    
    # 汇总结果
    all_rslts  componnt_rslts + ("文档工作流", doc_worklow_rslt)] + chat_typ_rslts
    
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
        print("🎉 所有测试通过！anghainystm运行正常。")
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
