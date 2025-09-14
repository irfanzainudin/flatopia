"""
文本Processing工具
"""
import re
from typing import List, Dict, Any
from datetime import datetime


class TextProcessor:
    """文本Processing器"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """清理文本"""
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()]', '', text)
        return text.strip()
    
    @staticmethod
    def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取（可以改进为更复杂的算法）
        words = re.findall(r'\b\w+\b', text.lower())
        
        # 过滤停用词
        stop_words = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 1]
        
        # 统计词频
        word_count = {}
        for word in keywords:
            word_count[word] = word_count.get(word, 0) + 1
        
        # 按词频排序
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, count in sorted_words[:max_keywords]]
    
    @staticmethod
    def summarize_text(text: str, max_length: int = 200) -> str:
        """文本摘要"""
        if len(text) <= max_length:
            return text
        
        # 简单的摘要：取前几个句子
        sentences = re.split(r'[.!?。！？]', text)
        summary = ""
        
        for sentence in sentences:
            if len(summary + sentence) <= max_length:
                summary += sentence + "。"
            else:
                break
        
        return summary.strip()
    
    @staticmethod
    def detect_language(text: str) -> str:
        """检测语言"""
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if chinese_chars > english_chars:
            return "zh"
        elif english_chars > chinese_chars:
            return "en"
        else:
            return "mixed"
    
    @staticmethod
    def format_timestamp(timestamp: str) -> str:
        """格式化时间戳"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return timestamp
    
    @staticmethod
    def extract_questions(text: str) -> List[str]:
        """提取问题"""
        # 匹配问号结尾的句子
        questions = re.findall(r'[^.!?]*\?', text)
        return [q.strip() for q in questions if q.strip()]
    
    @staticmethod
    def highlight_keywords(text: str, keywords: List[str]) -> str:
        """高亮关键词"""
        for keyword in keywords:
            text = re.sub(
                f'\\b{re.escape(keyword)}\\b',
                f'**{keyword}**',
                text,
                flags=re.IGNORECASE
            )
        return text
    
    @staticmethod
    def calculate_text_similarity(text1: str, text2: str) -> float:
        """计算文本相似度（简单的Jaccard相似度）"""
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
