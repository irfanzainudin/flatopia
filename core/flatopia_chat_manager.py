"""
Flatopia AI Immigration Advisor Chat Manager
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from .simple_langchain_config import simple_langchain_config
from prompts.flatopia_prompts import FlatopiaPrompts
from .faiss_knowledge_base import get_faiss_kb
from .smart_search import smart_search
from .knowledge_updater import knowledge_updater

logger = logging.getLogger(__name__)

class FlatopiaChatManager:
    """Flatopia AI Immigration Advisor Chat Manager"""
    
    def __init__(self):
        self.llm = simple_langchain_config.llm
        self.prompts = FlatopiaPrompts()
        self.conversation_history = []
        self.user_profile = {}
        self.conversation_stage = "greeting"
        self.collected_info = {
            "name": False,
            "age": False,
            "nationality": False,
            "goal": False,  # work, study, or both
            "family": False,
            "profession": False,
            "education_level": False,
            "field_of_interest": False,
            "english_test": False,
            "budget": False,
            "priorities": False
        }
        
        # Initialize knowledge base, smart search, and knowledge updater
        self.knowledge_base = None  # Lazy initialization
        self.smart_search = smart_search
        self.knowledge_updater = knowledge_updater
    
    async def chat(self, user_input: str, chat_type: str = "general") -> Dict[str, Any]:
        """Process chat conversation"""
        try:
            # Record user input
            self.conversation_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Intelligent conversation processing - Check if user is answering previous questions
            response = await self._smart_conversation_handler(user_input)
            
            # Enhance response with knowledge base if appropriate
            if self._should_use_knowledge_base(user_input, self.conversation_stage):
                response = self._enhance_response_with_knowledge(user_input, response)
            
            # Update knowledge base with new information if appropriate
            self._update_knowledge_base_if_needed(user_input, response)
            
            # Record AI response
            self.conversation_history.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            return {
                "answer": response,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "chat_type": chat_type,
                "conversation_stage": self.conversation_stage
            }
            
        except Exception as e:
            return {
                "answer": f"Sorry, I encountered an error: {str(e)}",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "chat_type": chat_type,
                "conversation_stage": self.conversation_stage
            }
    
    async def _smart_conversation_handler(self, user_input: str) -> str:
        """Dynamic conversation processing based on collected information"""
        user_input_lower = user_input.lower()
        
        # Debug information
        print(f"DEBUG: Smart handler - User input: '{user_input}'")
        print(f"DEBUG: Collected info: {self.collected_info}")
        print(f"DEBUG: Conversation stage: {self.conversation_stage}")
        
        # Handle greeting
        if self.conversation_stage == "greeting":
            print("DEBUG: Processing greeting")
            return await self._handle_greeting(user_input)
        
        # Dynamic flow control - check what information is still needed
        missing_info = self._get_missing_essential_info()
        
        if missing_info:
            # Still need to collect essential information
            return await self._handle_missing_info(user_input, missing_info)
        else:
            # All essential information collected, proceed to recommendations/analysis
            return await self._handle_complete_profile(user_input)
    
    def _is_nationality_response(self, user_input: str) -> bool:
        """Check if it is a nationality response"""
        user_input_lower = user_input.lower()
        # 检查是否包含国家名称或国籍词汇
        country_indicators = ['from', 'country', 'nationality', 'citizen', 'born in', 'originally from']
        return any(indicator in user_input_lower for indicator in country_indicators) or len(user_input.split()) <= 3
    
    def _is_family_response(self, user_input: str) -> bool:
        """Check if it is a family status response"""
        user_input_lower = user_input.lower()
        family_indicators = ['single', 'married', 'divorced', 'widowed', 'partner', 'relationship', 'kids', 'children', 'family']
        return any(indicator in user_input_lower for indicator in family_indicators)
    
    def _is_profession_response(self, user_input: str) -> bool:
        """Check if it is a profession response"""
        user_input_lower = user_input.lower()
        profession_indicators = ['it', 'software', 'engineer', 'doctor', 'teacher', 'business', 'work', 'job', 'profession', 'field']
        return any(indicator in user_input_lower for indicator in profession_indicators)
    
    def _is_priorities_response(self, user_input: str) -> bool:
        """Check if it is a priorities response"""
        user_input_lower = user_input.lower()
        priority_indicators = ['safety', 'education', 'healthcare', 'job', 'democracy', 'cost', 'climate', 'diversity', 'stability']
        return any(indicator in user_input_lower for indicator in priority_indicators) or 'priority' in user_input_lower
    
    def _is_goal_response(self, user_input: str) -> bool:
        """Check if it is a goal response"""
        user_input_lower = user_input.lower()
        goal_indicators = ['study', 'work', 'migration', 'university', 'college', 'job', 'both']
        return any(indicator in user_input_lower for indicator in goal_indicators)
    
    def _is_education_level_response(self, user_input: str) -> bool:
        """Check if it is an education level response"""
        user_input_lower = user_input.lower()
        education_indicators = ['10th', '12th', 'bachelor', 'master', 'degree', 'grade', '1', '2', '3', '4', '5']
        return any(indicator in user_input_lower for indicator in education_indicators)
    
    def _is_field_response(self, user_input: str) -> bool:
        """Check if it is a field response"""
        user_input_lower = user_input.lower()
        field_indicators = ['engineering', 'tech', 'business', 'medicine', 'arts', 'humanities', 'science', '1', '2', '3', '4', '5', '6']
        return any(indicator in user_input_lower for indicator in field_indicators)
    
    def _is_english_test_response(self, user_input: str) -> bool:
        """Check if it is an English test response"""
        user_input_lower = user_input.lower()
        test_indicators = ['ielts', 'toefl', 'english', 'test', 'score', 'planning', 'already', 'sure']
        return any(indicator in user_input_lower for indicator in test_indicators)
    
    def _is_budget_response(self, user_input: str) -> bool:
        """Check if it is a budget response"""
        user_input_lower = user_input.lower()
        budget_indicators = ['budget', 'cost', 'tuition', 'fee', 'dollar', 'usd', 'affordable', 'expensive', '1', '2', '3', '4']
        return any(indicator in user_input_lower for indicator in budget_indicators)

    async def _handle_greeting(self, user_input: str) -> str:
        """ProcessingGreeting stage"""
        # First try to extract information from the greeting input
        self._extract_user_info(user_input)
        
        # Check if we got any essential information
        if self.user_profile.get('name') and self.user_profile.get('age') and self.user_profile.get('nationality') and self.user_profile.get('goal'):
            # User provided complete information, skip to analysis
            self.collected_info["name"] = True
            self.collected_info["age"] = True
            self.collected_info["nationality"] = True
            self.collected_info["goal"] = True
            
            # Check if user specified a country interest
            if self.user_profile.get('country_interest'):
                self.conversation_stage = "country_analysis"
                country = self.user_profile['country_interest']
                user_profile = str(self.user_profile)
                
                # Search knowledge base for information about this country
                knowledge_results = self._search_knowledge_base(f"study abroad {country} immigration visa requirements")
                
                # Create enhanced prompt with knowledge base information
                prompt = f"""
                User Profile: {user_profile}
                Selected Country: {country}
                
                Knowledge Base Information:
                {knowledge_results}
                
                Please provide a detailed analysis for studying in {country}, including:
                1. Visa requirements and process
                2. University recommendations
                3. Cost of living and tuition
                4. Language requirements
                5. Application timeline
                6. Work opportunities during/after studies
                """
                
                response = self.llm.chat_completion([{"role": "user", "content": prompt}])
                return response
            else:
                # Complete profile but no specific country, provide recommendations
                self.conversation_stage = "country_recommendations"
                return await self._handle_country_recommendations(user_input)
        else:
            # Incomplete information, proceed with normal flow
            return self.prompts.get_greeting_prompt()
    
    async def _handle_name_collection(self, user_input: str) -> str:
        """Handle name collection"""
        self._extract_user_info(user_input)
        if self.user_profile.get('name'):
            self.collected_info["name"] = True
            self.conversation_stage = "age_collection"
            return f"Nice to meet you, {self.user_profile['name']}! 😊 Now, could you tell me your age? This helps me provide more personalized recommendations."
        else:
            return "I'd love to know your name! What should I call you?"
    
    async def _handle_age_collection(self, user_input: str) -> str:
        """Handle age collection"""
        self._extract_user_info(user_input)
        if self.user_profile.get('age'):
            self.collected_info["age"] = True
            self.conversation_stage = "nationality_collection"
            user_name = self.user_profile.get('name', 'there')
            age = int(self.user_profile['age'])
            
            if age < 20:
                return f" Thank you, {user_name}! Since you're {age}, I'd love to know - are you primarily looking for study opportunities abroad, or are you also interested in work opportunities? This helps me tailor my recommendations perfectly for you! 🎓💼"
            else:
                return f" Perfect, {user_name}! Now, what country are you from? (e.g., India, China, Brazil, Colombia, etc.) This helps me understand your background better. Also, what are your main priorities when choosing a destination country? (e.g., job opportunities, education quality, cost of living, language, etc.)"
        else:
            user_name = self.user_profile.get('name', 'there')
            return f" I need to know your age to help you better, {user_name}. Could you please tell me your age?"
    
    async def _handle_nationality_collection(self, user_input: str) -> str:
        """Handle nationality collection and destination priorities"""
        self._extract_user_info(user_input)
        
        # Debug information
        print(f"DEBUG: User input: '{user_input}'")
        print(f"DEBUG: Extracted nationality: '{self.user_profile.get('nationality')}'")
        print(f"DEBUG: User profile: {self.user_profile}")
        
        user_name = self.user_profile.get('name', 'there')
        
        if self.user_profile.get('nationality'):
            self.collected_info["nationality"] = True
            self.collected_info["priorities"] = True  # Assume they mentioned priorities
            self.conversation_stage = "goal_collection"
            age = int(self.user_profile.get('age', 0))
            
            if age < 20:
                # 对于20岁以下的用户，直接询问学习目标
                return f""" Wonderful, {user_name}! I see you're from {self.user_profile['nationality']}. 

Since you're {age}, let me ask - what's your main goal? Are you looking to:
- 🎓 **Study abroad** (university, college, or language courses)
- 💼 **Work opportunities** (part-time work while studying)
- 🌍 **Both** (study first, then work and migrate)

This helps me tailor my recommendations perfectly for you!"""
            else:
                # 对于20岁以上的用户，询问工作目标
                return f""" Great, {user_name}! I see you're from {self.user_profile['nationality']}. 

What's your main goal? Are you looking to:
- 🎓 **Study abroad** (university, college, or language courses)
- 💼 **Work migration** (find a job and potentially settle permanently)
- 🌍 **Both** (study first, then work and migrate)

This helps me tailor my recommendations to your specific needs!"""
        else:
            # 更友好的提示，接受任何国籍
            return f" I didn't catch your nationality, {user_name}. Could you please tell me what country you're from? (e.g., India, China, Brazil, Colombia, etc.)"
    
    async def _handle_goal_collection(self, user_input: str) -> str:
        """Handle goal collection"""
        self._extract_user_info(user_input)
        
        # Debug information
        print(f"DEBUG: Goal collection - User input: '{user_input}'")
        print(f"DEBUG: User profile: {self.user_profile}")
        
        user_name = self.user_profile.get('name', 'there')
        age = int(self.user_profile.get('age', 0))
        
        # Determine user goal
        user_input_lower = user_input.lower()
        if 'study' in user_input_lower or 'university' in user_input_lower or 'college' in user_input_lower or 'studying' in user_input_lower:
            self.user_profile['goal'] = 'study'
        elif 'work' in user_input_lower or 'job' in user_input_lower or 'migration' in user_input_lower:
            self.user_profile['goal'] = 'work'
        elif 'both' in user_input_lower:
            self.user_profile['goal'] = 'both'
        else:
            # 根据年龄默认假设
            if age < 20:
                self.user_profile['goal'] = 'study'
            else:
                self.user_profile['goal'] = 'work'
        
        self.collected_info["goal"] = True
        
        # 根据目标进入不同流程
        if self.user_profile['goal'] == 'study':
            self.conversation_stage = "education_level_collection"
            return f" Excellent choice, {user_name}! Let's explore study opportunities for you. What's your current education level?"
        elif self.user_profile['goal'] == 'work':
            # 对于工作目标，如果年龄超过20岁，询问家庭情况
            if age >= 20:
                self.conversation_stage = "family_collection"
                return f" Great, {user_name}! Since you're interested in work migration, I'd like to know about your family situation. Are you single, married, or in a relationship? This helps me understand your priorities better."
            else:
                self.conversation_stage = "profession_collection"
                return f" Perfect, {user_name}! What's your profession or field of work? (e.g., IT, Engineering, Healthcare, Education, Business, etc.)"
        else:  # both
            self.conversation_stage = "education_level_collection"
            return f" Wonderful, {user_name}! Since you're interested in both study and work, let's start with your education background. What's your current education level?"
    
    async def _handle_education_level_collection(self, user_input: str) -> str:
        """Handle education level collection"""
        self._extract_user_info(user_input)
        
        # Debug information
        print(f"DEBUG: Education level collection - User input: '{user_input}'")
        print(f"DEBUG: User profile: {self.user_profile}")
        
        user_name = self.user_profile.get('name', 'there')
        
        # Determine education level
        user_input_lower = user_input.lower()
        if '1' in user_input_lower or '10th' in user_input_lower or 'tenth' in user_input_lower:
            self.user_profile['education_level'] = '10th grade'
        elif '2' in user_input_lower or '12th' in user_input_lower or 'twelfth' in user_input_lower or 'high school' in user_input_lower:
            self.user_profile['education_level'] = '12th grade'
        elif '3' in user_input_lower or 'bachelor' in user_input_lower or 'undergraduate' in user_input_lower:
            self.user_profile['education_level'] = 'Bachelor\'s degree'
        elif '4' in user_input_lower or 'master' in user_input_lower or 'graduate' in user_input_lower:
            self.user_profile['education_level'] = 'Master\'s degree'
        elif 'what' in user_input_lower or '?' in user_input:
            # 用户可能不理解问题，提供更清晰的选项
            return f" No worries, {user_name}! Let me clarify - what's your current education level? Please choose:\n\n1. 10th grade (or equivalent)\n2. 12th grade (or equivalent) \n3. Bachelor's degree\n4. Master's degree\n\nOr just tell me what level you're at!"
        else:
            self.user_profile['education_level'] = user_input
        
        self.collected_info["education_level"] = True
        self.conversation_stage = "field_collection"
        return f" Great, {user_name}! What field of study are you most interested in?"
    
    async def _handle_field_collection(self, user_input: str) -> str:
        """Handle field collection"""
        self._extract_user_info(user_input)
        
        # Debug information
        print(f"DEBUG: Field collection - User input: '{user_input}'")
        print(f"DEBUG: User profile: {self.user_profile}")
        
        user_name = self.user_profile.get('name', 'there')
        
        # Determine field of study
        user_input_lower = user_input.lower()
        if '1' in user_input_lower or 'engineering' in user_input_lower or 'tech' in user_input_lower or 'technology' in user_input_lower:
            self.user_profile['field_of_interest'] = 'Engineering/Tech'
        elif '2' in user_input_lower or 'business' in user_input_lower or 'management' in user_input_lower:
            self.user_profile['field_of_interest'] = 'Business/Management'
        elif '3' in user_input_lower or 'medicine' in user_input_lower or 'healthcare' in user_input_lower or 'medical' in user_input_lower:
            self.user_profile['field_of_interest'] = 'Medicine/Healthcare'
        elif '4' in user_input_lower or 'arts' in user_input_lower or 'humanities' in user_input_lower or 'eat' in user_input_lower or 'food' in user_input_lower or 'culinary' in user_input_lower:
            self.user_profile['field_of_interest'] = 'Culinary Arts/Food Science'
        elif '5' in user_input_lower or 'science' in user_input_lower:
            self.user_profile['field_of_interest'] = 'Science'
        else:
            self.user_profile['field_of_interest'] = user_input
        
        self.collected_info["field_of_interest"] = True
        self.conversation_stage = "english_test_collection"
        return f" Excellent choice, {user_name}! Do you already have English test scores (IELTS/TOEFL), or are you planning to take them?"
    
    async def _handle_english_test_collection(self, user_input: str) -> str:
        """Handle English test collection"""
        self._extract_user_info(user_input)
        
        # Debug information
        print(f"DEBUG: English test collection - User input: '{user_input}'")
        print(f"DEBUG: User profile: {self.user_profile}")
        
        user_name = self.user_profile.get('name', 'there')
        
        # Determine English test status
        user_input_lower = user_input.lower()
        if 'already' in user_input_lower or 'have' in user_input_lower or '7' in user_input_lower or '6' in user_input_lower or '8' in user_input_lower or '9' in user_input_lower:
            self.user_profile['english_test'] = 'Already have scores'
        elif 'ielts' in user_input_lower:
            self.user_profile['english_test'] = 'Planning IELTS'
        elif 'toefl' in user_input_lower:
            self.user_profile['english_test'] = 'Planning TOEFL'
        elif 'sure' in user_input_lower or 'not sure' in user_input_lower:
            self.user_profile['english_test'] = 'Not sure yet'
        else:
            self.user_profile['english_test'] = user_input
        
        self.collected_info["english_test"] = True
        self.conversation_stage = "budget_collection"
        return f" Perfect, {user_name}! Now, what's your budget range for studying abroad? This helps me recommend the most suitable options for you."
    
    async def _handle_budget_collection(self, user_input: str) -> str:
        """Handle budget collection"""
        self._extract_user_info(user_input)
        
        # Debug information
        print(f"DEBUG: Budget collection - User input: '{user_input}'")
        print(f"DEBUG: User profile: {self.user_profile}")
        
        user_name = self.user_profile.get('name', 'there')
        
        # Determine budget and priorities
        user_input_lower = user_input.lower()
        if '1' in user_input_lower or 'low' in user_input_lower or 'affordable' in user_input_lower or '111' in user_input_lower:
            self.user_profile['budget'] = 'Under $15,000 USD'
            self.user_profile['priorities'] = 'Low tuition fees'
        elif '2' in user_input_lower or 'work' in user_input_lower:
            self.user_profile['budget'] = '$15,000-30,000 USD'
            self.user_profile['priorities'] = 'Work opportunities during study'
        elif '3' in user_input_lower or 'pr' in user_input_lower or 'permanent' in user_input_lower:
            self.user_profile['budget'] = '$30,000+ USD'
            self.user_profile['priorities'] = 'Easy path to permanent residence'
        elif '4' in user_input_lower or 'all' in user_input_lower:
            self.user_profile['budget'] = 'Flexible'
            self.user_profile['priorities'] = 'All of the above'
        else:
            self.user_profile['budget'] = user_input
            self.user_profile['priorities'] = user_input
        
        self.collected_info["budget"] = True
        self.collected_info["priorities"] = True
        self.conversation_stage = "country_recommendations"
        
        # Create dynamic country recommendations
        user_profile = str(self.user_profile)
        priorities = self.user_profile.get('priorities', '')
        prompt = self._create_dynamic_recommendation_prompt(user_profile, priorities)
        response = self.llm.chat_completion([{"role": "user", "content": prompt}])
        
        # 在推荐前添加个性化称呼
        personalized_response = f" Based on your preferences, {user_name}, here are my recommendations:\n\n{response}"
        return personalized_response
    
    async def _handle_family_collection(self, user_input: str) -> str:
        """Handle family information collection"""
        self._extract_user_info(user_input)
        
        # Debug information
        print(f"DEBUG: Family collection - User input: '{user_input}'")
        print(f"DEBUG: Extracted family: '{self.user_profile.get('family')}'")
        print(f"DEBUG: User profile: {self.user_profile}")
        
        user_name = self.user_profile.get('name', 'there')
        
        # 检查是否已经收集到家庭信息
        if self.user_profile.get('family'):
            self.collected_info["family"] = True
            self.conversation_stage = "profession_collection"
            return f" Thank you for sharing that, {user_name}! Now, what's your profession or field of work? (e.g., IT, Engineering, Healthcare, Education, Business, etc.) This helps me understand your job opportunities in different countries."
        else:
            return f" I didn't catch your family status, {user_name}. Are you single, married, or in a relationship?"
    
    async def _handle_profession_collection(self, user_input: str) -> str:
        """Handle profession information collection"""
        self._extract_user_info(user_input)
        
        # Debug information
        print(f"DEBUG: Profession collection - User input: '{user_input}'")
        print(f"DEBUG: Extracted profession: '{self.user_profile.get('profession')}'")
        print(f"DEBUG: User profile: {self.user_profile}")
        
        user_name = self.user_profile.get('name', 'there')
        
        # 检查是否已经收集到职业信息
        if self.user_profile.get('profession'):
            self.collected_info["profession"] = True
            self.conversation_stage = "priorities_collection"
            return f" Perfect, {user_name}! Now, what are your main priorities when choosing a country? Please select the most important factors for you:"
        else:
            return f" I didn't catch your profession, {user_name}. What field do you work in? (e.g., IT, Engineering, Healthcare, Education, Business, etc.)"
    
    async def _handle_priorities_collection(self, user_input: str) -> str:
        """Handle priorities collection"""
        self.user_profile['priorities'] = user_input
        self.collected_info["priorities"] = True
        
        user_name = self.user_profile.get('name', 'there')
        
        # Check if user has already expressed interest in a specific country
        if self.user_profile.get('country_interest'):
            country = self.user_profile['country_interest']
            self.conversation_stage = "country_analysis"
            user_profile = str(self.user_profile)
            
            # Search knowledge base for information about this country
            knowledge_results = self._search_knowledge_base(f"study abroad {country} immigration visa requirements")
            
            # Create enhanced prompt with knowledge base information
            prompt = f"""
            User Profile: {user_profile}
            Selected Country: {country}
            
            Knowledge Base Information:
            {knowledge_results}
            
            Please provide a detailed analysis for studying in {country}, including:
            1. Visa requirements and process
            2. University recommendations
            3. Cost of living and tuition
            4. Language requirements
            5. Application timeline
            6. Work opportunities during/after studies
            """
            
            response = self.llm.chat_completion([{"role": "user", "content": prompt}])
            return response
        else:
            # No specific country interest, provide recommendations
            self.conversation_stage = "country_recommendations"
            
            # 生成国家推荐
            user_profile = str(self.user_profile)
            priorities = user_input
            prompt = self.prompts.get_country_recommendations_prompt(user_profile, priorities)
            response = self.llm.chat_completion([{"role": "user", "content": prompt}])
            
            # 在推荐前添加个性化称呼
            personalized_response = f" Based on your preferences, {user_name}, here are my recommendations:\n\n{response}"
            return personalized_response
    
    async def _handle_country_recommendations(self, user_input: str) -> str:
        """Handle country recommendation selection"""
        # Extract any country mentioned by user
        country = self._extract_country_from_input(user_input)
        if country:
            self.conversation_stage = "country_analysis"
            user_profile = str(self.user_profile)
            
            # Search knowledge base for information about this country
            knowledge_results = self._search_knowledge_base(f"study abroad {country} immigration visa requirements")
            
            # Create enhanced prompt with knowledge base information
            prompt = f"""
            User Profile: {user_profile}
            Selected Country: {country}
            
            Knowledge Base Information:
            {knowledge_results}
            
            Please provide a detailed analysis for studying in {country}, including:
            1. Visa requirements and process
            2. University recommendations
            3. Cost of living and tuition
            4. Language requirements
            5. Application timeline
            6. Work opportunities during/after studies
            """
            
            response = self.llm.chat_completion([{"role": "user", "content": prompt}])
            return response
        else:
            return " I didn't catch which country you're interested in. Please tell me which country you'd like to learn more about (e.g., Italy, Japan, Spain, etc.)."
    
    async def _handle_profile_collection(self, user_input: str) -> str:
        """Processing档案收集阶段"""
        # 提取用户信息
        self._extract_user_info(user_input)
        
        # 生成分析提示
        user_info = f"Age: {self.user_profile.get('age', 'Not specified')}, Nationality: {self.user_profile.get('nationality', 'Not specified')}, Family: {self.user_profile.get('family', 'Not specified')}, Profession: {self.user_profile.get('profession', 'Not specified')}"
        
        prompt = self.prompts.get_analysis_prompt(user_info)
        response = self.llm.chat_completion([{"role": "user", "content": prompt}])
        
        self.conversation_stage = "priorities"
        return response
    
    async def _handle_priorities(self, user_input: str) -> str:
        """Processing优先级询问阶段"""
        # 更新用户档案
        self._extract_user_info(user_input)
        
        # 生成国家推荐
        user_profile = str(self.user_profile)
        prompt = f"""Based on the user's priorities: {user_input}

User profile: {user_profile}

Provide country recommendations following this format:

 🔍 **Analysing your family profile...**

Based on your background, I've found **X excellent matches** for your family, ranked by your chances:

1. 🇨🇦 **CANADA** - [brief description of why it matches their priorities]
2. 🇦🇺 **AUSTRALIA** - [brief description of why it matches their priorities]  
3. 🇳🇿 **NEW ZEALAND** - [brief description of why it matches their priorities]
4. 🇬🇧 **UK** - [brief description of why it matches their priorities]

Which country would you like to explore first?

Be encouraging and explain why each country matches their specific priorities."""
        
        response = self.llm.chat_completion([{"role": "user", "content": prompt}])
        self.conversation_stage = "country_analysis"
        return response
    
    async def _handle_country_analysis(self, user_input: str) -> str:
        """Handle country analysis阶段"""
        # 确定用户感兴趣的国家
        country = "Canada"  # 默认
        if "australia" in user_input.lower() or "au" in user_input.lower():
            country = "Australia"
        elif "new zealand" in user_input.lower() or "nz" in user_input.lower():
            country = "New Zealand"
        elif "uk" in user_input.lower() or "britain" in user_input.lower() or "gb" in user_input.lower():
            country = "UK"
        elif "germany" in user_input.lower() or "de" in user_input.lower():
            country = "Germany"
        elif "usa" in user_input.lower() or "us" in user_input.lower() or "america" in user_input.lower():
            country = "USA"
        
        user_profile = str(self.user_profile)
        
        # 根据用户目标选择不同的分析prompt
        if self.user_profile.get('goal') == 'study':
            prompt = self.prompts.get_study_country_analysis_prompt(country, user_profile)
        else:
            prompt = self.prompts.get_detailed_analysis_prompt(country, user_profile)
        
        response = self.llm.chat_completion([{"role": "user", "content": prompt}])
        
        self.conversation_stage = "detailed_analysis"
        return response
    
    async def _handle_action_plan(self, user_input: str) -> str:
        """Handle action plan阶段"""
        user_profile = str(self.user_profile)
        prompt = self.prompts.get_action_plan_prompt(user_profile)
        response = self.llm.chat_completion([{"role": "user", "content": prompt}])
        
        self.conversation_stage = "action_plan"
        return response
    
    async def _handle_children_education(self, user_input: str) -> str:
        """Handle children education问题"""
        prompt = f"""The user asked about children's education: {user_input}

Provide a comprehensive response about children's education during immigration transition, including:

- Education in home country (preparation phase)
- During application process
- Upon landing in destination country
- Specific details for Canada and Australia
- Pro tips for smooth transition

Use the exact format and encouraging tone from the example conversation."""
        
        response = self.llm.chat_completion([{"role": "user", "content": prompt}])
        return response
    
    async def _handle_university_recommendations(self, user_input: str) -> str:
        """Handle university recommendations请求"""
        # 从对话历史中获取用户选择的国家
        country = "Canada"  # 默认
        for message in reversed(self.conversation_history):
            if message["role"] == "assistant" and "country" in message["content"].lower():
                content = message["content"].lower()
                if "australia" in content or "au" in content:
                    country = "Australia"
                elif "canada" in content or "ca" in content:
                    country = "Canada"
                elif "new zealand" in content or "nz" in content:
                    country = "New Zealand"
                elif "uk" in content or "britain" in content:
                    country = "UK"
                elif "germany" in content or "de" in content:
                    country = "Germany"
                elif "usa" in content or "us" in content:
                    country = "USA"
                break
        
        field = self.user_profile.get('field_of_interest', 'Engineering/Tech')
        budget = self.user_profile.get('budget', 'Under $15,000 USD')
        
        prompt = self.prompts.get_university_recommendations_prompt(country, field, budget)
        response = self.llm.chat_completion([{"role": "user", "content": prompt}])
        
        return response
    
    async def _handle_general_question(self, user_input: str) -> str:
        """Handle general questions"""
        context = f"User profile: {self.user_profile}\nConversation history: {self.conversation_history[-3:] if len(self.conversation_history) > 3 else self.conversation_history}"
        
        prompt = self.prompts.get_follow_up_prompt(user_input, context)
        response = self.llm.chat_completion([{"role": "user", "content": prompt}])
        
        return response
    
    def _create_dynamic_recommendation_prompt(self, user_profile: str, priorities: str) -> str:
        """创建动态推荐prompt"""
        return f"""Based on the following user profile, provide personalized country recommendations for study abroad:

User Profile: {user_profile}
Priorities: {priorities}

Please provide TOP 5 country recommendations with specific reasons why each country matches their profile. Consider:
- Their nationality and current location
- Their age and education level
- Their field of interest
- Their budget constraints
- Their English test status
- Their specific priorities

Format your response as:
1. 🇨🇦 **COUNTRY NAME** - [Specific reason why it matches their profile]
2. 🇦🇺 **COUNTRY NAME** - [Specific reason why it matches their profile]
3. 🇳🇿 **COUNTRY NAME** - [Specific reason why it matches their profile]
4. 🇬🇧 **COUNTRY NAME** - [Specific reason why it matches their profile]
5. 🇩🇪 **COUNTRY NAME** - [Specific reason why it matches their profile]

Make each recommendation specific to their situation and provide actionable insights."""

    def _extract_user_info(self, user_input: str) -> None:
        """Extract information from user input using LLM for complex inputs"""
        user_input_lower = user_input.lower()
        
        # If input is long or contains multiple pieces of information, use LLM to extract
        if (len(user_input.split()) > 2 or 
            len(user_input) > 10 or
            any(keyword in user_input_lower for keyword in ['study', 'work', 'italy', 'canada', 'australia', 'budget', 'english', 'ielts', 'toefl', 'age', 'name', 'from', 'want', 'go', 'college', 'university']) or
            any(keyword in user_input for keyword in ['我叫', '岁', '想去', '读书', '中国人', '年龄', '国籍', '目标', '学习', '工作'])):
            print(f"DEBUG: Triggering LLM extraction for input: '{user_input}'")
            self._extract_info_with_llm(user_input)
            return
        
        # Simple extraction for short inputs
        # Extract name - 如果还没有名字，尝试从输入中提取
        if not self.user_profile.get('name'):
            # 简单的名字提取逻辑
            words = user_input.strip().split()
            if len(words) == 1 and words[0].isalpha() and len(words[0]) > 1:
                # 如果只有一个词且是字母，可能是名字
                self.user_profile['name'] = words[0].title()
            elif len(words) == 2 and all(word.isalpha() for word in words):
                # 如果是两个词且都是字母，可能是全名，取第一个作为名字
                self.user_profile['name'] = words[0].title()
        
        # Extract age
        import re
        age_match = re.search(r'\b(\d{1,2})\b', user_input)
        if age_match:
            self.user_profile['age'] = age_match.group(1)
        
        # Extract nationality - 扩展词汇列表和匹配逻辑
        nationalities = [
            'colombian', 'mexican', 'indian', 'china', 'chinese', 'brazilian', 'philippine', 'vietnamese', 
            'nigerian', 'pakistani', 'bangladeshi', 'american', 'canadian', 'australian', 'british',
            'german', 'french', 'spanish', 'italian', 'japanese', 'korean', 'thai', 'indonesian',
            'malaysian', 'singaporean', 'taiwanese', 'hong kong', 'argentinian', 'chilean', 'peruvian',
            'venezuelan', 'ecuadorian', 'bolivian', 'uruguayan', 'paraguayan', 'cuban', 'dominican',
            'haitian', 'jamaican', 'trinidadian', 'barbadian', 'guyanese', 'surinamese', 'belizean',
            'panamanian', 'costa rican', 'honduran', 'salvadoran', 'guatemalan', 'nicaraguan',
            'russian', 'ukrainian', 'polish', 'czech', 'hungarian', 'romanian', 'bulgarian',
            'croatian', 'serbian', 'slovak', 'slovenian', 'estonian', 'latvian', 'lithuanian',
            'finnish', 'swedish', 'norwegian', 'danish', 'dutch', 'belgian', 'swiss', 'austrian',
            'portuguese', 'greek', 'turkish', 'israeli', 'lebanese', 'jordanian', 'saudi', 'emirati',
            'egyptian', 'moroccan', 'tunisian', 'algerian', 'libyan', 'sudanese', 'ethiopian',
            'kenyan', 'ugandan', 'tanzanian', 'ghanaian', 'ivorian', 'senegalese', 'cameroonian',
            'zimbabwean', 'south african', 'botswanan', 'namibian', 'zambian', 'malawian',
            'mozambican', 'angolan', 'congolese', 'rwandan', 'burundian', 'madagascan',
            'mauritian', 'seychellois', 'comorian', 'djiboutian', 'eritrean', 'somalian'
        ]
        
        # 更灵活的匹配逻辑
        for nationality in nationalities:
            if nationality in user_input_lower:
                self.user_profile['nationality'] = nationality.title()
                break
        
        # 如果没有匹配到，尝试提取任何看起来像国籍的词汇
        if not self.user_profile.get('nationality'):
            # 简单的启发式：如果用户输入了看起来像国籍的词
            words = user_input.strip().split()
            for word in words:
                if word.isalpha() and len(word) > 2:
                    # 检查是否可能是国籍
                    if word.lower() not in ['the', 'and', 'or', 'but', 'for', 'with', 'from', 'to', 'in', 'on', 'at', 'by', 'of', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall']:
                        self.user_profile['nationality'] = word.title()
                        break
            words = user_input_lower.split()
            for word in words:
                if len(word) > 2 and word.isalpha():
                    # 检查是否可能是国籍，排除常见的名字
                    common_names = ['yan', 'john', 'mary', 'david', 'sarah', 'michael', 'jennifer', 'robert', 'lisa', 'james', 'eason', 'alex', 'chris', 'sam', 'tom', 'nick', 'dan', 'ben', 'max', 'leo']
                    if word not in common_names and any(char.isalpha() for char in word):
                        self.user_profile['nationality'] = word.title()
                        break
        
        # Extract family information - 改进识别逻辑
        if 'single' in user_input_lower or 'unmarried' in user_input_lower or 'not married' in user_input_lower:
            self.user_profile['family'] = 'Single'
        elif 'married' in user_input_lower or 'husband' in user_input_lower or 'wife' in user_input_lower or 'spouse' in user_input_lower:
            self.user_profile['family'] = 'Married'
        elif 'divorced' in user_input_lower or 'separated' in user_input_lower:
            self.user_profile['family'] = 'Divorced/Separated'
        elif 'widowed' in user_input_lower:
            self.user_profile['family'] = 'Widowed'
        elif 'partner' in user_input_lower or 'boyfriend' in user_input_lower or 'girlfriend' in user_input_lower:
            self.user_profile['family'] = 'In a relationship'
        
        # 提取子女信息
        if 'kids' in user_input_lower or 'children' in user_input_lower or 'child' in user_input_lower:
            kids_match = re.search(r'(\d+)\s*(?:kids|children|child)', user_input_lower)
            if kids_match:
                self.user_profile['children'] = kids_match.group(1)
            else:
                self.user_profile['children'] = 'Yes'
        
        # Extract profession information - 扩展职业列表
        professions = [
            'it', 'software', 'developer', 'programmer', 'accountant', 'engineer', 'teacher', 'doctor', 'nurse', 'manager',
            'business', 'marketing', 'sales', 'finance', 'banking', 'law', 'lawyer', 'consultant', 'designer',
            'artist', 'writer', 'journalist', 'scientist', 'researcher', 'analyst', 'administrator', 'coordinator',
            'specialist', 'technician', 'assistant', 'director', 'executive', 'officer', 'supervisor', 'lead',
            'architect', 'consultant', 'freelancer', 'entrepreneur', 'student', 'graduate', 'intern'
        ]
        for profession in professions:
            if profession in user_input_lower:
                self.user_profile['profession'] = profession.title()
                break
        
        # 如果没有匹配到，尝试提取任何看起来像职业的词汇
        if not self.user_profile.get('profession'):
            words = user_input_lower.split()
            for word in words:
                if len(word) > 2 and word.isalpha():
                    # 检查是否可能是职业
                    if any(char.isalpha() for char in word):
                        self.user_profile['profession'] = word.title()
                        break
        
        # 提取教育信息
        if 'bachelor' in user_input_lower or 'degree' in user_input_lower:
            self.user_profile['education'] = 'Bachelor\'s degree'
        elif 'master' in user_input_lower:
            self.user_profile['education'] = 'Master\'s degree'
        elif 'phd' in user_input_lower or 'doctorate' in user_input_lower:
            self.user_profile['education'] = 'PhD'
    
    def _extract_country_from_input(self, user_input: str) -> str:
        """Extract country from user input - supports any country"""
        user_input_lower = user_input.lower()
        
        # Common country names and their variations
        countries = {
            'italy': ['italy', 'italian', 'italia'],
            'japan': ['japan', 'japanese', 'nippon'],
            'spain': ['spain', 'spanish', 'españa'],
            'france': ['france', 'french', 'français'],
            'germany': ['germany', 'german', 'deutschland'],
            'uk': ['uk', 'britain', 'british', 'england', 'scotland', 'wales'],
            'canada': ['canada', 'canadian'],
            'australia': ['australia', 'australian'],
            'new zealand': ['new zealand', 'kiwi', 'nz'],
            'usa': ['usa', 'america', 'american', 'united states'],
            'netherlands': ['netherlands', 'dutch', 'holland'],
            'sweden': ['sweden', 'swedish'],
            'norway': ['norway', 'norwegian'],
            'denmark': ['denmark', 'danish'],
            'finland': ['finland', 'finnish'],
            'switzerland': ['switzerland', 'swiss'],
            'austria': ['austria', 'austrian'],
            'belgium': ['belgium', 'belgian'],
            'ireland': ['ireland', 'irish'],
            'portugal': ['portugal', 'portuguese'],
            'greece': ['greece', 'greek'],
            'turkey': ['turkey', 'turkish'],
            'poland': ['poland', 'polish'],
            'czech republic': ['czech republic', 'czech', 'czechia'],
            'hungary': ['hungary', 'hungarian'],
            'romania': ['romania', 'romanian'],
            'bulgaria': ['bulgaria', 'bulgarian'],
            'croatia': ['croatia', 'croatian'],
            'slovenia': ['slovenia', 'slovenian'],
            'slovakia': ['slovakia', 'slovak'],
            'estonia': ['estonia', 'estonian'],
            'latvia': ['latvia', 'latvian'],
            'lithuania': ['lithuania', 'lithuanian'],
            'south korea': ['south korea', 'korea', 'korean'],
            'china': ['china', 'chinese'],
            'singapore': ['singapore', 'singaporean'],
            'malaysia': ['malaysia', 'malaysian'],
            'thailand': ['thailand', 'thai'],
            'vietnam': ['vietnam', 'vietnamese'],
            'philippines': ['philippines', 'filipino'],
            'indonesia': ['indonesia', 'indonesian'],
            'india': ['india', 'indian'],
            'brazil': ['brazil', 'brazilian'],
            'argentina': ['argentina', 'argentinian'],
            'chile': ['chile', 'chilean'],
            'mexico': ['mexico', 'mexican'],
            'colombia': ['colombia', 'colombian'],
            'peru': ['peru', 'peruvian'],
            'venezuela': ['venezuela', 'venezuelan'],
            'ecuador': ['ecuador', 'ecuadorian'],
            'bolivia': ['bolivia', 'bolivian'],
            'uruguay': ['uruguay', 'uruguayan'],
            'paraguay': ['paraguay', 'paraguayan'],
            'cuba': ['cuba', 'cuban'],
            'dominican republic': ['dominican republic', 'dominican'],
            'haiti': ['haiti', 'haitian'],
            'jamaica': ['jamaica', 'jamaican'],
            'trinidad and tobago': ['trinidad and tobago', 'trinidadian'],
            'barbados': ['barbados', 'barbadian'],
            'guyana': ['guyana', 'guyanese'],
            'suriname': ['suriname', 'surinamese'],
            'belize': ['belize', 'belizean'],
            'panama': ['panama', 'panamanian'],
            'costa rica': ['costa rica', 'costa rican'],
            'honduras': ['honduras', 'honduran'],
            'el salvador': ['el salvador', 'salvadoran'],
            'guatemala': ['guatemala', 'guatemalan'],
            'nicaragua': ['nicaragua', 'nicaraguan'],
            'russia': ['russia', 'russian'],
            'ukraine': ['ukraine', 'ukrainian'],
            'belarus': ['belarus', 'belarusian'],
            'moldova': ['moldova', 'moldovan'],
            'georgia': ['georgia', 'georgian'],
            'armenia': ['armenia', 'armenian'],
            'azerbaijan': ['azerbaijan', 'azerbaijani'],
            'kazakhstan': ['kazakhstan', 'kazakh'],
            'uzbekistan': ['uzbekistan', 'uzbek'],
            'kyrgyzstan': ['kyrgyzstan', 'kyrgyz'],
            'tajikistan': ['tajikistan', 'tajik'],
            'turkmenistan': ['turkmenistan', 'turkmen'],
            'afghanistan': ['afghanistan', 'afghan'],
            'pakistan': ['pakistan', 'pakistani'],
            'bangladesh': ['bangladesh', 'bangladeshi'],
            'sri lanka': ['sri lanka', 'sri lankan'],
            'nepal': ['nepal', 'nepalese'],
            'bhutan': ['bhutan', 'bhutanese'],
            'maldives': ['maldives', 'maldivian'],
            'myanmar': ['myanmar', 'burmese'],
            'cambodia': ['cambodia', 'cambodian'],
            'laos': ['laos', 'laotian'],
            'brunei': ['brunei', 'bruneian'],
            'east timor': ['east timor', 'timorese'],
            'mongolia': ['mongolia', 'mongolian'],
            'north korea': ['north korea', 'dprk'],
            'taiwan': ['taiwan', 'taiwanese'],
            'hong kong': ['hong kong', 'hongkong'],
            'macau': ['macau', 'macanese'],
            'israel': ['israel', 'israeli'],
            'palestine': ['palestine', 'palestinian'],
            'jordan': ['jordan', 'jordanian'],
            'lebanon': ['lebanon', 'lebanese'],
            'syria': ['syria', 'syrian'],
            'iraq': ['iraq', 'iraqi'],
            'iran': ['iran', 'iranian'],
            'saudi arabia': ['saudi arabia', 'saudi'],
            'uae': ['uae', 'united arab emirates', 'emirati'],
            'qatar': ['qatar', 'qatari'],
            'kuwait': ['kuwait', 'kuwaiti'],
            'bahrain': ['bahrain', 'bahraini'],
            'oman': ['oman', 'omani'],
            'yemen': ['yemen', 'yemeni'],
            'egypt': ['egypt', 'egyptian'],
            'libya': ['libya', 'libyan'],
            'tunisia': ['tunisia', 'tunisian'],
            'algeria': ['algeria', 'algerian'],
            'morocco': ['morocco', 'moroccan'],
            'sudan': ['sudan', 'sudanese'],
            'south sudan': ['south sudan', 'south sudanese'],
            'ethiopia': ['ethiopia', 'ethiopian'],
            'eritrea': ['eritrea', 'eritrean'],
            'djibouti': ['djibouti', 'djiboutian'],
            'somalia': ['somalia', 'somalian'],
            'kenya': ['kenya', 'kenyan'],
            'uganda': ['uganda', 'ugandan'],
            'tanzania': ['tanzania', 'tanzanian'],
            'rwanda': ['rwanda', 'rwandan'],
            'burundi': ['burundi', 'burundian'],
            'madagascar': ['madagascar', 'madagascan'],
            'mauritius': ['mauritius', 'mauritian'],
            'seychelles': ['seychelles', 'seychellois'],
            'comoros': ['comoros', 'comorian'],
            'ghana': ['ghana', 'ghanaian'],
            'nigeria': ['nigeria', 'nigerian'],
            'cameroon': ['cameroon', 'cameroonian'],
            'chad': ['chad', 'chadian'],
            'central african republic': ['central african republic', 'central african'],
            'congo': ['congo', 'congolese'],
            'democratic republic of congo': ['democratic republic of congo', 'drc', 'congolese'],
            'gabon': ['gabon', 'gabonese'],
            'equatorial guinea': ['equatorial guinea', 'equatorial guinean'],
            'sao tome and principe': ['sao tome and principe', 'sao tomean'],
            'angola': ['angola', 'angolan'],
            'zambia': ['zambia', 'zambian'],
            'zimbabwe': ['zimbabwe', 'zimbabwean'],
            'botswana': ['botswana', 'botswanan'],
            'namibia': ['namibia', 'namibian'],
            'south africa': ['south africa', 'south african'],
            'lesotho': ['lesotho', 'basotho'],
            'swaziland': ['swaziland', 'swazi'],
            'malawi': ['malawi', 'malawian'],
            'mozambique': ['mozambique', 'mozambican']
        }
        
        # Check for country matches
        for country, variations in countries.items():
            for variation in variations:
                if variation in user_input_lower:
                    return country.title()
        
        # If no match found, try to extract any capitalized word that might be a country
        words = user_input.strip().split()
        for word in words:
            if word.isalpha() and word[0].isupper() and len(word) > 2:
                # Check if it's not a common word
                if word.lower() not in ['the', 'and', 'or', 'but', 'for', 'with', 'from', 'to', 'in', 'on', 'at', 'by', 'of', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall', 'like', 'want', 'prefer', 'choose', 'select', 'pick']:
                    return word
        
        return None

    def _get_missing_essential_info(self) -> list:
        """Get list of essential information that is still missing"""
        essential_info = ["name", "age", "nationality", "goal"]
        missing = []
        
        for info in essential_info:
            if not self.collected_info.get(info, False):
                missing.append(info)
        
        return missing

    def _get_missing_optional_info(self) -> list:
        """Get list of optional information that is still missing based on user's goal"""
        optional_info = []
        
        if self.user_profile.get('goal') == 'study':
            study_info = ["education_level", "field_of_interest", "english_test", "budget"]
            for info in study_info:
                if not self.collected_info.get(info, False):
                    optional_info.append(info)
        elif self.user_profile.get('goal') == 'work':
            work_info = ["profession", "family", "priorities"]
            for info in work_info:
                if not self.collected_info.get(info, False):
                    optional_info.append(info)
        
        return optional_info

    async def _handle_missing_info(self, user_input: str, missing_info: list) -> str:
        """Handle missing information collection dynamically"""
        user_name = self.user_profile.get('name', 'there')
        
        # Check if user provided information in their input
        if self.user_profile.get('name') and 'name' in missing_info:
            missing_info.remove('name')
        if self.user_profile.get('age') and 'age' in missing_info:
            missing_info.remove('age')
        if self.user_profile.get('nationality') and 'nationality' in missing_info:
            missing_info.remove('nationality')
        if self.user_profile.get('goal') and 'goal' in missing_info:
            missing_info.remove('goal')
        
        # If all essential info is now collected, move to next stage
        if not missing_info:
            return await self._handle_complete_profile(user_input)
        
        # Ask for the first missing piece of information
        missing_type = missing_info[0]
        
        if missing_type == "name":
            return await self._handle_name_collection(user_input)
        elif missing_type == "age":
            return await self._handle_age_collection(user_input)
        elif missing_type == "nationality":
            return await self._handle_nationality_collection(user_input)
        elif missing_type == "goal":
            return await self._handle_goal_collection(user_input)
        else:
            return f" I need more information to help you better, {user_name}. Could you please provide more details?"

    async def _handle_complete_profile(self, user_input: str) -> str:
        """Handle when essential profile information is complete"""
        user_name = self.user_profile.get('name', 'there')
        
        # Check if user has expressed interest in a specific country
        if self.user_profile.get('country_interest'):
            country = self.user_profile['country_interest']
            self.conversation_stage = "country_analysis"
            user_profile = str(self.user_profile)
            
            # Search knowledge base for information about this country
            knowledge_results = self._search_knowledge_base(f"study abroad {country} immigration visa requirements")
            
            # Create enhanced prompt with knowledge base information
            prompt = f"""
            User Profile: {user_profile}
            Selected Country: {country}
            
            Knowledge Base Information:
            {knowledge_results}
            
            Please provide a detailed analysis for studying in {country}, including:
            1. Visa requirements and process
            2. University recommendations
            3. Cost of living and tuition
            4. Language requirements
            5. Application timeline
            6. Work opportunities during/after studies
            """
            
            response = self.llm.chat_completion([{"role": "user", "content": prompt}])
            return response
        
        # Check if we need to collect optional information
        missing_optional = self._get_missing_optional_info()
        if missing_optional:
            return await self._handle_optional_info_collection(user_input, missing_optional)
        
        # All information collected, provide recommendations
        self.conversation_stage = "country_recommendations"
        return await self._handle_country_recommendations(user_input)

    async def _handle_optional_info_collection(self, user_input: str, missing_optional: list) -> str:
        """Handle collection of optional information"""
        user_name = self.user_profile.get('name', 'there')
        
        # Check if user provided any of the missing optional information
        for info in missing_optional[:]:
            if self.user_profile.get(info):
                missing_optional.remove(info)
        
        # If all optional info is now collected, move to recommendations
        if not missing_optional:
            return await self._handle_complete_profile(user_input)
        
        # Ask for the first missing optional information
        missing_type = missing_optional[0]
        
        if missing_type == "education_level":
            return await self._handle_education_level_collection(user_input)
        elif missing_type == "field_of_interest":
            return await self._handle_field_collection(user_input)
        elif missing_type == "english_test":
            return await self._handle_english_test_collection(user_input)
        elif missing_type == "budget":
            return await self._handle_budget_collection(user_input)
        elif missing_type == "profession":
            return await self._handle_profession_collection(user_input)
        elif missing_type == "family":
            return await self._handle_family_collection(user_input)
        elif missing_type == "priorities":
            return await self._handle_priorities_collection(user_input)
        else:
            return f" I need a bit more information to provide better recommendations, {user_name}. Could you tell me more about your preferences?"

    def _extract_info_with_llm(self, user_input: str) -> None:
        """Use LLM to extract multiple pieces of information from complex input"""
        try:
            prompt = f"""
            Extract the following information from this user input: "{user_input}"
            
            The input may be in Chinese or English. Please extract:
            - Name: Look for patterns like "我叫X", "I'm X", "My name is X", "i'm X"
            - Age: Look for numbers followed by "岁", "years old", "age is X", or just numbers
            - Nationality: Look for "中国人", "Chinese", "India", "Indian", "au", "australia", "usa", "us", etc.
            - Goal: Look for "读书", "study", "工作", "work", "学习", "想去", "want to", "go to", "college", "university"
            - Country interest: Look for country names like "瑞士", "Switzerland", "意大利", "Italy", "china", "chinese"
            
            Return a JSON object with these fields (use null if not found):
            {{
                "name": "extracted name",
                "age": "extracted age as string",
                "nationality": "extracted nationality",
                "goal": "study/work/both",
                "education_level": "high school/bachelor/master/phd",
                "field_of_interest": "extracted field",
                "english_test": "yes/no/planning",
                "budget": "extracted budget info",
                "country_interest": "extracted country of interest",
                "priorities": "extracted priorities"
            }}
            
            Only extract information that is clearly stated. Be conservative - if uncertain, use null.
            """
            
            response = self.llm.chat_completion([{"role": "user", "content": prompt}])
            print(f"DEBUG: LLM extraction response: {response}")
            
            # Parse JSON response
            import json
            try:
                extracted_info = json.loads(response)
                print(f"DEBUG: Parsed extracted info: {extracted_info}")
                
                # Update user profile with extracted information
                for key, value in extracted_info.items():
                    if value and value != "null":
                        if key == "country_interest":
                            # Store country interest separately
                            self.user_profile["country_interest"] = value
                        else:
                            self.user_profile[key] = value
                            
                # Update collected info flags
                for key in ["name", "age", "nationality", "goal", "education_level", "field_of_interest", "english_test", "budget", "priorities"]:
                    if self.user_profile.get(key):
                        self.collected_info[key] = True
                        
            except json.JSONDecodeError:
                # Fallback to simple extraction if JSON parsing fails
                pass
                
        except Exception as e:
            print(f"Error in LLM extraction: {e}")
            # Fallback to simple extraction
            pass

    def reset_conversation(self) -> None:
        """重置对话"""
        self.conversation_history = []
        self.user_profile = {}
        self.conversation_stage = "greeting"
        self.collected_info = {
            "age": False,
            "nationality": False,
            "goal": False,
            "family": False,
            "profession": False,
            "education_level": False,
            "field_of_interest": False,
            "english_test": False,
            "budget": False,
            "priorities": False
        }

    def _get_knowledge_base(self):
        """Get knowledge base instance (lazy initialization)"""
        if self.knowledge_base is None:
            self.knowledge_base = get_faiss_kb()
        return self.knowledge_base
    
    def _search_knowledge_base(self, query: str, search_type: str = "auto") -> Dict[str, Any]:
        """
        Search the knowledge base for relevant information
        
        Args:
            query: Search query
            search_type: Type of search ("auto", "universities", "visas", "both")
            
        Returns:
            Dictionary containing search results
        """
        try:
            kb = self._get_knowledge_base()
            if not kb.is_available():
                return {"error": "Knowledge base not available"}
            
            # Perform smart search using the smart search strategy
            results = self.smart_search.smart_search(query, max_results=5)
            
            # Format results for LLM consumption
            formatted_results = self._format_knowledge_results(results)
            
            return {
                "success": True,
                "results": formatted_results,
                "search_type": results.get("metadata", {}).get("intent_analysis", {}).get("primary_intent", "auto"),
                "query": query
            }
            
        except Exception as e:
            return {"error": f"Knowledge base search failed: {str(e)}"}
    
    def _format_knowledge_results(self, results: Dict[str, Any]) -> str:
        """
        Format knowledge base results for LLM consumption
        
        Args:
            results: Raw search results from knowledge base
            
        Returns:
            Formatted string for LLM
        """
        formatted = []
        
        # Format university results
        if results.get("universities"):
            formatted.append("🎓 **UNIVERSITY INFORMATION:**")
            for i, result in enumerate(results["universities"][:3], 1):
                content = result.get("content", "")
                metadata = result.get("metadata", {})
                formatted.append(f"{i}. {content}")
                if metadata:
                    formatted.append(f"   Additional info: {metadata}")
            formatted.append("")
        
        # Format visa results
        if results.get("visas"):
            formatted.append("🛂 **VISA & IMMIGRATION INFORMATION:**")
            for i, result in enumerate(results["visas"][:3], 1):
                content = result.get("content", "")
                metadata = result.get("metadata", {})
                formatted.append(f"{i}. {content}")
                if metadata:
                    formatted.append(f"   Additional info: {metadata}")
            formatted.append("")
        
        return "\n".join(formatted) if formatted else "No relevant information found in knowledge base."
    
    def _should_use_knowledge_base(self, user_input: str, conversation_stage: str) -> bool:
        """
        Determine if knowledge base should be used for this query
        
        Args:
            user_input: User's input
            conversation_stage: Current conversation stage
            
        Returns:
            Boolean indicating whether to use knowledge base
        """
        # Use knowledge base for specific stages or when user asks specific questions
        knowledge_stages = [
            "country_recommendations", 
            "university_recommendations", 
            "country_analysis",
            "action_planning"
        ]
        
        # Check if in a knowledge-relevant stage
        if conversation_stage in knowledge_stages:
            return True
        
        # Check for knowledge-seeking keywords
        knowledge_keywords = [
            "university", "college", "school", "education", "program", "course",
            "visa", "immigration", "work permit", "residence", "citizenship",
            "tuition", "scholarship", "admission", "requirements", "application"
        ]
        
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in knowledge_keywords)
    
    def _enhance_response_with_knowledge(self, user_input: str, base_response: str) -> str:
        """
        Enhance the base response with knowledge base information
        
        Args:
            user_input: User's input
            base_response: Base response from LLM
            
        Returns:
            Enhanced response with knowledge base information
        """
        try:
            # Search knowledge base
            kb_results = self._search_knowledge_base(user_input)
            
            if kb_results.get("success") and kb_results.get("results"):
                knowledge_info = kb_results["results"]
                
                # Create enhanced prompt
                enhanced_prompt = f"""
Based on the following knowledge base information, enhance your response to be more accurate and helpful:

KNOWLEDGE BASE INFORMATION:
{knowledge_info}

ORIGINAL RESPONSE:
{base_response}

USER QUESTION:
{user_input}

Please provide an enhanced response that incorporates the relevant knowledge base information while maintaining a natural conversation flow. If the knowledge base information is not relevant, use your original response.
"""
                
                # Get enhanced response from LLM
                enhanced_response = self.llm.invoke(enhanced_prompt)
                return enhanced_response
            else:
                return base_response
                
        except Exception as e:
            # If knowledge base fails, return original response
            return base_response
    
    def _update_knowledge_base_if_needed(self, user_input: str, response: str):
        """
        Update knowledge base with new information if appropriate
        
        Args:
            user_input: User's input
            response: AI's response
        """
        try:
            # Check if knowledge base is available
            kb = self._get_knowledge_base()
            if not kb.is_available():
                return
            
            # Update knowledge base
            update_result = self.knowledge_updater.update_knowledge_base(user_input, response)
            
            if update_result.get("success"):
                logger.info(f"✅ Knowledge base updated: {update_result['updated_chunks']} chunks added")
            else:
                logger.debug(f"ℹ️ Knowledge base not updated: {update_result.get('reason', 'Unknown reason')}")
                
        except Exception as e:
            logger.error(f"❌ Error updating knowledge base: {e}")
    
    def get_knowledge_base_status(self) -> Dict[str, Any]:
        """
        Get knowledge base status and statistics
        
        Returns:
            Dictionary containing knowledge base status
        """
        try:
            # Get knowledge base summary
            kb = self._get_knowledge_base()
            kb_summary = kb.get_knowledge_summary()
            
            # Get update statistics
            update_stats = self.knowledge_updater.get_update_statistics()
            
            return {
                "knowledge_base": kb_summary,
                "update_statistics": update_stats,
                "smart_search_available": self.smart_search is not None,
                "knowledge_updater_available": self.knowledge_updater is not None
            }
            
        except Exception as e:
            return {"error": f"Failed to get knowledge base status: {str(e)}"}

# Global Flatopia Chat manager instance
flatopia_chat_manager = FlatopiaChatManager()
