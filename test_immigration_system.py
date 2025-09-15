"""
移民咨询SystemTest script
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.immigration_chat_manager import immigration_chat_manager
from prompts.immigration_prompts import ImmigrationPrompts


async def test_immigration_system():
    """测试移民咨询System"""
    print("🌍 开始测试移民咨询System...")
    
    tests = [
        ("SystemInitialize", test_system_initialization),
        ("用户信息收集", test_profile_collection),
        ("移民分析", test_immigration_analysis),
        ("签证指南", test_visa_guide),
        ("国家对比", test_country_comparison),
        ("PR规划", test_pr_planning)
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


async def test_system_initialization():
    """测试SystemInitialize"""
    try:
        # 测试Chat managerInitialize
        manager = immigration_chat_manager
        
        # 测试国家数据Loading
        countries = manager.get_available_countries()
        if not countries:
            return False
        
        # 测试签证类型Loading
        visa_types = manager.get_available_visa_types()
        if not visa_types:
            return False
        
        print(f"   支持的国家: {len(countries)} 个")
        print(f"   支持的签证类型: {len(visa_types)} 个")
        
        return True
        
    except Exception as e:
        print(f"   SystemInitializeFailed: {e}")
        return False


async def test_profile_collection():
    """测试用户信息收集"""
    try:
        # 模拟用户输入
        user_input = "我今年25岁，男性，中国国籍，想去加拿大工作，有3年软件开发经验"
        
        # 测试信息收集
        result = await immigration_chat_manager.chat(
            user_input=user_input,
            chat_type="profile_collection"
        )
        
        # 检查结果
        success = result["success"] and len(result["answer"]) > 0
        
        if success:
            print(f"   用户信息收集Success")
            print(f"   提取的信息: {result.get('extracted_info', {})}")
        else:
            print(f"   用户信息收集Failed: {result.get('error', '未知Error')}")
        
        return success
        
    except Exception as e:
        print(f"   用户信息收集测试Failed: {e}")
        return False


async def test_immigration_analysis():
    """测试移民分析"""
    try:
        # 设置用户档案
        immigration_chat_manager.update_user_profile({
            "age": 25,
            "gender": "男",
            "nationality": "中国",
            "target_country": "加拿大",
            "experience": "3年软件开发"
        })
        
        # 测试移民分析
        result = await immigration_chat_manager.chat(
            user_input="请分析我的移民可行性",
            chat_type="immigration_analysis"
        )
        
        # 检查结果
        success = result["success"] and len(result["answer"]) > 0
        
        if success:
            print(f"   移民分析Success")
            print(f"   分析结果长度: {len(result['answer'])} 字符")
        else:
            print(f"   移民分析Failed: {result.get('error', '未知Error')}")
        
        return success
        
    except Exception as e:
        print(f"   移民分析测试Failed: {e}")
        return False


async def test_visa_guide():
    """测试签证指南"""
    try:
        # 测试签证指南
        result = await immigration_chat_manager.chat(
            user_input="我想了解加拿大的工作签证申请指南",
            chat_type="visa_guide"
        )
        
        # 检查结果
        success = result["success"] and len(result["answer"]) > 0
        
        if success:
            print(f"   签证指南生成Success")
            print(f"   指南长度: {len(result['answer'])} 字符")
        else:
            print(f"   签证指南生成Failed: {result.get('error', '未知Error')}")
        
        return success
        
    except Exception as e:
        print(f"   签证指南测试Failed: {e}")
        return False


async def test_country_comparison():
    """测试国家对比"""
    try:
        # 测试国家对比
        result = await immigration_chat_manager.chat(
            user_input="请对比加拿大、澳大利亚和新西兰的移民政策",
            chat_type="country_comparison"
        )
        
        # 检查结果
        success = result["success"] and len(result["answer"]) > 0
        
        if success:
            print(f"   国家对比Success")
            print(f"   对比结果长度: {len(result['answer'])} 字符")
        else:
            print(f"   国家对比Failed: {result.get('error', '未知Error')}")
        
        return success
        
    except Exception as e:
        print(f"   国家对比测试Failed: {e}")
        return False


async def test_pr_planning():
    """测试PR规划"""
    try:
        # 测试PR规划
        result = await immigration_chat_manager.chat(
            user_input="我想了解加拿大的永久居民申请规划",
            chat_type="pr_planning"
        )
        
        # 检查结果
        success = result["success"] and len(result["answer"]) > 0
        
        if success:
            print(f"   PR规划Success")
            print(f"   规划长度: {len(result['answer'])} 字符")
        else:
            print(f"   PR规划Failed: {result.get('error', '未知Error')}")
        
        return success
        
    except Exception as e:
        print(f"   PR规划测试Failed: {e}")
        return False


async def test_prompt_templates():
    """测试提示词模板"""
    print("\n📝 测试提示词模板...")
    
    try:
        prompts = ImmigrationPrompts()
        
        # 测试System提示词
        system_prompt = prompts.get_system_prompt()
        if not system_prompt or len(system_prompt) < 100:
            return False
        
        # 测试用户档案提示词
        profile_prompt = prompts.get_user_profile_prompt()
        if not profile_prompt or len(profile_prompt) < 100:
            return False
        
        # 测试移民分析提示词
        analysis_prompt = prompts.get_immigration_analysis_prompt({"age": 25})
        if not analysis_prompt or len(analysis_prompt) < 100:
            return False
        
        print(f"   System提示词: {len(system_prompt)} 字符")
        print(f"   用户档案提示词: {len(profile_prompt)} 字符")
        print(f"   移民分析提示词: {len(analysis_prompt)} 字符")
        
        return True
        
    except Exception as e:
        print(f"   提示词模板测试Failed: {e}")
        return False


async def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🌍 开始运行移民咨询System测试")
    print("=" * 60)
    
    # 测试System组件
    component_results = await test_immigration_system()
    
    # 测试提示词模板
    prompt_result = await test_prompt_templates()
    
    # 汇总结果
    all_results = component_results + [("提示词模板", prompt_result)]
    
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
        print("🎉 所有测试通过！移民咨询System运行正常。")
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
