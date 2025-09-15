"""
基础LangChainTest script
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.simple_langchain_config import GroqLLM
from core.config import settings


async def test_basic_components():
    """测试基础组件"""
    print("🧪 测试基础LangChain组件...")
    
    tests = [
        ("Groq LLM", test_groq_llm),
        ("ConfigurationLoading", test_config_loading),
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


async def test_groq_llm():
    """测试Groq LLM"""
    try:
        # 检查API密钥
        if not settings.groq_api_key or settings.groq_api_key == "your_groq_api_key_here":
            print("   跳过LLM测试：未设置API密钥")
            return False
        
        # 创建LLM实例
        llm = GroqLLM(
            groq_api_key=settings.groq_api_key,
            model_name="llama-3.1-8b-instant"
        )
        
        # 测试简单调用
        response = llm("你好，请简单介绍一下自己")
        
        # 检查响应
        success = len(response) > 0 and "Error:" not in response
        
        if success:
            print(f"   LLM响应: {response[:100]}...")
        else:
            print(f"   LLM响应: {response}")
        
        return success
        
    except Exception as e:
        print(f"   LLM测试Failed: {e}")
        return False


async def test_config_loading():
    """测试ConfigurationLoading"""
    try:
        # 检查Configuration是否正确Loading
        config_loaded = (
            hasattr(settings, 'groq_api_key') and
            hasattr(settings, 'default_model') and
            hasattr(settings, 'chunk_size') and
            hasattr(settings, 'chunk_overlap')
        )
        
        if config_loaded:
            print(f"   API密钥: {'已设置' if settings.groq_api_key != 'your_groq_api_key_here' else '未设置'}")
            print(f"   默认Model: {settings.default_model}")
            print(f"   块大小: {settings.chunk_size}")
            print(f"   块重叠: {settings.chunk_overlap}")
        
        return config_loaded
        
    except Exception as e:
        print(f"   ConfigurationLoadingFailed: {e}")
        return False


async def test_simple_chat():
    """测试简单聊天"""
    print("\n💬 测试简单聊天...")
    
    try:
        # 检查API密钥
        if not settings.groq_api_key or settings.groq_api_key == "your_groq_api_key_here":
            print("   跳过聊天测试：未设置API密钥")
            return False
        
        # 创建LLM实例
        llm = GroqLLM(
            groq_api_key=settings.groq_api_key,
            model_name="llama-3.1-8b-instant"
        )
        
        # 测试不同的问题
        test_questions = [
            "你好，请介绍一下自己",
            "什么是人工智能？",
            "请解释一下RAG技术"
        ]
        
        results = []
        
        for i, question in enumerate(test_questions, 1):
            try:
                print(f"   问题 {i}: {question}")
                response = llm(question)
                
                success = len(response) > 0 and "Error:" not in response
                results.append(success)
                
                if success:
                    print(f"   回答: {response[:100]}...")
                else:
                    print(f"   Error: {response}")
                
            except Exception as e:
                print(f"   问题 {i} Failed: {e}")
                results.append(False)
        
        return all(results)
        
    except Exception as e:
        print(f"   聊天测试Failed: {e}")
        return False


async def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 开始运行基础LangChain测试")
    print("=" * 60)
    
    # 测试基础组件
    component_results = await test_basic_components()
    
    # 测试简单聊天
    chat_result = await test_simple_chat()
    
    # 汇总结果
    all_results = component_results + [("简单聊天", chat_result)]
    
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
        print("🎉 所有测试通过！基础LangChainSystem运行正常。")
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
