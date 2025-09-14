# Flatopia Q问答A机器人

基于Groq API和RAG技术的智能Q问答A机器人，提供准确、快速的Q问答AService。

## 功能特性

- 🤖 基于Groq API的智能对话
- 📚 RAG（检索增强生成）技术
- 🔍 向量数据库支持
- 💬 多轮对话记忆
- 🌐 Web界面和APIInterface
- ⚡ 高性能和低延迟

## 快速开始

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configuration环境变量

```bash
cp env.example .env
# 编辑 .env File，添加您的Groq API密钥
```

### 3. 运行Application

```bash
# 启动Web界面
streamlit run app.py

# 或启动APIService
uvicorn api.main:app --reload
```

## 项目结构

```
Flatopia/
├── api/                 # FastAPI后端
├── core/               # 核心功能模块
├── data/               # 数据存储
├── prompts/            # Prompt模板
├── utils/              # 工具函数
├── app.py             # Streamlit前端
└── requirements.txt   # 依赖Management
```

## 技术栈

- **后端**: FastAPI, Groq API
- **前端**: Streamlit
- **向量数据库**: ChromaDB
- **嵌入Model**: sentence-transformers
- **LLM**: Groq (Llama 3)

## 许可证

MIT License
