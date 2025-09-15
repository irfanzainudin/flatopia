"""
启动Script
"""
import os
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.config import settings
from core.rag_system import rag_system
from utils.data_loader import DataLoader


async def initialize_system():
    """InitializeSystem"""
    print("🚀 正在InitializeFlatopiaQ问答A机器人...")
    
    # 检查环境变量
    if not settings.groq_api_key or settings.groq_api_key == "your_groq_api_key_here":
        print("❌ 请先设置GROQ_API_KEY环境变量")
        print("   1. 复制 env.example 为 .env")
        print("   2. 在 .env File中设置您的Groq API密钥")
        return False
    
    # Initialize知识库
    try:
        print("📚 正在Initialize知识库...")
        
        # 添加示例文档
        sample_docs = DataLoader.load_sample_documents()
        metadatas = [
            {"source": "sample_doc", "topic": "platopia_intro", "index": i}
            for i in range(len(sample_docs))
        ]
        
        rag_system.add_documents(sample_docs, metadatas)
        
        # 显示知识库信息
        info = rag_system.get_collection_info()
        print(f"✅ 知识库Initialize完成，包含 {info.get('document_count', 0)} 个文档")
        
    except Exception as e:
        print(f"⚠️ 知识库InitializeFailed: {e}")
        print("   System仍可运行，但RAG功能可能不可用")
    
    print("✅ SystemInitialize完成！")
    return True


def main():
    """主函数"""
    print("=" * 50)
    print("🤖 Flatopia Q问答A机器人")
    print("=" * 50)
    
    # InitializeSystem
    success = asyncio.run(initialize_system())
    
    if not success:
        print("\n❌ InitializeFailed，请检查Configuration后重试")
        return
    
    print("\n📋 可用的启动选项：")
    print("1. 启动Web界面: streamlit run app.py")
    print("2. 启动APIService: uvicorn api.main:app --reload")
    print("3. 运行测试: python test.py")
    
    print("\n🔧 Configuration信息：")
    print(f"   Model: {settings.default_model}")
    print(f"   最大令牌数: {settings.max_tokens}")
    print(f"   温度: {settings.temperature}")
    print(f"   向量数据库: {settings.vector_db_path}")
    
    print("\n📖 Usage instructions：")
    print("   1. 确保已Install dependencies: pip install -r requirements.txt")
    print("   2. 设置环境变量: cp env.example .env")
    print("   3. 在.env中Configuration您的Groq API密钥")
    print("   4. 选择上述选项之一Start service")


if __name__ == "__main__":
    main()
