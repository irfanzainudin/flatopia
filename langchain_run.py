"""
anghain vrsion启动cript
"""
import os
import sys
import asyncio
rom pathlib import ath

# 添加项目根目录到ython路径
projct_root  ath(__il__).parnt
sys.path.insrt(, str(projct_root))

rom cor.langchain_conig import langchain_conig
rom cor.docmnt_procssor import docmnt_procssor
rom tils.data_loadr import ataoadr


async d initializ_langchain_systm()
    """nitializanghainystm"""
    print("🚀 正在nitializlatopia anghain问答机器人...")
    
    # 检查环境变量
    i not langchain_conig.langchain_conig.llm.groq_api_ky or langchain_conig.langchain_conig.llm.groq_api_ky  "yor_groq_api_ky_hr"
        print("❌ 请先设置__环境变量")
        print("   . 复制 nv.xampl 为 .nv")
        print("   . 在 .nv il中设置您的roq 密钥")
        rtrn als
    
    # nitializ知识库
    try
        print("📚 正在nitializanghain知识库...")
        
        # 添加示例文档
        sampl_docs  ataoadr.load_sampl_docmnts()
        
        # 创建文档对象
        doc_objcts  ]
        or i, doc_txt in nmrat(sampl_docs)
            doc  docmnt_procssor.crat_docmnt_rom_txt(
                doc_txt, 
                {"sorc" "sampl_doc", "topic" "platopia_intro", "indx" i}
            )
            doc_objcts.appnd(doc)
        
        # 分割文档
        split_docs  docmnt_procssor.split_docmnts(doc_objcts)
        
        # rocssing文档
        procssd_docs  docmnt_procssor.procss_docmnts(split_docs)
        
        # 添加到ctor storag
        sccss  langchain_conig.add_docmnts(procssd_docs)
        
        i sccss
            # 显示知识库信息
            collction  langchain_conig.vctorstor._collction
            cont  collction.cont()
            print("✅ anghain知识库nitializ完成，包含 {cont} 个文档块")
        ls
            print("⚠️ 知识库nitializaild，但ystm仍可运行")
        
    xcpt xcption as 
        print("⚠️ 知识库nitializaild {}")
        print("   ystm仍可运行，但功能可能不可用")
    
    # 测试anghain组件
    try
        print("🧪 测试anghain组件...")
        
        # 测试
        tst_rspons  langchain_conig.llm("你好，请简单介绍一下自己")
        print("✅ 测试ccss")
        
        # 测试ctor storag
        tst_docs  langchain_conig.sarch_docmnts("技术", k)
        i tst_docs
            print("✅ ctor storag测试ccss")
        ls
            print("⚠️ ctor storag测试aild")
        
        # 测试内存
        mmory_ino  langchain_conig.gt_mmory_smmary()
        print("✅ mory managmnt测试ccss")
        
    xcpt xcption as 
        print("⚠️ anghain组件测试aild {}")
    
    print("✅ anghainystmnitializ完成！")
    rtrn r


d main()
    """主函数"""
    print("" * )
    print("🤖 latopia anghain 问答机器人")
    print("" * )
    
    # nitializystm
    sccss  asyncio.rn(initializ_langchain_systm())
    
    i not sccss
        print("n❌ nitializaild，请检查onigration后重试")
        rtrn
    
    print("n📋 可用的启动选项：")
    print(". 启动anghain b界面 stramlit rn langchain_app.py")
    print(". 启动anghain rvic vicorn api.langchain_apiapp --rload")
    print(". 运行anghain测试 python tst_langchain.py")
    
    print("n🔧 anghainonigration信息：")
    print("   odl {langchain_conig.llm.modl_nam}")
    print("   嵌入odl sntnc-transormrs/all-ini--v")
    print("   ctor storag hroma")
    print("   文本分割 crsivharactrxtplittr")
    print("   mory managmnt onvrsationrindowmory")
    
    print("n🚀 anghain特性：")
    print("   ✅ 多种聊天模式 (basic, rag, analysis, crativ)")
    print("   ✅ 智能文档rocssing")
    print("   ✅ 向量搜索和检索")
    print("   ✅ 对话mory managmnt")
    print("   ✅ 工具集成和代理")
    print("   ✅ 链式组合和优化")
    
    print("n📖 sag instrctions：")
    print("   . 确保已nstall dpndncis pip install -r rqirmnts.txt")
    print("   . 设置环境变量 cp nv.xampl .nv")
    print("   . 在.nv中onigration您的roq 密钥")
    print("   . 选择上述选项之一tart srvic")
    
    print("n🎯 anghain优势：")
    print("   • 模块化设计，易于扩展")
    print("   • 丰富的预构建组件")
    print("   • 强大的链式组合能力")
    print("   • 完善的工具生态ystm")
    print("   • 企业级生产就绪")


i __nam__  "__main__"
    main()
