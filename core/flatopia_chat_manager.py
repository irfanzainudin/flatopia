"""
Flatopia AI Immigration Advisor Chat Manager
"""
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from .simple_langchain_config import simple_langchain_config
from prompts.flatopia_prompts import FlatopiaPrompts

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
    
    async def chat(self, user_input: str, chat_type: str = "general") -> Dict[str, Any]:
        """Process chat conversation"""
        try:
            # Record user input
            self.conversation_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
            
            # Intelligent conversation processing - 检查用户是否在回答之前的问题
            response = await self._smart_conversation_handler(user_input)
            
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
        """Intelligent conversation processing - 严格按照顺序Processing"""
        user_input_lower = user_input.lower()
        
        # Debug information
        print(f"DEBUG: Smart handler - User input: '{user_input}'")
        print(f"DEBUG: Collected info: {self.collected_info}")
        print(f"DEBUG: Conversation stage: {self.conversation_stage}")
        
        # Strictly check in order，不跳过任何步骤
        if self.conversation_stage == "greeting":
            # Greeting stage - 显示问候语并进入Name collection stage
            print("DEBUG: Processing greeting")
            self.conversation_stage = "name_collection"
            return await self._handle_greeting(user_input)
        
        elif not self.collected_info["name"]:
            # Name collection stage
            print("DEBUG: Processing name collection")
            return await self._handle_name_collection(user_input)
        
        elif not self.collected_info["age"]:
            # Age collection stage
            print("DEBUG: Processing age collection")
            return await self._handle_age_collection(user_input)
        
        elif not self.collected_info["nationality"]:
            # Nationality collection stage 
            user_input_lower = user_input.lower()
            if 'study' in user_input_lower or 'work' in user_input_lower or 'both' in user_input_lower:
                # 用户已经回答了目标问题，跳过国籍收集直接进入目标收集
                self.collected_info["nationality"] = True
                self.conversation_stage = "goal_collection"
                return await self._handle_goal_collection(user_input)
            else:
                return await self._handle_nationality_collection(user_input)
        
        elif not self.collected_info["goal"]:
            # Goal collection stage
            user_input_lower = user_input.lower()
            if 'study' in user_input_lower or 'work' in user_input_lower or 'both' in user_input_lower:
                return await self._handle_goal_collection(user_input)
            else:
                return await self._handle_goal_collection(user_input)
        
        elif self.user_profile.get('goal') == 'study':
            # Study-related process
            if not self.collected_info["education_level"]:
                if self._is_education_level_response(user_input):
                    return await self._handle_education_level_collection(user_input)
                else:
                    return await self._handle_education_level_collection(user_input)
            elif not self.collected_info["field_of_interest"]:
                if self._is_field_response(user_input):
                    return await self._handle_field_collection(user_input)
                else:
                    return await self._handle_field_collection(user_input)
            elif not self.collected_info["english_test"]:
                if self._is_english_test_response(user_input):
                    return await self._handle_english_test_collection(user_input)
                else:
                    return await self._handle_english_test_collection(user_input)
            elif not self.collected_info["budget"]:
                if self._is_budget_response(user_input):
                    return await self._handle_budget_collection(user_input)
                else:
                    return await self._handle_budget_collection(user_input)
        
        elif not self.collected_info["family"]:
            # Work-related process - Family info
            if self._is_family_response(user_input):
                return await self._handle_family_collection(user_input)
            else:
                return await self._handle_family_collection(user_input)
        
        elif not self.collected_info["profession"]:
            # Work-related process - profession info
            if self._is_profession_response(user_input):
                return await self._handle_profession_collection(user_input)
            else:
                return await self._handle_profession_collection(user_input)
        
        elif not self.collected_info["priorities"]:
            # 优先级收集阶段
            if self._is_priorities_response(user_input):
                return await self._handle_priorities_collection(user_input)
            else:
                return await self._handle_priorities_collection(user_input)
        
        # 后续阶段Processi
        if self.conversation_stage == "country_recommendations":
            return await self._handle_country_recommendations(user_input)
        elif self.conversation_stage == "country_analysis":
            return await self._handle_country_analysis(user_input)
        elif "plan" in user_input_lower or "timeline" in user_input_lower or "step" in user_input_lower:
            return await self._handle_action_plan(user_input)
        elif "children" in user_input_lower or "education" in user_input_lower or "kids" in user_input_lower:
            return await self._handle_children_education(user_input)
        elif "university" in user_input_lower or "universities" in user_input_lower or "yes" in user_input_lower:
            return await self._handle_university_recommendations(user_input)
        else:
            return await self._handle_general_question(user_input)
    
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
        # 不立即改变对话阶段，让用户看到问候语后再进入下一阶段
        return self.prompts.get_greeting_prompt()
    
    async def _handle_name_collection(self, user_input: str) -> str:
        """Handle name collection"""
        self._extract_user_info(user_input)
        if self.user_profile.get('name'):
            self.collected_info["name"] = True
            self.conversation_stage = "age_collection"
            return f"**Flatopia AI**: Nice to meet you, {self.user_profile['name']}! 😊 Now, could you tell me your age? This helps me provide more personalized recommendations."
        else:
            return "**Flatopia AI**: I'd love to know your name! What should I call you?"
    
    async def _handle_age_collection(self, user_input: str) -> str:
        """Handle age collection"""
        self._extract_user_info(user_input)
        if self.user_profile.get('age'):
            self.collected_info["age"] = True
            self.conversation_stage = "nationality_collection"
            user_name = self.user_profile.get('name', 'there')
            age = int(self.user_profile['age'])
            
            if age < 20:
                return f"**Flatopia AI**: Thank you, {user_name}! Since you're {age}, I'd love to know - are you primarily looking for study opportunities abroad, or are you also interested in work opportunities? This helps me tailor my recommendations perfectly for you! 🎓💼"
            else:
                return f"**Flatopia AI**: Perfect, {user_name}! Now, what country are you from? (e.g., India, China, Brazil, Colombia, etc.) This helps me understand your background better."
        else:
            user_name = self.user_profile.get('name', 'there')
            return f"**Flatopia AI**: I need to know your age to help you better, {user_name}. Could you please tell me your age?"
    
    async def _handle_nationality_collection(self, user_input: str) -> str:
        """Handle nationality collection"""
        self._extract_user_info(user_input)
        
        # Debug information
        print(f"DEBUG: User input: '{user_input}'")
        print(f"DEBUG: Extracted nationality: '{self.user_profile.get('nationality')}'")
        print(f"DEBUG: User profile: {self.user_profile}")
        
        user_name = self.user_profile.get('name', 'there')
        
        if self.user_profile.get('nationality'):
            self.collected_info["nationality"] = True
            self.conversation_stage = "goal_collection"
            age = int(self.user_profile.get('age', 0))
            
            if age < 20:
                # 对于20岁以下的用户，直接询问学习目标
                return f"""**Flatopia AI**: Wonderful, {user_name}! I see you're from {self.user_profile['nationality']}. 

Since you're {age}, let me ask - what's your main goal? Are you looking to:
- 🎓 **Study abroad** (university, college, or language courses)
- 💼 **Work opportunities** (part-time work while studying)
- 🌍 **Both** (study first, then work and migrate)

This helps me tailor my recommendations perfectly for you!"""
            else:
                # 对于20岁以上的用户，询问工作目标
                return f"""**Flatopia AI**: Great, {user_name}! I see you're from {self.user_profile['nationality']}. 

What's your main goal? Are you looking to:
- 🎓 **Study abroad** (university, college, or language courses)
- 💼 **Work migration** (find a job and potentially settle permanently)
- 🌍 **Both** (study first, then work and migrate)

This helps me tailor my recommendations to your specific needs!"""
        else:
            # 更友好的提示，接受任何国籍
            return f"**Flatopia AI**: I didn't catch your nationality, {user_name}. Could you please tell me what country you're from? (e.g., India, China, Brazil, Colombia, etc.)"
    
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
            return f"**Flatopia AI**: Excellent choice, {user_name}! Let's explore study opportunities for you. What's your current education level?"
        elif self.user_profile['goal'] == 'work':
            # 对于工作目标，如果年龄超过20岁，询问家庭情况
            if age >= 20:
                self.conversation_stage = "family_collection"
                return f"**Flatopia AI**: Great, {user_name}! Since you're interested in work migration, I'd like to know about your family situation. Are you single, married, or in a relationship? This helps me understand your priorities better."
            else:
                self.conversation_stage = "profession_collection"
                return f"**Flatopia AI**: Perfect, {user_name}! What's your profession or field of work? (e.g., IT, Engineering, Healthcare, Education, Business, etc.)"
        else:  # both
            self.conversation_stage = "education_level_collection"
            return f"**Flatopia AI**: Wonderful, {user_name}! Since you're interested in both study and work, let's start with your education background. What's your current education level?"
    
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
            return f"**Flatopia AI**: No worries, {user_name}! Let me clarify - what's your current education level? Please choose:\n\n1. 10th grade (or equivalent)\n2. 12th grade (or equivalent) \n3. Bachelor's degree\n4. Master's degree\n\nOr just tell me what level you're at!"
        else:
            self.user_profile['education_level'] = user_input
        
        self.collected_info["education_level"] = True
        self.conversation_stage = "field_collection"
        return f"**Flatopia AI**: Great, {user_name}! What field of study are you most interested in?"
    
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
        return f"**Flatopia AI**: Excellent choice, {user_name}! Do you already have English test scores (IELTS/TOEFL), or are you planning to take them?"
    
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
        return f"**Flatopia AI**: Perfect, {user_name}! Now, what's your budget range for studying abroad? This helps me recommend the most suitable options for you."
    
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
        response = self.llm(prompt)
        
        # 在推荐前添加个性化称呼
        personalized_response = f"**Flatopia AI**: Based on your preferences, {user_name}, here are my recommendations:\n\n{response}"
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
            return f"**Flatopia AI**: Thank you for sharing that, {user_name}! Now, what's your profession or field of work? (e.g., IT, Engineering, Healthcare, Education, Business, etc.) This helps me understand your job opportunities in different countries."
        else:
            return f"**Flatopia AI**: I didn't catch your family status, {user_name}. Are you single, married, or in a relationship?"
    
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
            return f"**Flatopia AI**: Perfect, {user_name}! Now, what are your main priorities when choosing a country? Please select the most important factors for you:"
        else:
            return f"**Flatopia AI**: I didn't catch your profession, {user_name}. What field do you work in? (e.g., IT, Engineering, Healthcare, Education, Business, etc.)"
    
    async def _handle_priorities_collection(self, user_input: str) -> str:
        """Handle priorities collection"""
        self.user_profile['priorities'] = user_input
        self.collected_info["priorities"] = True
        self.conversation_stage = "country_recommendations"
        
        user_name = self.user_profile.get('name', 'there')
        
        # 生成国家推荐
        user_profile = str(self.user_profile)
        priorities = user_input
        prompt = self.prompts.get_country_recommendations_prompt(user_profile, priorities)
        response = self.llm(prompt)
        
        # 在推荐前添加个性化称呼
        personalized_response = f"**Flatopia AI**: Based on your preferences, {user_name}, here are my recommendations:\n\n{response}"
        return personalized_response
    
    async def _handle_country_recommendations(self, user_input: str) -> str:
        """Handle country recommendation selection"""
        # Determine user selected country
        country = self._detect_country_choice(user_input)
        if country:
            self.conversation_stage = "country_analysis"
            user_profile = str(self.user_profile)
            prompt = self.prompts.get_detailed_analysis_prompt(country, user_profile)
            response = self.llm(prompt)
            return response
        else:
            return "**Flatopia AI**: I didn't catch which country you're interested in. Please tell me which country from the list interests you most (e.g., Canada, Australia, New Zealand, UK, or Germany)."
    
    async def _handle_profile_collection(self, user_input: str) -> str:
        """Processing档案收集阶段"""
        # 提取用户信息
        self._extract_user_info(user_input)
        
        # 生成分析提示
        user_info = f"Age: {self.user_profile.get('age', 'Not specified')}, Nationality: {self.user_profile.get('nationality', 'Not specified')}, Family: {self.user_profile.get('family', 'Not specified')}, Profession: {self.user_profile.get('profession', 'Not specified')}"
        
        prompt = self.prompts.get_analysis_prompt(user_info)
        response = self.llm(prompt)
        
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

**Flatopia AI**: 🔍 **Analysing your family profile...**

Based on your background, I've found **X excellent matches** for your family, ranked by your chances:

1. 🇨🇦 **CANADA** - [brief description of why it matches their priorities]
2. 🇦🇺 **AUSTRALIA** - [brief description of why it matches their priorities]  
3. 🇳🇿 **NEW ZEALAND** - [brief description of why it matches their priorities]
4. 🇬🇧 **UK** - [brief description of why it matches their priorities]

Which country would you like to explore first?

Be encouraging and explain why each country matches their specific priorities."""
        
        response = self.llm(prompt)
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
        
        response = self.llm(prompt)
        
        self.conversation_stage = "detailed_analysis"
        return response
    
    async def _handle_action_plan(self, user_input: str) -> str:
        """Handle action plan阶段"""
        user_profile = str(self.user_profile)
        prompt = self.prompts.get_action_plan_prompt(user_profile)
        response = self.llm(prompt)
        
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
        
        response = self.llm(prompt)
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
        response = self.llm(prompt)
        
        return response
    
    async def _handle_general_question(self, user_input: str) -> str:
        """Handle general questions"""
        context = f"User profile: {self.user_profile}\nConversation history: {self.conversation_history[-3:] if len(self.conversation_history) > 3 else self.conversation_history}"
        
        prompt = self.prompts.get_follow_up_prompt(user_input, context)
        response = self.llm(prompt)
        
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
        """Extract information from user input"""
        user_input_lower = user_input.lower()
        
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
    
    def _detect_country_choice(self, user_input: str) -> str:
        """检测用户选择的国家"""
        user_input_lower = user_input.lower()
        
        if "canada" in user_input_lower or "canadian" in user_input_lower:
            return "Canada"
        elif "australia" in user_input_lower or "australian" in user_input_lower:
            return "Australia"
        elif "new zealand" in user_input_lower or "kiwi" in user_input_lower:
            return "New Zealand"
        elif "uk" in user_input_lower or "britain" in user_input_lower or "british" in user_input_lower:
            return "UK"
        elif "germany" in user_input_lower or "german" in user_input_lower:
            return "Germany"
        elif "1" in user_input_lower or "first" in user_input_lower:
            return "Canada"
        elif "2" in user_input_lower or "second" in user_input_lower:
            return "Australia"
        elif "3" in user_input_lower or "third" in user_input_lower:
            return "New Zealand"
        elif "4" in user_input_lower or "fourth" in user_input_lower:
            return "UK"
        elif "5" in user_input_lower or "fifth" in user_input_lower:
            return "Germany"
        
        return None

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

# Global Flatopia Chat manager instance
flatopia_chat_manager = FlatopiaChatManager()
