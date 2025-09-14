"""
移民咨询专用Chat manager
"""
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from .simple_langchain_config import simple_langchain_config
from prompts.immigration_prompts import ImmigrationPrompts


class ImmigrationChatManager:
    """移民咨询Chat manager"""
    
    def __init__(self):
        self.langchain_config = simple_langchain_config
        self.prompts = ImmigrationPrompts()
        self.conversation_history = []
        self.user_profile = {}
        self.max_history = 20
        
        # 移民相关数据
        self.countries_data = self._load_countries_data()
        self.visa_types = self._load_visa_types()
    
    def _load_countries_data(self) -> Dict[str, Dict[str, Any]]:
        """Loading国家数据"""
        return {
            "加拿大": {
                "official_languages": ["英语", "法语"],
                "work_languages": ["英语", "法语"],
                "visa_types": ["工作签证", "学习签证", "投资移民", "技术移民"],
                "pr_requirements": {"居住时间": "5年内住满3年", "语言要求": "CLB 4级"},
                "popular_cities": ["多伦多", "温哥华", "蒙特利尔", "卡尔加里"]
            },
            "澳大利亚": {
                "official_languages": ["英语"],
                "work_languages": ["英语"],
                "visa_types": ["技术移民", "投资移民", "学习签证", "工作签证"],
                "pr_requirements": {"居住时间": "4年内住满2年", "语言要求": "雅思6分"},
                "popular_cities": ["悉尼", "墨尔本", "布里斯班", "珀斯"]
            },
            "新西兰": {
                "official_languages": ["英语", "毛利语"],
                "work_languages": ["英语"],
                "visa_types": ["技术移民", "投资移民", "学习签证", "工作假期签证"],
                "pr_requirements": {"居住时间": "5年内住满2年", "语言要求": "雅思6.5分"},
                "popular_cities": ["奥克兰", "惠灵顿", "基督城", "汉密尔顿"]
            },
            "美国": {
                "official_languages": ["英语"],
                "work_languages": ["英语"],
                "visa_types": ["H1B工作签证", "F1学生签证", "EB-5投资移民", "L1签证"],
                "pr_requirements": {"居住时间": "5年", "语言要求": "英语基础"},
                "popular_cities": ["纽约", "洛杉矶", "旧金山", "芝加哥"]
            },
            "英国": {
                "official_languages": ["英语"],
                "work_languages": ["英语"],
                "visa_types": ["技术工人签证", "学生签证", "投资移民", "创新者签证"],
                "pr_requirements": {"居住时间": "5年", "语言要求": "B1水平"},
                "popular_cities": ["伦敦", "曼彻斯特", "伯明翰", "爱丁堡"]
            },
            "德国": {
                "official_languages": ["德语"],
                "work_languages": ["德语", "英语"],
                "visa_types": ["工作签证", "学习签证", "蓝卡", "自雇签证"],
                "pr_requirements": {"居住时间": "5年", "语言要求": "B1德语"},
                "popular_cities": ["柏林", "慕尼黑", "汉堡", "法兰克福"]
            },
            "日本": {
                "official_languages": ["日语"],
                "work_languages": ["日语", "英语"],
                "visa_types": ["工作签证", "学习签证", "投资经营签证", "高度人才签证"],
                "pr_requirements": {"居住时间": "10年", "语言要求": "N1日语"},
                "popular_cities": ["东京", "大阪", "横滨", "名古屋"]
            }
        }
    
    def _load_visa_types(self) -> Dict[str, Dict[str, Any]]:
        """Loading签证类型数据"""
        return {
            "工作签证": {
                "description": "基于工作机会的临时居留签证",
                "requirements": ["工作邀请", "技能认证", "语言能力"],
                "duration": "1-4年",
                "pr_path": "是"
            },
            "学习签证": {
                "description": "基于教育机会的学生签证",
                "requirements": ["录取通知书", "资金证明", "语言能力"],
                "duration": "课程期间",
                "pr_path": "毕业后可转换"
            },
            "技术移民": {
                "description": "基于技能和经验的移民签证",
                "requirements": ["技能评估", "语言考试", "工作经验"],
                "duration": "永久",
                "pr_path": "直接获得"
            },
            "投资移民": {
                "description": "基于投资金额的移民签证",
                "requirements": ["投资资金", "商业计划", "资金来源证明"],
                "duration": "永久",
                "pr_path": "直接获得"
            }
        }
    
    async def chat(self, 
                   user_input: str, 
                   chat_type: str = "immigration_analysis") -> Dict[str, Any]:
        """
        Processing移民咨询对话
        
        Args:
            user_input: 用户输入
            chat_type: 聊天类型 (profile_collection, immigration_analysis, visa_guide, pr_planning, country_comparison)
            
        Returns:
            包含回复和相关信息的字典
        """
        try:
            # 添加用户消息到历史
            self._add_message("user", user_input)
            
            # 根据类型选择Processing方式
            if chat_type == "profile_collection":
                result = await self._handle_profile_collection(user_input)
            elif chat_type == "immigration_analysis":
                result = await self._handle_immigration_analysis(user_input)
            elif chat_type == "visa_guide":
                result = await self._handle_visa_guide(user_input)
            elif chat_type == "pr_planning":
                result = await self._handle_pr_planning(user_input)
            elif chat_type == "country_comparison":
                result = await self._handle_country_comparison(user_input)
            else:
                result = await self._handle_general_immigration_chat(user_input)
            
            # 添加助手回复到历史
            self._add_message("assistant", result["answer"])
            
            return {
                **result,
                "timestamp": datetime.now().isoformat(),
                "chat_type": chat_type,
                "success": True
            }
            
        except Exception as e:
            error_msg = f"Processing移民咨询时出错: {str(e)}"
            self._add_message("assistant", error_msg)
            
            return {
                "answer": error_msg,
                "timestamp": datetime.now().isoformat(),
                "chat_type": chat_type,
                "success": False,
                "error": str(e)
            }
    
    async def _handle_profile_collection(self, user_input: str) -> Dict[str, Any]:
        """Processing用户信息收集"""
        try:
            # Use用户信息收集提示词
            prompt = self.prompts.get_user_profile_prompt()
            
            # 获取LLM回复
            response = self.langchain_config.get_llm_response(prompt)
            
            # 尝试从用户输入中提取信息
            extracted_info = self._extract_user_info(user_input)
            if extracted_info:
                self.user_profile.update(extracted_info)
            
            return {
                "answer": response,
                "extracted_info": extracted_info,
                "user_profile": self.user_profile
            }
            
        except Exception as e:
            raise Exception(f"用户信息收集Failed: {str(e)}")
    
    async def _handle_immigration_analysis(self, user_input: str) -> Dict[str, Any]:
        """Processing移民分析"""
        try:
            # Use移民分析提示词
            prompt = self.prompts.get_immigration_analysis_prompt(self.user_profile)
            
            # 获取LLM回复
            response = self.langchain_config.get_llm_response(prompt)
            
            return {
                "answer": response,
                "user_profile": self.user_profile
            }
            
        except Exception as e:
            raise Exception(f"移民分析Failed: {str(e)}")
    
    async def _handle_visa_guide(self, user_input: str) -> Dict[str, Any]:
        """Processing签证指南"""
        try:
            # 从用户输入中提取国家和签证类型
            country, visa_type = self._extract_country_and_visa_type(user_input)
            
            if not country or not visa_type:
                return {
                    "answer": "请指定目标国家和签证类型，例如：我想了解加拿大的工作签证申请指南。",
                    "user_profile": self.user_profile
                }
            
            # Use签证指南提示词
            prompt = self.prompts.get_visa_guide_prompt(country, visa_type, self.user_profile)
            
            # 获取LLM回复
            response = self.langchain_config.get_llm_response(prompt)
            
            return {
                "answer": response,
                "country": country,
                "visa_type": visa_type,
                "user_profile": self.user_profile
            }
            
        except Exception as e:
            raise Exception(f"签证指南生成Failed: {str(e)}")
    
    async def _handle_pr_planning(self, user_input: str) -> Dict[str, Any]:
        """Processing永久居民规划"""
        try:
            # 从用户输入中提取国家
            country = self._extract_country(user_input)
            current_status = self._extract_current_status(user_input)
            
            if not country:
                return {
                    "answer": "请指定目标国家，例如：我想了解加拿大的永久居民申请规划。",
                    "user_profile": self.user_profile
                }
            
            # Use永久居民规划提示词
            prompt = self.prompts.get_pr_planning_prompt(country, current_status, self.user_profile)
            
            # 获取LLM回复
            response = self.langchain_config.get_llm_response(prompt)
            
            return {
                "answer": response,
                "country": country,
                "current_status": current_status,
                "user_profile": self.user_profile
            }
            
        except Exception as e:
            raise Exception(f"永久居民规划Failed: {str(e)}")
    
    async def _handle_country_comparison(self, user_input: str) -> Dict[str, Any]:
        """Processing国家对比"""
        try:
            # 从用户输入中提取国家列表
            countries = self._extract_countries(user_input)
            
            if not countries:
                return {
                    "answer": "请指定要对比的国家，例如：请对比加拿大、澳大利亚和新西兰的移民政策。",
                    "user_profile": self.user_profile
                }
            
            # Use国家对比提示词
            prompt = self.prompts.get_country_comparison_prompt(countries, self.user_profile)
            
            # 获取LLM回复
            response = self.langchain_config.get_llm_response(prompt)
            
            return {
                "answer": response,
                "countries": countries,
                "user_profile": self.user_profile
            }
            
        except Exception as e:
            raise Exception(f"国家对比Failed: {str(e)}")
    
    async def _handle_general_immigration_chat(self, user_input: str) -> Dict[str, Any]:
        """Processing一般移民咨询"""
        try:
            # 构建一般移民咨询提示词
            system_prompt = self.prompts.get_system_prompt()
            chat_history = self._get_chat_history_formatted()
            
            prompt = f"""{system_prompt}

## 对话历史
{chat_history}

## 用户问题
{user_input}

请根据用户的问题和背景信息，提供专业的移民咨询建议。"""
            
            # 获取LLM回复
            response = self.langchain_config.get_llm_response(prompt)
            
            return {
                "answer": response,
                "user_profile": self.user_profile
            }
            
        except Exception as e:
            raise Exception(f"一般移民咨询Failed: {str(e)}")
    
    def _extract_user_info(self, user_input: str) -> Dict[str, Any]:
        """从用户输入中提取信息"""
        extracted = {}
        
        # 简单的关键词提取（实际Application中可以Use更复杂的NLP技术）
        if "年龄" in user_input or "岁" in user_input:
            # 提取年龄
            import re
            age_match = re.search(r'(\d+)岁?', user_input)
            if age_match:
                extracted["age"] = int(age_match.group(1))
        
        if "男" in user_input:
            extracted["gender"] = "男"
        elif "女" in user_input:
            extracted["gender"] = "女"
        
        # 提取国籍
        for country in self.countries_data.keys():
            if country in user_input:
                extracted["nationality"] = country
                break
        
        # 提取目标国家
        for country in self.countries_data.keys():
            if f"去{country}" in user_input or f"移民{country}" in user_input:
                extracted["target_country"] = country
                break
        
        return extracted
    
    def _extract_country_and_visa_type(self, user_input: str) -> tuple:
        """提取国家和签证类型"""
        country = None
        visa_type = None
        
        # 提取国家
        for c in self.countries_data.keys():
            if c in user_input:
                country = c
                break
        
        # 提取签证类型
        for v in self.visa_types.keys():
            if v in user_input:
                visa_type = v
                break
        
        return country, visa_type
    
    def _extract_country(self, user_input: str) -> str:
        """提取国家"""
        for country in self.countries_data.keys():
            if country in user_input:
                return country
        return None
    
    def _extract_current_status(self, user_input: str) -> str:
        """提取当前身份状态"""
        status_keywords = {
            "学生": "学生签证",
            "工作": "工作签证",
            "旅游": "旅游签证",
            "临时": "临时居留",
            "永久": "永久居民"
        }
        
        for keyword, status in status_keywords.items():
            if keyword in user_input:
                return status
        
        return "未知"
    
    def _extract_countries(self, user_input: str) -> List[str]:
        """提取国家列表"""
        countries = []
        for country in self.countries_data.keys():
            if country in user_input:
                countries.append(country)
        return countries
    
    def _add_message(self, role: str, content: str):
        """添加消息到历史记录"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.conversation_history.append(message)
        
        # 保持历史记录在限制范围内
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def _get_chat_history_formatted(self) -> str:
        """获取格式化的对话历史"""
        if not self.conversation_history:
            return ""
        
        history_parts = []
        for msg in self.conversation_history[-10:]:  # 只保留最近10条
            role = "用户" if msg["role"] == "user" else "顾问"
            history_parts.append(f"{role}: {msg['content']}")
        
        return "\n".join(history_parts)
    
    def get_user_profile(self) -> Dict[str, Any]:
        """获取用户档案"""
        return self.user_profile.copy()
    
    def update_user_profile(self, profile_data: Dict[str, Any]):
        """更新用户档案"""
        self.user_profile.update(profile_data)
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
    
    def get_available_countries(self) -> List[str]:
        """获取可用国家列表"""
        return list(self.countries_data.keys())
    
    def get_available_visa_types(self) -> List[str]:
        """获取可用签证类型列表"""
        return list(self.visa_types.keys())
    
    def get_country_info(self, country: str) -> Dict[str, Any]:
        """获取国家信息"""
        return self.countries_data.get(country, {})
    
    def get_visa_info(self, visa_type: str) -> Dict[str, Any]:
        """获取签证信息"""
        return self.visa_types.get(visa_type, {})


# 全局移民咨询Chat manager实例
immigration_chat_manager = ImmigrationChatManager()
