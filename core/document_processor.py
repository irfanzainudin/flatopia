"""
Based on LangChain的文档Processing器
"""
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader, 
    Docx2txtLoader,
    WebBaseLoader,
    DirectoryLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from .langchain_config import langchain_config


class DocumentProcessor:
    """文档Processing器"""
    
    def __init__(self):
        self.text_splitter = langchain_config.text_splitter
        self.supported_formats = {
            '.txt': TextLoader,
            '.pdf': PyPDFLoader,
            '.docx': Docx2txtLoader,
            '.html': WebBaseLoader,
            '.htm': WebBaseLoader
        }
    
    def load_document(self, file_path: str) -> List[Document]:
        """Loading单个文档"""
        try:
            file_path = Path(file_path)
            file_extension = file_path.suffix.lower()
            
            if file_extension not in self.supported_formats:
                raise ValueError(f"不支持的File格式: {file_extension}")
            
            loader_class = self.supported_formats[file_extension]
            
            if file_extension in ['.html', '.htm']:
                loader = loader_class([str(file_path)])
            else:
                loader = loader_class(str(file_path))
            
            documents = loader.load()
            return documents
            
        except Exception as e:
            print(f"Loading文档Failed {file_path}: {e}")
            return []
    
    def load_directory(self, directory_path: str, glob_pattern: str = "**/*") -> List[Document]:
        """Loading目录中的所有文档"""
        try:
            loader = DirectoryLoader(
                directory_path,
                glob=glob_pattern,
                loader_cls=self._get_loader_for_glob,
                show_progress=True
            )
            documents = loader.load()
            return documents
            
        except Exception as e:
            print(f"Loading目录Failed {directory_path}: {e}")
            return []
    
    def _get_loader_for_glob(self, file_path: str):
        """根据File扩展名获取对应的Loading器"""
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension in self.supported_formats:
            return self.supported_formats[file_extension]
        else:
            return TextLoader  # 默认Use文本Loading器
    
    def load_web_content(self, urls: List[str]) -> List[Document]:
        """Loading网页内容"""
        try:
            loader = WebBaseLoader(urls)
            documents = loader.load()
            return documents
            
        except Exception as e:
            print(f"Loading网页内容Failed: {e}")
            return []
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """分割文档"""
        try:
            split_docs = self.text_splitter.split_documents(documents)
            return split_docs
            
        except Exception as e:
            print(f"分割文档Failed: {e}")
            return documents
    
    def process_documents(self, 
                         documents: List[Document], 
                         add_metadata: bool = True) -> List[Document]:
        """Processing文档（添加元数据、清理等）"""
        processed_docs = []
        
        for i, doc in enumerate(documents):
            try:
                # 清理文档内容
                cleaned_content = self._clean_document_content(doc.page_content)
                
                # 创建新文档
                processed_doc = Document(
                    page_content=cleaned_content,
                    metadata=doc.metadata.copy() if doc.metadata else {}
                )
                
                # 添加Processing元数据
                if add_metadata:
                    processed_doc.metadata.update({
                        "processed": True,
                        "document_id": i,
                        "content_length": len(cleaned_content),
                        "word_count": len(cleaned_content.split())
                    })
                
                processed_docs.append(processed_doc)
                
            except Exception as e:
                print(f"Processing文档Failed: {e}")
                processed_docs.append(doc)
        
        return processed_docs
    
    def _clean_document_content(self, content: str) -> str:
        """清理文档内容"""
        # 移除多余的空白字符
        content = ' '.join(content.split())
        
        # 移除特殊字符（保留中文、英文、数字和基本标点）
        import re
        content = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()（）【】""''""''，。！？；：]', '', content)
        
        return content.strip()
    
    def create_document_from_text(self, 
                                 text: str, 
                                 metadata: Optional[Dict[str, Any]] = None) -> Document:
        """从文本创建文档"""
        metadata = metadata or {}
        metadata.update({
            "source": "manual_input",
            "type": "text"
        })
        
        return Document(
            page_content=text,
            metadata=metadata
        )
    
    def batch_process(self, 
                     file_paths: List[str], 
                     add_to_vectorstore: bool = True) -> Dict[str, Any]:
        """批量Processing文档"""
        results = {
            "total_files": len(file_paths),
            "successful_files": 0,
            "failed_files": 0,
            "total_documents": 0,
            "processed_documents": 0,
            "errors": []
        }
        
        all_documents = []
        
        for file_path in file_paths:
            try:
                # Loading文档
                documents = self.load_document(file_path)
                
                if documents:
                    # 分割文档
                    split_docs = self.split_documents(documents)
                    
                    # Processing文档
                    processed_docs = self.process_documents(split_docs)
                    
                    all_documents.extend(processed_docs)
                    results["successful_files"] += 1
                    results["total_documents"] += len(documents)
                    results["processed_documents"] += len(processed_docs)
                else:
                    results["failed_files"] += 1
                    results["errors"].append(f"无法LoadingFile: {file_path}")
                    
            except Exception as e:
                results["failed_files"] += 1
                results["errors"].append(f"ProcessingFileFailed {file_path}: {str(e)}")
        
        # 添加到Vector storage
        if add_to_vectorstore and all_documents:
            try:
                success = langchain_config.add_documents(all_documents)
                if not success:
                    results["errors"].append("添加到Vector storageFailed")
            except Exception as e:
                results["errors"].append(f"添加到Vector storageFailed: {str(e)}")
        
        return results
    
    def get_document_info(self, documents: List[Document]) -> Dict[str, Any]:
        """获取文档信息统计"""
        if not documents:
            return {"total_documents": 0}
        
        total_chars = sum(len(doc.page_content) for doc in documents)
        total_words = sum(len(doc.page_content.split()) for doc in documents)
        
        # 统计元数据
        metadata_stats = {}
        for doc in documents:
            for key, value in doc.metadata.items():
                if key not in metadata_stats:
                    metadata_stats[key] = []
                metadata_stats[key].append(value)
        
        return {
            "total_documents": len(documents),
            "total_characters": total_chars,
            "total_words": total_words,
            "average_chars_per_doc": total_chars / len(documents),
            "average_words_per_doc": total_words / len(documents),
            "metadata_fields": list(metadata_stats.keys()),
            "metadata_stats": metadata_stats
        }


# 全局文档Processing器实例
document_processor = DocumentProcessor()
