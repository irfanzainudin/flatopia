"""
Prompt优化建议工具
"""
import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class PromptAnalysis:
    """Prompt分析结果"""
    clarity_score: float
    structure_score: float
    specificity_score: float
    completeness_score: float
    overall_score: float
    suggestions: List[str]
    strengths: List[str]
    weaknesses: List[str]


class PromptOptimizer:
    """Prompt优化器"""
    
    def __init__(self):
        self.optimization_rules = {
            "clarity": [
                "Use简洁明了的语言",
                "避免过于复杂的句子结构",
                "Use具体的词汇而非抽象概念",
                "避免歧义和模糊表达"
            ],
            "structure": [
                "Use清晰的标题和分段",
                "采用一致的格式和风格",
                "Use列表和编号组织信息",
                "保持逻辑顺序清晰"
            ],
            "specificity": [
                "提供具体的示例和场景",
                "Use明确的指令和约束",
                "定义关键术语和概念",
                "提供可衡量的标准"
            ],
            "completeness": [
                "覆盖所有必要的上下文信息",
                "包含ErrorProcessing指导",
                "提供多种场景的考虑",
                "包含输出格式要求"
            ]
        }
    
    def analyze_prompt(self, prompt: str) -> PromptAnalysis:
        """分析prompt质量"""
        clarity_score = self._analyze_clarity(prompt)
        structure_score = self._analyze_structure(prompt)
        specificity_score = self._analyze_specificity(prompt)
        completeness_score = self._analyze_completeness(prompt)
        
        overall_score = (clarity_score + structure_score + specificity_score + completeness_score) / 4
        
        suggestions = self._generate_suggestions(prompt, {
            "clarity": clarity_score,
            "structure": structure_score,
            "specificity": specificity_score,
            "completeness": completeness_score
        })
        
        strengths = self._identify_strengths(prompt)
        weaknesses = self._identify_weaknesses(prompt, {
            "clarity": clarity_score,
            "structure": structure_score,
            "specificity": specificity_score,
            "completeness": completeness_score
        })
        
        return PromptAnalysis(
            clarity_score=clarity_score,
            structure_score=structure_score,
            specificity_score=specificity_score,
            completeness_score=completeness_score,
            overall_score=overall_score,
            suggestions=suggestions,
            strengths=strengths,
            weaknesses=weaknesses
        )
    
    def _analyze_clarity(self, prompt: str) -> float:
        """分析清晰度"""
        score = 0.0
        
        # 检查句子长度
        sentences = re.split(r'[.!?。！？]', prompt)
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences) if sentences else 0
        
        if avg_sentence_length <= 15:
            score += 0.3
        elif avg_sentence_length <= 25:
            score += 0.2
        else:
            score += 0.1
        
        # 检查复杂词汇
        complex_words = re.findall(r'\b\w{10,}\b', prompt)
        if len(complex_words) / len(prompt.split()) < 0.1:
            score += 0.3
        elif len(complex_words) / len(prompt.split()) < 0.2:
            score += 0.2
        else:
            score += 0.1
        
        # 检查重复词汇
        words = prompt.lower().split()
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        repetition_ratio = max(word_freq.values()) / len(words) if words else 0
        if repetition_ratio < 0.1:
            score += 0.4
        elif repetition_ratio < 0.2:
            score += 0.3
        else:
            score += 0.1
        
        return min(score, 1.0)
    
    def _analyze_structure(self, prompt: str) -> float:
        """分析结构"""
        score = 0.0
        
        # 检查标题Use
        if re.search(r'^#+\s', prompt, re.MULTILINE):
            score += 0.3
        
        # 检查列表Use
        if re.search(r'^\s*[-*+]\s', prompt, re.MULTILINE) or re.search(r'^\s*\d+\.\s', prompt, re.MULTILINE):
            score += 0.3
        
        # 检查分段
        paragraphs = re.split(r'\n\s*\n', prompt)
        if len(paragraphs) >= 3:
            score += 0.2
        elif len(paragraphs) >= 2:
            score += 0.1
        
        # 检查格式一致性
        if re.search(r'^\s*[-*+]\s', prompt, re.MULTILINE):
            if all(re.match(r'^\s*[-*+]\s', line) for line in prompt.split('\n') if re.search(r'^\s*[-*+]\s', line)):
                score += 0.2
        
        return min(score, 1.0)
    
    def _analyze_specificity(self, prompt: str) -> float:
        """分析具体性"""
        score = 0.0
        
        # 检查示例
        if re.search(r'例如|比如|举例|示例', prompt):
            score += 0.3
        
        # 检查具体数字
        if re.search(r'\d+', prompt):
            score += 0.2
        
        # 检查具体指令
        action_words = ['请', '要求', '必须', '应该', '需要', '确保']
        if any(word in prompt for word in action_words):
            score += 0.3
        
        # 检查格式要求
        if re.search(r'格式|结构|样式|模板', prompt):
            score += 0.2
        
        return min(score, 1.0)
    
    def _analyze_completeness(self, prompt: str) -> float:
        """分析完整性"""
        score = 0.0
        
        # 检查上下文信息
        context_indicators = ['上下文', '背景', '信息', '数据', '内容']
        if any(word in prompt for word in context_indicators):
            score += 0.3
        
        # 检查输出要求
        output_indicators = ['输出', '回答', '结果', '格式', '要求']
        if any(word in prompt for word in output_indicators):
            score += 0.3
        
        # 检查ErrorProcessing
        error_indicators = ['如果', '当', 'Error', '异常', 'Failed']
        if any(word in prompt for word in error_indicators):
            score += 0.2
        
        # 检查多种场景
        scenario_indicators = ['情况', '场景', '条件', '假设']
        if any(word in prompt for word in scenario_indicators):
            score += 0.2
        
        return min(score, 1.0)
    
    def _generate_suggestions(self, prompt: str, scores: Dict[str, float]) -> List[str]:
        """生成优化建议"""
        suggestions = []
        
        for category, score in scores.items():
            if score < 0.6:
                suggestions.extend(self.optimization_rules[category])
        
        # 特定建议
        if len(prompt.split()) < 50:
            suggestions.append("增加更多详细信息和上下文")
        
        if not re.search(r'请|要求|必须', prompt):
            suggestions.append("添加明确的指令和行动要求")
        
        if not re.search(r'格式|结构|样式', prompt):
            suggestions.append("指定期望的输出格式和结构")
        
        return list(set(suggestions))  # 去重
    
    def _identify_strengths(self, prompt: str) -> List[str]:
        """识别优势"""
        strengths = []
        
        if re.search(r'^#+\s', prompt, re.MULTILINE):
            strengths.append("Use了清晰的标题结构")
        
        if re.search(r'^\s*[-*+]\s', prompt, re.MULTILINE):
            strengths.append("Use了列表格式组织信息")
        
        if re.search(r'例如|比如|举例', prompt):
            strengths.append("包含了具体示例")
        
        if len(prompt.split()) > 100:
            strengths.append("提供了详细的信息和上下文")
        
        return strengths
    
    def _identify_weaknesses(self, prompt: str, scores: Dict[str, float]) -> List[str]:
        """识别弱点"""
        weaknesses = []
        
        if scores["clarity"] < 0.6:
            weaknesses.append("语言表达不够清晰")
        
        if scores["structure"] < 0.6:
            weaknesses.append("结构组织不够清晰")
        
        if scores["specificity"] < 0.6:
            weaknesses.append("缺乏具体的指令和示例")
        
        if scores["completeness"] < 0.6:
            weaknesses.append("信息不够完整")
        
        return weaknesses
    
    def optimize_prompt(self, prompt: str) -> str:
        """优化prompt"""
        analysis = self.analyze_prompt(prompt)
        
        optimized_prompt = prompt
        
        # 添加结构改进
        if analysis.structure_score < 0.6:
            if not re.search(r'^#+\s', optimized_prompt, re.MULTILINE):
                optimized_prompt = f"# 任务说明\n\n{optimized_prompt}"
        
        # 添加具体性改进
        if analysis.specificity_score < 0.6:
            if not re.search(r'请|要求|必须', optimized_prompt):
                optimized_prompt += "\n\n请按照以上要求完成任务。"
        
        # 添加完整性改进
        if analysis.completeness_score < 0.6:
            if not re.search(r'输出|回答|结果', optimized_prompt):
                optimized_prompt += "\n\n请提供详细的回答和解释。"
        
        return optimized_prompt
    
    def compare_prompts(self, original: str, optimized: str) -> Dict[str, Any]:
        """比较prompt优化效果"""
        original_analysis = self.analyze_prompt(original)
        optimized_analysis = self.analyze_prompt(optimized)
        
        improvements = {
            "clarity": optimized_analysis.clarity_score - original_analysis.clarity_score,
            "structure": optimized_analysis.structure_score - original_analysis.structure_score,
            "specificity": optimized_analysis.specificity_score - original_analysis.specificity_score,
            "completeness": optimized_analysis.completeness_score - original_analysis.completeness_score,
            "overall": optimized_analysis.overall_score - original_analysis.overall_score
        }
        
        return {
            "original": original_analysis,
            "optimized": optimized_analysis,
            "improvements": improvements,
            "improvement_percentage": {
                key: f"{(value * 100):.1f}%" for key, value in improvements.items()
            }
        }


# 全局优化器实例
prompt_optimizer = PromptOptimizer()
