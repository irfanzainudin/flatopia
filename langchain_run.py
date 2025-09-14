"""
LangChain version启动Script
"""
import os
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.langchain_config import langchain_config
from core.document_processor import document_processor
from utils.data_loader import DataLoader


async def initialize_langchain_system():
    """InitializeLangChainSystem"""
    print("🚀 正在InitializeFlatopia LangChainQ问答A机器人...")
    
    # 检查环境变量
    if not langchain_config.langchain_config.llm.groq_api_key or langchain_config.langchain_config.llm.groq_api_key == "your_groq_api_key_here":
        print("❌ 请先设置GROQ_API_KEY环境变量")
        print("   1. 复制 env.example 为 .env")
        print("   2. 在 .env File中设置您的Groq API密钥")
        return False
    
    # Initialize知识库
    try:
        print("📚 正在InitializeLangChain知识库...")
        
        # 添加示例文档
        sample_docs = DataLoader.load_sample_documents()
        
        # 创建文档对象
        doc_objects = []
        for i, doc_text in enumerate(sample_docs):
            doc = document_processor.create_document_from_text(
                doc_text, 
                {"source": "sample_doc", "topic": "platopia_intro", "index": i}
            )
            doc_objects.append(doc)
        
        # 分割文档
        split_docs = document_processor.split_documents(doc_objects)
        
        # Processing文档
        processed_docs = document_processor.process_documents(split_docs)
        
        # 添加到Vector storage
        success = langchain_config.add_documents(processed_docs)
        
        if success:
            # 显示知识库信息
            collection = langchain_config.vectorstore._collection
            count = collection.count()
            print(f"✅ LangChain知识库Initialize完成，包含 {count} 个文档块")
        else:
            print("⚠️ 知识库InitializeFailed，但System仍可运行")
        
    except Exception as e:
        print(f"⚠️ 知识库InitializeFailed: {e}")
        print("   System仍可运行，但RAG功能可能不可用")
    
    # 测试LangChain组件
    try:
        print("🧪 测试LangChain组件...")
        
        # 测试LLM
        test_response = langchain_config.llm("你好，请简单介绍一下自己")
        print("✅ LLM测试Success")
        
        # 测试Vector storage
        test_docs = langchain_config.search_documents("RAG技术", k=1)
        if test_docs:
            print("✅ Vector storage测试Success")
        else:
            print("⚠️ Vector storage测试Failed")
        
        # 测试内存
        memory_info = langchain_config.get_memory_summary()
        print("✅ Memory management测试Success")
        
    except Exception as e:
        print(f"⚠️ LangChain组件测试Failed: {e}")
    
    print("✅ LangChainSystemInitialize完成！")
    return True


def main():
    """主函数"""
    print("=" * 60)
    print("🤖 Flatopia LangChain Q问答A机器人")
    print("=" * 60)
    
    # InitializeSystem
    success = asyncio.run(initialize_langchain_system())
    
    if not success:
        print("\n❌ InitializeFailed，请检查Configuration后重试")
        return
    
    print("\n📋 可用的启动选项：")
    print("1. 启动LangChain Web界面: streamlit run langchain_app.py")
    print("2. 启动LangChain APIService: uvicorn api.langchain_api:app --reload")
    print("3. 运行LangChain测试: python test_langchain.py")
    
    print("\n🔧 LangChainConfiguration信息：")
    print(f"   LLMModel: {langchain_config.llm.model_name}")
    print(f"   嵌入Model: sentence-transformers/all-MiniLM-L6-v2")
    print(f"   Vector storage: ChromaDB")
    print(f"   文本分割: RecursiveCharacterTextSplitter")
    print(f"   Memory management: ConversationBufferWindowMemory")
    
    print("\n🚀 LangChain特性：")
    print("   ✅ 多种聊天模式 (basic, rag, analysis, creative)")
    print("   ✅ 智能文档Processing")
    print("   ✅ 向量搜索和检索")
    print("   ✅ 对话Memory management")
    print("   ✅ 工具集成和代理")
    print("   ✅ 链式组合和优化")
    
    print("\n📖 Usage instructions：")
    print("   1. 确保已Install dependencies: pip install -r requirements.txt")
    print("   2. 设置环境变量: cp env.example .env")
    print("   3. 在.env中Configuration您的Groq API密钥")
    print("   4. 选择上述选项之一Start service")
    
    print("\n🎯 LangChain优势：")
    print("   • 模块化设计，易于扩展")
    print("   • 丰富的预构建组件")
    print("   • 强大的链式组合能力")
    print("   • 完善的工具生态System")
    print("   • 企业级生产就绪")


if __name__ == "__main__":
    main()
