"""
PromptTest script
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.prompt_tester import prompt_tester
from utils.prompt_optimizer import prompt_optimizer
from prompts.chat_prompts import ChatPrompts


async def test_prompts():
    """测试所有prompt"""
    print("🚀 开始Prompt测试和优化...")
    
    # 运行测试
    test_results = await prompt_tester.run_all_tests()
    
    # 打印结果
    prompt_tester.print_test_summary(test_results)
    
    # 保存结果
    prompt_tester.save_test_results(test_results)
    
    return test_results


def analyze_prompt_quality():
    """分析prompt质量"""
    print("\n🔍 分析Prompt质量...")
    
    prompts = ChatPrompts()
    
    # 测试不同的prompt
    test_prompts = [
        ("SystemPrompt", prompts.get_system_prompt()),
        ("RAG Prompt", prompts.get_rag_prompt("测试问题", "测试上下文")),
        ("商业分析Prompt", prompts.get_business_analysis_prompt("测试商业问题")),
        ("代码审查Prompt", prompts.get_code_review_prompt("def test(): pass", "python")),
        ("学习路径Prompt", prompts.get_learning_path_prompt("机器学习", "beginner"))
    ]
    
    print("\n📊 Prompt质量分析结果:")
    print("="*60)
    
    for name, prompt in test_prompts:
        analysis = prompt_optimizer.analyze_prompt(prompt)
        
        print(f"\n📝 {name}")
        print(f"   总体评分: {analysis.overall_score:.2f}/1.0")
        print(f"   清晰度: {analysis.clarity_score:.2f}")
        print(f"   结构: {analysis.structure_score:.2f}")
        print(f"   具体性: {analysis.specificity_score:.2f}")
        print(f"   完整性: {analysis.completeness_score:.2f}")
        
        if analysis.strengths:
            print(f"   ✅ 优势: {', '.join(analysis.strengths)}")
        
        if analysis.weaknesses:
            print(f"   ❌ 弱点: {', '.join(analysis.weaknesses)}")
        
        if analysis.suggestions:
            print(f"   💡 建议: {', '.join(analysis.suggestions[:3])}...")


def optimize_prompts():
    """优化prompt示例"""
    print("\n🔧 Prompt优化示例...")
    
    # 示例prompt
    original_prompt = """请回答用户问题。要准确，要详细。"""
    
    print("\n📝 原始Prompt:")
    print(original_prompt)
    
    # 分析原始prompt
    original_analysis = prompt_optimizer.analyze_prompt(original_prompt)
    print(f"\n📊 原始评分: {original_analysis.overall_score:.2f}/1.0")
    
    # 优化prompt
    optimized_prompt = prompt_optimizer.optimize_prompt(original_prompt)
    
    print("\n✨ 优化后Prompt:")
    print(optimized_prompt)
    
    # 分析优化后的prompt
    optimized_analysis = prompt_optimizer.analyze_prompt(optimized_prompt)
    print(f"\n📊 优化后评分: {optimized_analysis.overall_score:.2f}/1.0")
    
    # 比较结果
    comparison = prompt_optimizer.compare_prompts(original_prompt, optimized_prompt)
    
    print("\n📈 改进效果:")
    for metric, improvement in comparison["improvement_percentage"].items():
        print(f"   {metric}: {improvement}")


def main():
    """主函数"""
    print("="*60)
    print("🎯 Flatopia Prompt测试和优化工具")
    print("="*60)
    
    try:
        # 分析prompt质量
        analyze_prompt_quality()
        
        # 优化prompt示例
        optimize_prompts()
        
        # 运行完整测试
        print("\n" + "="*60)
        print("🧪 运行完整测试...")
        test_results = asyncio.run(test_prompts())
        
        print("\n🎉 Prompt测试和优化完成！")
        
        # 提供优化建议
        print("\n💡 优化建议:")
        print("1. 定期测试prompt效果")
        print("2. 根据用户反馈调整prompt")
        print("3. UseA/B测试比较不同版本")
        print("4. 监控prompt性能指标")
        print("5. 持续迭代和改进")
        
    except Exception as e:
        print(f"❌ 测试过程中出现Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
