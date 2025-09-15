"""
Prompt测试和验证工具
"""
import asyncio
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..core.groq_client import groq_client
from ..prompts.chat_prompts import ChatPrompts


class PromptTester:
    """Prompt测试器"""
    
    def __init__(self):
        self.test_results = []
        self.prompts = ChatPrompts()
    
    async def test_system_prompt(self) -> Dict[str, Any]:
        """测试Systemprompt"""
        print("🧪 测试Systemprompt...")
        
        test_questions = [
            "你好，请介绍一下自己",
            "什么是RAG技术？",
            "如何优化Python代码性能？",
            "请帮我分析一个商业问题"
        ]
        
        results = []
        for question in test_questions:
            try:
                messages = [
                    {"role": "system", "content": self.prompts.get_system_prompt()},
                    {"role": "user", "content": question}
                ]
                
                response = await groq_client.chat_completion(messages)
                
                results.append({
                    "question": question,
                    "response": response,
                    "success": True,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                results.append({
                    "question": question,
                    "error": str(e),
                    "success": False,
                    "timestamp": datetime.now().isoformat()
                })
        
        return {
            "test_type": "system_prompt",
            "total_tests": len(test_questions),
            "successful_tests": len([r for r in results if r["success"]]),
            "results": results
        }
    
    async def test_rag_prompt(self) -> Dict[str, Any]:
        """测试RAG prompt"""
        print("🧪 测试RAG prompt...")
        
        test_cases = [
            {
                "query": "什么是RAG技术？",
                "context": "RAG（检索增强生成）是一种结合了信息检索和文本生成的技术。它首先从知识库中检索与用户问题相关的文档片段，然后将这些信息作为上下文提供给语言Model，生成更准确的回答。"
            },
            {
                "query": "如何优化Q问答ASystem？",
                "context": "Q问答ASystem优化可以从多个方面入手：1. 改进检索算法，提高相关文档的召回率；2. 优化prompt设计，引导Model生成更好的回答；3. Use更高质量的嵌入Model；4. 增加知识库的覆盖度和准确性。"
            }
        ]
        
        results = []
        for case in test_cases:
            try:
                rag_prompt = self.prompts.get_rag_prompt(case["query"], case["context"])
                messages = [
                    {"role": "system", "content": self.prompts.get_system_prompt()},
                    {"role": "user", "content": rag_prompt}
                ]
                
                response = await groq_client.chat_completion(messages)
                
                results.append({
                    "query": case["query"],
                    "context": case["context"],
                    "response": response,
                    "success": True,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                results.append({
                    "query": case["query"],
                    "error": str(e),
                    "success": False,
                    "timestamp": datetime.now().isoformat()
                })
        
        return {
            "test_type": "rag_prompt",
            "total_tests": len(test_cases),
            "successful_tests": len([r for r in results if r["success"]]),
            "results": results
        }
    
    async def test_specialized_prompts(self) -> Dict[str, Any]:
        """测试专业prompt"""
        print("🧪 测试专业prompt...")
        
        test_cases = [
            {
                "type": "business_analysis",
                "question": "如何分析一个SaaS产品的市场机会？",
                "prompt_func": self.prompts.get_business_analysis_prompt
            },
            {
                "type": "code_review",
                "question": "请审查这段Python代码",
                "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
                "prompt_func": lambda q: self.prompts.get_code_review_prompt(q, "python")
            },
            {
                "type": "learning_path",
                "question": "机器学习",
                "level": "beginner",
                "prompt_func": lambda q: self.prompts.get_learning_path_prompt(q, "beginner")
            }
        ]
        
        results = []
        for case in test_cases:
            try:
                if case["type"] == "code_review":
                    prompt = case["prompt_func"](case["code"])
                elif case["type"] == "learning_path":
                    prompt = case["prompt_func"](case["question"])
                else:
                    prompt = case["prompt_func"](case["question"])
                
                messages = [
                    {"role": "system", "content": self.prompts.get_system_prompt()},
                    {"role": "user", "content": prompt}
                ]
                
                response = await groq_client.chat_completion(messages)
                
                results.append({
                    "type": case["type"],
                    "question": case["question"],
                    "response": response,
                    "success": True,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                results.append({
                    "type": case["type"],
                    "question": case["question"],
                    "error": str(e),
                    "success": False,
                    "timestamp": datetime.now().isoformat()
                })
        
        return {
            "test_type": "specialized_prompts",
            "total_tests": len(test_cases),
            "successful_tests": len([r for r in results if r["success"]]),
            "results": results
        }
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        print("🚀 开始运行Prompt测试...")
        
        tests = [
            self.test_system_prompt(),
            self.test_rag_prompt(),
            self.test_specialized_prompts()
        ]
        
        results = await asyncio.gather(*tests, return_exceptions=True)
        
        # Processing异常结果
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "test_type": f"test_{i}",
                    "error": str(result),
                    "success": False
                })
            else:
                processed_results.append(result)
        
        # 计算总体统计
        total_tests = sum(r.get("total_tests", 0) for r in processed_results)
        successful_tests = sum(r.get("successful_tests", 0) for r in processed_results)
        
        return {
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "success_rate": f"{(successful_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%",
                "timestamp": datetime.now().isoformat()
            },
            "test_results": processed_results
        }
    
    def save_test_results(self, results: Dict[str, Any], filename: str = "prompt_test_results.json"):
        """保存测试结果"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✅ 测试结果已保存到 {filename}")
        except Exception as e:
            print(f"❌ 保存测试结果Failed: {e}")
    
    def print_test_summary(self, results: Dict[str, Any]):
        """打印测试摘要"""
        summary = results["summary"]
        
        print("\n" + "="*50)
        print("📊 Prompt测试结果摘要")
        print("="*50)
        print(f"总测试数: {summary['total_tests']}")
        print(f"Success测试: {summary['successful_tests']}")
        print(f"Success率: {summary['success_rate']}")
        print(f"测试时间: {summary['timestamp']}")
        
        print("\n📋 详细结果:")
        for test in results["test_results"]:
            status = "✅" if test.get("successful_tests", 0) > 0 else "❌"
            print(f"{status} {test['test_type']}: {test.get('successful_tests', 0)}/{test.get('total_tests', 0)}")


# 全局测试器实例
prompt_tester = PromptTester()
