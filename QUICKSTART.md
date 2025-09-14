# 🚀 Flatopia 快速开始指南

## 第一步：环境准备

### 1. 安装Python依赖
```bash
pip install -r requirements.txt
```

### 2. 获取Groq API密钥
1. 访问 [Groq Console](https://console.groq.com/)
2. 注册/登录账户
3. 创建API密钥
4. 复制API密钥

### 3. Configuration环境变量
```bash
# 复制环境变量模板
cp env.example .env

# 编辑 .env File，添加您的API密钥
GROQ_API_KEY=your_actual_groq_api_key_here
```

## 第二步：InitializeSystem

### 运行InitializeScript
```bash
python run.py
```

这将：
- 检查Configuration是否正确
- Initialize向量数据库
- Loading示例文档到知识库
- 显示System状态

## 第三步：Start service

### 方式1：Web界面（推荐）
```bash
streamlit run app.py
```
访问 http://localhost:8501

### 方式2：APIService
```bash
uvicorn api.main:app --reload
```
访问 http://localhost:8000/docs 查看API文档

## 第四步：测试System

### 运行测试
```bash
python test.py
```

### 手动测试
1. 在Web界面中输入问题
2. 尝试不同的功能：
   - 普通对话
   - RAG增强Q问答A
   - 问题分析
   - 创意回复

## 功能特性

### 🤖 智能对话
- 基于Groq API的高性能对话
- 支持多种Model（Llama 3, Mixtral等）
- 多轮对话记忆

### 📚 RAGSystem
- 向量数据库存储知识
- 智能文档检索
- 上下文增强回答

### 🔧 高级功能
- 问题分析
- 创意内容生成
- 文档Management
- 搜索功能

## Use示例

### 基础Q问答A
```
用户：什么是RAG技术？
Flatopia：RAG（检索增强生成）是一种结合了信息检索和文本生成的技术...
```

### RAG增强Q问答A
```
用户：Flatopia有哪些特点？
Flatopia：基于您的问题，我从知识库中找到了相关信息。Flatopia是一个基于Groq API和RAG技术的智能Q问答A机器人...
```

### 问题分析
```
用户：如何优化Q问答ASystem？
Flatopia：**问题分析：**
1. 问题类型：技术优化咨询
2. 复杂度：中等
3. 建议解答方向：性能优化、架构设计、用户体验
4. 关键信息：当前System状态、性能瓶颈、优化目标
```

## Configuration说明

### ModelConfiguration
在 `.env` File中可以调整：
```env
DEFAULT_MODEL=llama3-8b-8192  # 默认Model
MAX_TOKENS=1024               # 最大令牌数
TEMPERATURE=0.7               # 创造性参数
```

### RAGConfiguration
```env
CHUNK_SIZE=1000               # 文档分块大小
CHUNK_OVERLAP=200             # 分块重叠
TOP_K=5                       # 检索结果数量
```

## 常见问题

### Q: API密钥无效怎么办？
A: 检查 `.env` File中的 `GROQ_API_KEY` 是否正确设置

### Q: 知识库为空怎么办？
A: 运行 `python run.py` 重新Initialize，或通过Web界面添加文档

### Q: 如何添加自己的文档？
A: 在Web界面的"知识库Management"部分添加文档，或UseAPIInterface

### Q: 如何提高回答质量？
A: 
1. 添加更多相关文档到知识库
2. 调整prompt模板
3. 优化检索参数
4. Use更合适的Model

## 下一步

1. **自定义知识库**：添加您的专业文档
2. **优化Prompt**：根据需求调整提示词
3. **集成Application**：将API集成到您的Application中
4. **扩展功能**：添加更多高级功能

## 技术支持

如有问题，请检查：
1. 依赖是否正确安装
2. API密钥是否有效
3. 网络连接是否正常
4. 查看Error日志

---

🎉 恭喜！您已经Success搭建了FlatopiaQ问答A机器人！
