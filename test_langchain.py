"""
LangChainTest script
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.langchain_chat_manager import langchain_chat_manager
from core.document_processor import document_processor
from core.langchain_config import langchain_config
from utils.data_loader import DataLoader


async def test_langchain_components():
    """测试LangChain组件"""
    print("🧪 测试LangChain组件...")
    
    tests = [
        ("LLM", test_llm),
        ("嵌入Model", test_embeddings),
        ("Vector storage", test_vectorstore),
        ("文档Processing器", test_document_processor),
        ("Memory management", test_memory),
        ("Chat manager", test_chat_manager),
        ("RAG链", test_rag_chain),
        ("代理", test_agent)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n🔍 测试 {test_name}...")
            result = await test_func()
            results.append((test_name, result))
            status = "✅ 通过" if result else "❌ Failed"
            print(f"{status} {test_name}")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    return results


async def test_llm():
    """测试LLM"""
    try:
        response = langchain_config.llm("你好，请简单介绍一下自己")
        return len(response) > 0
    except Exception as e:
        print(f"LLM测试Failed: {e}")
        return False


async def test_embeddings():
    """测试嵌入Model"""
    try:
        test_text = "这是一个测试文本"
        embedding = langchain_config.embeddings.embed_query(test_text)
        return len(embedding) > 0
    except Exception as e:
        print(f"嵌入Model测试Failed: {e}")
        return False


async def test_vectorstore():
    """测试Vector storage"""
    try:
        # 添加测试文档
        test_doc = document_processor.create_document_from_text(
            "这是一个测试文档，用于测试Vector storage功能。",
            {"source": "test", "type": "test_doc"}
        )
        
        # 添加到Vector storage
        success = langchain_config.add_documents([test_doc])
        
        if success:
            # 测试搜索
            docs = langchain_config.search_documents("测试文档", k=1)
            return len(docs) > 0
        
        return False
    except Exception as e:
        print(f"Vector storage测试Failed: {e}")
        return False


async def test_document_processor():
    """测试文档Processing器"""
    try:
        # 测试文本Processing
        test_text = "这是一个测试文档。它包含多个句子。用于测试文档Processing功能。"
        doc = document_processor.create_document_from_text(test_text)
        
        # 测试文档分割
        split_docs = document_processor.split_documents([doc])
        
        # 测试文档Processing
        processed_docs = document_processor.process_documents(split_docs)
        
        return len(processed_docs) > 0
    except Exception as e:
        print(f"文档Processing器测试Failed: {e}")
        return False


async def test_memory():
    """测试Memory management"""
    try:
        # 测试内存操作
        memory_info = langchain_config.get_memory_summary()
        
        # 清空内存
        langchain_config.clear_memory()
        
        return "memory_type" in memory_info
    except Exception as e:
        print(f"Memory management测试Failed: {e}")
        return False


async def test_chat_manager():
    """测试Chat manager"""
    try:
        # 测试基础对话
        result = await langchain_chat_manager.chat("你好，请介绍一下自己")
        
        return result["success"]
    except Exception as e:
        print(f"Chat manager测试Failed: {e}")
        return False


async def test_rag_chain():
    """测试RAG链"""
    try:
        # 测试RAG对话
        result = await langchain_chat_manager.chat("什么是RAG技术？", chat_type="rag")
        
        return result["success"]
    except Exception as e:
        print(f"RAG链测试Failed: {e}")
        return False


async def test_agent():
    """测试代理"""
    try:
        # 测试代理
        result = langchain_config.get_agent_response("你好，请介绍一下自己")
        
        return result["success"]
    except Exception as e:
        print(f"代理测试Failed: {e}")
        return False


async def test_document_workflow():
    """测试文档工作流"""
    print("\n📚 测试文档工作流...")
    
    try:
        # Loading示例文档
        sample_docs = DataLoader.load_sample_documents()
        
        # 创建文档对象
        doc_objects = []
        for i, doc_text in enumerate(sample_docs[:2]):  # 只测试前2个文档
            doc = document_processor.create_document_from_text(
                doc_text,
                {"source": f"test_doc_{i}", "type": "sample"}
            )
            doc_objects.append(doc)
        
        # 分割文档
        split_docs = document_processor.split_documents(doc_objects)
        print(f"   文档分割: {len(split_docs)} 个文档块")
        
        # Processing文档
        processed_docs = document_processor.process_documents(split_docs)
        print(f"   文档Processing: {len(processed_docs)} 个Processing后的文档")
        
        # 添加到Vector storage
        success = langchain_config.add_documents(processed_docs)
        print(f"   Vector storage: {'Success' if success else 'Failed'}")
        
        # 测试搜索
        search_results = langchain_config.search_documents("RAG技术", k=3)
        print(f"   搜索测试: 找到 {len(search_results)} 个相关文档")
        
        return success and len(search_results) > 0
        
    except Exception as e:
        print(f"文档工作流测试Failed: {e}")
        return False


async def test_chat_types():
    """测试不同聊天类型"""
    print("\n💬 测试不同聊天类型...")
    
    test_queries = [
        ("基础对话", "你好，请介绍一下自己", "basic"),
        ("RAG对话", "什么是RAG技术？", "rag"),
        ("分析对话", "如何优化Python代码性能？", "analysis"),
        ("创意对话", "人工智能的未来发展", "creative")
    ]
    
    results = []
    
    for chat_type, query, expected_type in test_queries:
        try:
            result = await langchain_chat_manager.chat(query, chat_type=expected_type)
            success = result["success"] and len(result["answer"]) > 0
            results.append((chat_type, success))
            status = "✅" if success else "❌"
            print(f"   {status} {chat_type}: {result['answer'][:50]}...")
        except Exception as e:
            print(f"   ❌ {chat_type}: {e}")
            results.append((chat_type, False))
    
    return results


async def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 开始运行LangChain测试")
    print("=" * 60)
    
    # 测试组件
    component_results = await test_langchain_components()
    
    # 测试文档工作流
    doc_workflow_result = await test_document_workflow()
    
    # 测试聊天类型
    chat_type_results = await test_chat_types()
    
    # 汇总结果
    all_results = component_results + [("文档工作流", doc_workflow_result)] + chat_type_results
    
    # 显示测试结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = 0
    for test_name, result in all_results:
        status = "✅ 通过" if result else "❌ Failed"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(all_results)} 个测试通过")
    
    if passed == len(all_results):
        print("🎉 所有测试通过！LangChainSystem运行正常。")
    else:
        print("⚠️ 部分测试Failed，请检查Configuration和依赖。")
    
    return passed == len(all_results)


def main():
    """主函数"""
    try:
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试运行异常: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
