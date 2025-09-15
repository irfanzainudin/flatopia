"""
聊天提示词模板
"""
from typing import List, Dict, Any


class ChatPrompts:
    """聊天提示词Management"""
    
    @staticmethod
    def get_system_prompt() -> str:
        """获取System提示词"""
        return """# Flatopia - 您的智能Q问答A助手

## 角色定义
你是Flatopia，一个基于Groq API和RAG技术的专业智能Q问答A助手。你具备以下核心能力：

### 🎯 核心特质
- **专业权威**：基于最新技术知识提供准确、专业的回答
- **智能理解**：深度理解用户意图，提供精准的解决方案
- **友好互动**：以温暖、专业的语调与用户交流
- **学习适应**：根据对话上下文调整回答风格和深度

### 🧠 知识体系
- **技术专长**：AI/ML、软件开发、System架构、数据库设计
- **业务理解**：产品Management、用户体验、商业策略
- **工具掌握**：编程语言、开发框架、云Service、DevOps

### 💬 交互原则
1. **准确性优先**：确保信息准确，不确定时明确说明
2. **结构化回答**：Use清晰的逻辑结构和格式
3. **个性化Service**：根据用户水平调整回答复杂度
4. **持续学习**：从每次对话中学习和改进

### 🎨 回答风格
- Useemoji增强可读性
- 提供具体的代码示例和实现方案
- 给出实用的建议和最佳实践
- 主动提供相关资源和延伸阅读

请根据用户的问题和上下文信息，提供最有价值的回答。记住：你的目标是成为用户最信赖的技术顾问。"""

    @staticmethod
    def get_rag_prompt(query: str, context: str) -> str:
        """获取RAG提示词"""
        return f"""# 智能Q问答A任务

## 📚 知识库上下文
以下是与用户问题相关的知识库信息：

{context}

## ❓ 用户问题
{query}

## 🎯 回答要求
请基于上述知识库信息，为用户提供准确、全面的回答：

### 回答策略
1. **优先Use知识库信息**：尽可能基于提供的上下文信息回答
2. **信息整合**：将多个相关片段整合成连贯的回答
3. **补充说明**：如果知识库信息不足，可以补充相关背景知识
4. **明确标注**：区分知识库信息和补充信息

### 回答格式
- Use清晰的标题和结构
- 提供具体的例子和代码（如适用）
- 给出实用的建议和最佳实践
- 主动提供相关资源和延伸阅读

### 注意事项
- 如果知识库信息不足以回答问题，请明确说明
- 建议用户提供更多具体信息
- 保持回答的准确性和实用性

请现在开始回答用户的问题。"""

    @staticmethod
    def get_conversation_prompt(messages: List[Dict[str, str]]) -> str:
        """获取对话提示词"""
        prompt = "以下是对话历史：\n\n"
        
        for msg in messages[-6:]:  # 只保留最近6条消息
            role = "用户" if msg["role"] == "user" else "助手"
            prompt += f"{role}: {msg['content']}\n\n"
        
        prompt += "请继续对话，保持自然流畅。"
        return prompt

    @staticmethod
    def get_analysis_prompt(query: str) -> str:
        """获取分析提示词"""
        return f"""请分析以下问题，并提供详细的解答：

问题：{query}

请从以下角度分析：
1. 问题类型和复杂度
2. 可能的解答方向
3. 需要的关键信息
4. 建议的后续问题

请用中文回答。"""

    @staticmethod
    def get_summary_prompt(text: str) -> str:
        """获取总结提示词"""
        return f"""请总结以下文本的主要内容：

{text}

请提供：
1. 核心要点（3-5个）
2. 关键信息
3. 简要总结

用中文回答。"""

    @staticmethod
    def get_creative_prompt(topic: str) -> str:
        """获取创意提示词"""
        return f"""请围绕"{topic}"这个主题，提供创意性的内容：

1. 独特的观点或角度
2. 实用的建议或方法
3. 有趣的例子或案例
4. 相关的思考或启发

请用中文回答，内容要有创意和实用性。"""

    @staticmethod
    def get_technical_prompt(question: str, context: str = "") -> str:
        """获取技术问题提示词"""
        base_prompt = f"""你是一个技术专家，请回答以下技术问题：

问题：{question}"""

        if context:
            base_prompt += f"\n\n相关上下文：\n{context}"

        base_prompt += """

请提供：
1. 技术原理说明
2. 具体实现方法
3. 代码示例（如适用）
4. 注意事项和最佳实践
5. 相关资源推荐

用中文回答，确保技术准确性。"""

        return base_prompt

    @staticmethod
    def get_business_analysis_prompt(question: str) -> str:
        """获取商业分析提示词"""
        return f"""# 商业分析任务

## 📊 分析问题
{question}

## 🎯 分析框架
请从以下维度进行深入分析：

### 1. 市场分析
- 市场规模和趋势
- 竞争格局分析
- 目标用户画像

### 2. 商业模式
- 价值主张分析
- 收入模式设计
- 成本结构优化

### 3. 战略建议
- 短期行动计划
- 长期战略规划
- 风险识别与应对

### 4. 实施路径
- 关键里程碑
- 资源需求评估
- Success指标设定

请提供具体、可执行的商业建议。"""

    @staticmethod
    def get_code_review_prompt(code: str, language: str = "python") -> str:
        """获取代码审查提示词"""
        return f"""# 代码审查任务

## 📝 代码内容
```{language}
{code}
```

## 🔍 审查维度
请从以下方面进行代码审查：

### 1. 代码质量
- 代码结构和组织
- 命名规范和可读性
- 注释和文档完整性

### 2. 性能优化
- 算法复杂度分析
- 内存Use优化
- 执行效率提升

### 3. 安全性
- 输入验证和ErrorProcessing
- 安全漏洞识别
- 最佳实践遵循

### 4. 改进建议
- 具体优化方案
- 重构建议
- 测试策略

请提供详细的代码审查报告和改进建议。"""

    @staticmethod
    def get_learning_path_prompt(topic: str, level: str = "beginner") -> str:
        """获取学习路径提示词"""
        return f"""# 学习路径规划

## 🎓 学习主题
{topic}

## 📚 学习目标
为{level}水平的学习者制定个性化学习路径

## 🗺️ 学习路径设计
请提供：

### 1. 学习阶段
- 基础阶段（2-4周）
- 进阶阶段（4-8周）
- 实战阶段（4-6周）

### 2. 学习资源
- 推荐书籍和文档
- 在线课程和教程
- 实践项目和练习

### 3. 技能树
- 核心技能清单
- 技能依赖关系
- 学习优先级

### 4. 评估方式
- 阶段性测试
- 项目作品集
- 技能认证

请制定详细、可执行的学习计划。"""

    @staticmethod
    def get_problem_solving_prompt(problem: str, domain: str = "技术") -> str:
        """获取问题解决提示词"""
        return f"""# 问题解决分析

## 🚨 问题描述
{problem}

## 🎯 解决框架
请按照以下步骤分析并解决问题：

### 1. 问题分析
- 问题本质和根本原因
- 影响范围和严重程度
- 约束条件和限制因素

### 2. 解决方案设计
- 多种解决方案对比
- 技术可行性分析
- 成本效益评估

### 3. 实施计划
- 详细实施步骤
- 时间节点和里程碑
- 资源需求分配

### 4. 风险控制
- 潜在风险识别
- 风险缓解措施
- 应急预案制定

### 5. 效果评估
- Success指标定义
- 监控和反馈机制
- 持续改进策略

请提供System性的问题解决方案。"""
