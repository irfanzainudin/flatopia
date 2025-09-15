"""
数据Loading工具
"""
import os
import json
from typing import List, Dict, Any
from pathlib import Path


class DataLoader:
    """数据Loading器"""
    
    @staticmethod
    def load_sample_documents() -> List[str]:
        """Loading示例文档"""
        sample_docs = [
            """
            Flatopia是一个基于Groq API和RAG技术的智能Q问答A机器人。
            它能够理解用户的问题，并从知识库中检索相关信息来生成准确的回答。
            Flatopia支持多种功能，包括普通对话、文档搜索、问题分析等。
            """,
            """
            RAG（检索增强生成）是一种结合了信息检索和文本生成的技术。
            它首先从知识库中检索与用户问题相关的文档片段，
            然后将这些信息作为上下文提供给语言Model，生成更准确的回答。
            RAG技术能够显著提高Q问答ASystem的准确性和可靠性。
            """,
            """
            Groq是一个专门为AI推理优化的硬件和软件平台。
            它提供了高性能的APIInterface，支持多种开源大语言Model，
            包括Llama、Mixtral、Gemma等。Groq API具有低延迟、
            高吞吐量的特点，非常适合实时对话Application。
            """,
            """
            向量数据库是存储和检索高维向量数据的专门数据库。
            在RAGSystem中，文档被转换为向量表示并存储在向量数据库中。
            当用户提问时，System会将问题转换为向量，然后搜索最相似的文档向量。
            常用的向量数据库包括ChromaDB、Pinecone、Weaviate等。
            """,
            """
            Prompt工程是优化大语言Model输入提示的技术。
            通过精心设计的提示词，可以引导Model生成更准确、更符合预期的回答。
            在Q问答ASystem中，好的提示词应该包含角色定义、任务描述、输出格式要求等。
            """
        ]
        return sample_docs
    
    @staticmethod
    def load_sample_questions() -> List[str]:
        """Loading示例问题"""
        return [
            "什么是RAG技术？",
            "Groq API有什么优势？",
            "如何优化Q问答ASystem的性能？",
            "向量数据库在RAG中的作用是什么？",
            "如何设计有效的提示词？",
            "Flatopia有哪些功能特点？",
            "如何提高Q问答A的准确性？",
            "什么是检索增强生成？"
        ]
    
    @staticmethod
    def save_conversation_history(history: List[Dict[str, Any]], filename: str = "conversation_history.json"):
        """保存对话历史"""
        try:
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            
            file_path = data_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存对话历史Failed: {e}")
            return False
    
    @staticmethod
    def load_conversation_history(filename: str = "conversation_history.json") -> List[Dict[str, Any]]:
        """Loading对话历史"""
        try:
            data_dir = Path("data")
            file_path = data_dir / filename
            
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"Loading对话历史Failed: {e}")
            return []
    
    @staticmethod
    def export_knowledge_base(collection_info: Dict[str, Any], filename: str = "knowledge_base_export.json"):
        """导出知识库信息"""
        try:
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            
            file_path = data_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(collection_info, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"导出知识库Failed: {e}")
            return False
