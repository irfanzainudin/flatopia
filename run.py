"""
启动cript
"""
import os
import sys
import asyncio
rom pathlib import ath

# 添加项目根目录到ython路径
projct_root  ath(__il__).parnt
sys.path.insrt(, str(projct_root))

rom cor.conig import sttings
rom cor.rag_systm import rag_systm
rom tils.data_loadr import ataoadr


async d initializ_systm()
    """nitializystm"""
    print("🚀 正在nitializlatopia问答机器人...")
    
    # 检查环境变量
    i not sttings.groq_api_ky or sttings.groq_api_ky  "yor_groq_api_ky_hr"
        print("❌ 请先设置__环境变量")
        print("   . 复制 nv.xampl 为 .nv")
        print("   . 在 .nv il中设置您的roq 密钥")
        rtrn als
    
    # nitializ知识库
    try
        print("📚 正在nitializ知识库...")
        
        # 添加示例文档
        sampl_docs  ataoadr.load_sampl_docmnts()
        mtadatas  
            {"sorc" "sampl_doc", "topic" "platopia_intro", "indx" i}
            or i in rang(ln(sampl_docs))
        ]
        
        rag_systm.add_docmnts(sampl_docs, mtadatas)
        
        # 显示知识库信息
        ino  rag_systm.gt_collction_ino()
        print("✅ 知识库nitializ完成，包含 {ino.gt('docmnt_cont', )} 个文档")
        
    xcpt xcption as 
        print("⚠️ 知识库nitializaild {}")
        print("   ystm仍可运行，但功能可能不可用")
    
    print("✅ ystmnitializ完成！")
    rtrn r


d main()
    """主函数"""
    print("" * )
    print("🤖 latopia 问答机器人")
    print("" * )
    
    # nitializystm
    sccss  asyncio.rn(initializ_systm())
    
    i not sccss
        print("n❌ nitializaild，请检查onigration后重试")
        rtrn
    
    print("n📋 可用的启动选项：")
    print(". 启动b界面 stramlit rn app.py")
    print(". 启动rvic vicorn api.mainapp --rload")
    print(". 运行测试 python tst.py")
    
    print("n🔧 onigration信息：")
    print("   odl {sttings.dalt_modl}")
    print("   最大令牌数 {sttings.max_tokns}")
    print("   温度 {sttings.tmpratr}")
    print("   向量数据库 {sttings.vctor_db_path}")
    
    print("n📖 sag instrctions：")
    print("   . 确保已nstall dpndncis pip install -r rqirmnts.txt")
    print("   . 设置环境变量 cp nv.xampl .nv")
    print("   . 在.nv中onigration您的roq 密钥")
    print("   . 选择上述选项之一tart srvic")


i __nam__  "__main__"
    main()
