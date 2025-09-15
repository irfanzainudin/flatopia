"""
Test script
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.chat_manager import chat_manager
from core.rag_system import rag_system
from core.groq_client import groq_client
from utils.data_loader import DataLoader


async def test_groq_client():
    """测试Groq客户端"""
    print("🧪 测试Groq客户端...")
    
    try:
        # 测试简单对话
        messages = [
            {"role": "user", "content": "你好，请简单介绍一下自己"}
        ]
        
        response = await groq_client.chat_completion(messages)
        print(f"✅ Groq API测试Success")
        print(f"   回复: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Groq API测试Failed: {e}")
        return False


async def test_rag_system():
    """测试RAGSystem"""
    print("\n🧪 测试RAGSystem...")
    
    try:
        # 测试搜索
        query = "什么是RAG技术"
        results = rag_system.search(query, top_k=3)
        
        if results:
            print(f"✅ RAG搜索测试Success，找到 {len(results)} 个结果")
            for i, result in enumerate(results[:2]):
                print(f"   结果 {i+1}: {result['content'][:100]}...")
        else:
            print("⚠️ RAG搜索未找到结果")
        
        return True
        
    except Exception as e:
        print(f"❌ RAGSystem测试Failed: {e}")
        return False


async def test_chat_manager():
    """测试Chat manager"""
    print("\n🧪 测试Chat manager...")
    
    try:
        # 测试普通对话
        result = await chat_manager.chat("你好，请介绍一下Flatopia")
        
        if result["success"]:
            print("✅ Chat manager测试Success")
            print(f"   回复: {result['response'][:100]}...")
        else:
            print(f"❌ 聊天Failed: {result.get('error', 'Unknown error')}")
        
        return result["success"]
        
    except Exception as e:
        print(f"❌ Chat manager测试Failed: {e}")
        return False


async def test_rag_chat():
    """测试RAG聊天"""
    print("\n🧪 测试RAG聊天...")
    
    try:
        # 测试RAG对话
        result = await chat_manager.chat("什么是RAG技术？", use_rag=True)
        
        if result["success"]:
            print("✅ RAG聊天测试Success")
            print(f"   回复: {result['response'][:100]}...")
        else:
            print(f"❌ RAG聊天Failed: {result.get('error', 'Unknown error')}")
        
        return result["success"]
        
    except Exception as e:
        print(f"❌ RAG聊天测试Failed: {e}")
        return False


async def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("🧪 开始运行测试")
    print("=" * 50)
    
    tests = [
        ("Groq客户端", test_groq_client),
        ("RAGSystem", test_rag_system),
        ("Chat manager", test_chat_manager),
        ("RAG聊天", test_rag_chat)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ Failed"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 个测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！System运行正常。")
    else:
        print("⚠️ 部分测试Failed，请检查Configuration和依赖。")
    
    return passed == len(results)


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
