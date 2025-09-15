"""
SMS Chat Manager for Flatopia
Handles SMS-style conversations with 160 character limit
"""
import re
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from .sms_database import sms_db
from .multi_api_llm import MultiAPILLM
from .faiss_knowledge_base import get_faiss_kb
from .smart_search import smart_search
from .knowledge_updater import knowledge_updater

logger = logging.getLogger(__name__)

class SMSChatManager:
    """SMS Chat Manager for Flatopia"""
    
    def __init__(self):
        self.llm = MultiAPILLM()
        self.knowledge_base = None
        self.smart_search = smart_search
        self.knowledge_updater = knowledge_updater
        
        # SMS conversation stages
        self.stages = {
            'greeting': self._handle_greeting,
            'age_collection': self._handle_age_collection,
            'underage_decision': self._handle_underage_decision,
            'goal_collection': self._handle_goal_collection,
            'passport_collection': self._handle_passport_collection,
            'education_collection': self._handle_education_collection,
            'field_collection': self._handle_field_collection,
            'english_test_collection': self._handle_english_test_collection,
            'priorities_collection': self._handle_priorities_collection,
            'budget_collection': self._handle_budget_collection,
            'recommendations': self._handle_recommendations,
            'country_details': self._handle_country_details,
            'university_list': self._handle_university_list
        }

    def _is_question_or_informational(self, message: str) -> bool:
        """Heuristic: decide if message should be handled by RAG Q&A."""
        if not message:
            return False
        text = (message or "").strip().lower()
        if not text:
            return False
        if text.isdigit():
            return False
        # Keywords and signals indicating a question or info need
        keywords = [
            'visa', 'pr', 'permanent', 'residence', 'immigration', 'ielts', 'toefl',
            'how', 'what', 'which', 'when', 'where', 'can i', 'could i', 'requirements',
            'pathway', 'work', 'study', 'university', 'scholarship', 'tuition', 'cost', '?'
        ]
        if any(k in text for k in keywords):
            return True
        # Long free text likely needs understanding
        return len(text) >= 20

    def _format_context_snippets(self, items, max_chars: int = 600) -> str:
        """Build compact context from KB results within char budget."""
        parts = []
        used = 0
        for it in items or []:
            snippet = it.get('text') if isinstance(it, dict) else str(it)
            if not snippet:
                continue
            snippet = snippet.strip().replace('\n', ' ')
            if len(snippet) > 200:
                snippet = snippet[:197] + '...'
            if used + len(snippet) + 3 > max_chars:
                break
            parts.append(f"- {snippet}")
            used += len(snippet) + 3
        return "\n".join(parts)

    def _rag_answer(self, message: str, session: Dict[str, Any]) -> Optional[str]:
        """Retrieve with FAISS and compose a concise LLM answer (<=160 chars)."""
        try:
            kb = self._get_knowledge_base()
            uni_results = []
            visa_results = []
            if kb and kb.is_available():
                try:
                    visa_results = kb.search_visas(message, top_k=3) or []
                except Exception:
                    visa_results = []
                try:
                    uni_results = kb.search_universities(message, top_k=3) or []
                except Exception:
                    uni_results = []

            context = self._format_context_snippets((visa_results or []) + (uni_results or []))

            prompt = (
                "You are Flatopia's SMS immigration assistant.\n"
                "Task: Answer the user's message using the provided context.\n"
                "Rules:\n"
                "- Max 160 characters.\n"
                "- Be clear and helpful.\n"
                "- If context is insufficient, give best guidance and suggest next step.\n"
                "Context:\n" + (context or "(no context)") + "\n"
                "User: " + (message or "").strip() + "\n"
                "Answer (<=160 chars):"
            )
            raw = self.llm(prompt)
            reply = (raw or "").strip()
            # Enforce 160-char limit just in case
            return self._truncate_message(reply)
        except Exception:
            return None
    
    def _get_knowledge_base(self):
        """Lazy load knowledge base"""
        if self.knowledge_base is None:
            self.knowledge_base = get_faiss_kb()
        return self.knowledge_base
    
    def _truncate_message(self, message: str, max_length: int = 160) -> str:
        """Truncate message to fit SMS limit"""
        if not message:
            return ""
        if len(message) <= max_length:
            return message
        
        # Try to truncate at word boundary
        truncated = message[:max_length-3]
        last_space = truncated.rfind(' ')
        if last_space > max_length * 0.8:  # If we can truncate at a reasonable point
            return truncated[:last_space] + "..."
        else:
            return truncated + "..."
    
    def _extract_phone_number(self, from_number: str) -> str:
        """Extract and normalize phone number"""
        # Remove all non-digit characters
        phone = re.sub(r'\D', '', from_number)
        
        # Handle different phone number formats
        if phone.startswith('61') and len(phone) == 12:
            # Australian number: +61477619672 -> 61477619672
            return phone
        elif phone.startswith('0') and len(phone) == 10:
            # Australian local number: 0477619672 -> 61477619672
            return '61' + phone[1:]
        elif len(phone) == 10:
            # Assume US/Canada number: 1234567890 -> 11234567890
            return '1' + phone
        else:
            # Return as is for other formats
            return phone
    
    def _extract_user_info(self, message: str) -> Dict[str, Any]:
        """Extract information from user message"""
        info = {}
        message_lower = message.lower().strip()
        
        # Extract age (digits first)
        age_match = re.search(r'\b(\d{1,2})\b', message)
        if age_match:
            info['age'] = int(age_match.group(1))
        else:
            # Try parse basic English number words up to 99 (e.g., "twenty four")
            words = {
                'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
                'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
                'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
                'nineteen': 19
            }
            tens = {
                'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
                'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
            }
            # Normalize hyphens to spaces
            norm = re.sub(r'[-]+', ' ', message_lower)
            tokens = re.findall(r'[a-z]+', norm)
            # Try sliding window of 1-2 tokens to form 0-99
            candidate_age: Optional[int] = None
            for i in range(len(tokens)):
                # single word
                w1 = tokens[i]
                if w1 in words:
                    val = words[w1]
                    if 10 <= val <= 80:
                        candidate_age = val
                        break
                if w1 in tens:
                    val = tens[w1]
                    if 10 <= val <= 80:
                        candidate_age = val
                        # maybe "twenty four"
                        if i + 1 < len(tokens):
                            w2 = tokens[i+1]
                            if w2 in words and 0 < words[w2] < 10:
                                val2 = val + words[w2]
                                if 10 <= val2 <= 80:
                                    candidate_age = val2
                        break
                # two-word combination
                if i + 1 < len(tokens):
                    w2 = tokens[i+1]
                    if w1 in tens and w2 in words:
                        val = tens[w1] + words[w2]
                        if 10 <= val <= 80:
                            candidate_age = val
                            break
            if candidate_age is not None:
                info['age'] = candidate_age
        
        # Extract nationality/passport
        nationalities = {
            'indian': 'Indian', 'india': 'Indian',
            'chinese': 'Chinese', 'china': 'Chinese',
            'australian': 'Australian', 'australia': 'Australian',
            'canadian': 'Canadian', 'canada': 'Canadian',
            'american': 'American', 'usa': 'American', 'us': 'American',
            'british': 'British', 'uk': 'British', 'england': 'British'
        }
        
        for key, value in nationalities.items():
            if key in message_lower:
                info['nationality'] = value
                break
        
        # Extract education level (from numbers)
        if message.isdigit():
            info['education_choice'] = int(message)
        
        # Extract field choice
        fields = {
            '1': 'Engineering/Tech',
            '2': 'Business',
            '3': 'Medicine',
            '4': 'Arts/Humanities',
            '5': 'Other'
        }
        if message in fields:
            info['field_choice'] = fields[message]
        
        # Extract English test status
        if 'planning' in message_lower or 'plan' in message_lower:
            info['english_test'] = 'planning'
        elif 'yes' in message_lower:
            info['english_test'] = 'yes'
        elif 'no' in message_lower:
            info['english_test'] = 'no'
        
        # Extract priorities choice
        priorities = {
            '1': 'Low tuition fees',
            '2': 'Work opportunities during study',
            '3': 'Easy path to permanent residence',
            '4': 'All of the above'
        }
        if message in priorities:
            info['priorities_choice'] = priorities[message]
        
        # Extract budget choice
        budget_options = {
            '1': 'Under 10 lakhs',
            '2': '10-20 lakhs',
            '3': '20+ lakhs'
        }
        if message in budget_options:
            info['budget_choice'] = budget_options[message]
        
        # Extract country code
        country_codes = {
            'ca': 'Canada', 'canada': 'Canada',
            'au': 'Australia', 'australia': 'Australia',
            'nz': 'New Zealand', 'new zealand': 'New Zealand',
            'us': 'USA', 'usa': 'USA',
            'uk': 'UK', 'united kingdom': 'UK'
        }
        if message_lower in country_codes:
            info['country_code'] = country_codes[message_lower]
        
        return info

    def _extract_info_with_llm(self, message: str) -> Dict[str, Any]:
        """Use LLM to extract structured info from free text (JSON-only)."""
        try:
            prompt = (
                "You are an information extraction assistant for an SMS immigration advisor.\n"
                "Extract user info from the message. Return ONLY a compact JSON object with keys: "
                "age (integer or null), nationality, goal, education_level, field_of_interest, english_test, budget, country_interest, priorities. "
                "If a field is unknown, use null.\n"
                "Examples:\n"
                "Input: 'hi, I am 24, indian' -> {\"age\":24,\"nationality\":\"Indian\",\"goal\":null,\"education_level\":null,\"field_of_interest\":null,\"english_test\":null,\"budget\":null,\"country_interest\":null,\"priorities\":null}\n"
                "Input: '18岁 中国人 想去澳大利亚读书' -> {\"age\":18,\"nationality\":\"Chinese\",\"goal\":\"study\",\"education_level\":null,\"field_of_interest\":null,\"english_test\":null,\"budget\":null,\"country_interest\":\"Australia\",\"priorities\":null}\n"
                "Message: " + message.strip() + "\nReturn ONLY the JSON object."
            )
            raw = self.llm(prompt)
            import json as _json
            data = {}
            try:
                data = _json.loads(raw.strip())
            except Exception:
                s = raw.find('{'); e = raw.rfind('}')
                if s != -1 and e != -1 and e > s:
                    data = _json.loads(raw[s:e+1])
            if isinstance(data, dict):
                return { (k or '').strip().lower(): v for k, v in data.items() }
            return {}
        except Exception:
            return {}
    
    async def process_sms(self, from_number: str, message: str) -> str:
        """Process incoming SMS and return response"""
        try:
            message = message or ""
            phone_number = self._extract_phone_number(from_number)
            
            # Get or create user session
            session = sms_db.get_user_session(phone_number)
            if not session:
                session = sms_db.create_user_session(phone_number)
            
            # Add user message to history
            sms_db.add_conversation_message(phone_number, 'user', message)
            
            # Get current stage
            current_stage = session.get('current_stage', 'greeting')

            # Support 'hi' to reset overall flow state and send opening message
            normalized = (message or "").strip().lower()
            if normalized in ["hi", "hello", "hey"]:
                reset_updates = {
                    'name': None,
                    'age': None,
                    'nationality': None,
                    'education_level': None,
                    'field_of_interest': None,
                    'english_test_status': None,
                    'budget_range': None,
                    'priorities': None,
                    'country_interest': None,
                    'current_stage': 'greeting'
                }
                sms_db.update_user_session(phone_number, reset_updates)
                current_stage = 'greeting'
            
            # If message looks like a general question/info (not pure digits), try RAG QA first
            if (message or "").strip() and not (message or "").strip().isdigit():
                if self._is_question_or_informational(message):
                    rag = self._rag_answer(message, session)
                    if rag:
                        # Do not change stage; respond immediately
                        response = rag
                        response = self._truncate_message(response)
                        sms_db.add_conversation_message(phone_number, 'bot', response)
                        return response

            # Process message based on stage
            if current_stage in self.stages:
                response = await self.stages[current_stage](phone_number, message, session)
            else:
                response = "Sorry, I didn't understand. Text HELP for assistance."
            
            # Truncate response to SMS limit
            response = self._truncate_message(response)
            
            # Add bot response to history
            sms_db.add_conversation_message(phone_number, 'bot', response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing SMS: {e}")
            return "Sorry, there was an error. Please try again."
    
    async def _handle_greeting(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle greeting stage"""
        # Update stage to age collection
        sms_db.update_user_session(phone_number, {'current_stage': 'age_collection'})
        return "Welcome to Flatopia! I'm your AI visa assistant. I'll help you find study abroad opportunities with pathways to permanent residence. What's your age?"
    
    async def _handle_age_collection(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle age collection"""
        info = self._extract_user_info(message)
        
        if 'age' in info:
            age_val = info['age']
            if age_val is not None and 10 <= age_val <= 80:
                next_stage = 'underage_decision' if age_val < 18 else 'goal_collection'
                sms_db.update_user_session(phone_number, {'age': age_val, 'current_stage': next_stage})
                if next_stage == 'underage_decision':
                    return "You're under 18. Are you considering studying abroad soon or staying domestically for now?\n1) Study abroad\n2) Stay domestically"
                else:
                    return "What's your main goal?\n1) Study\n2) Work\n3) Study + Work"
        else:
            # Fallback: parse first 1-2 digit number as age if reasonable
            import re
            m = re.search(r"\b(\d{1,2})\b", message or "")
            if m:
                try:
                    age_val = int(m.group(1))
                    if 10 <= age_val <= 80:
                        next_stage = 'underage_decision' if age_val < 18 else 'goal_collection'
                        sms_db.update_user_session(phone_number, {'age': age_val, 'current_stage': next_stage})
                        if next_stage == 'underage_decision':
                            return "You're under 18. Are you considering studying abroad soon or staying domestically for now?\n1) Study abroad\n2) Stay domestically"
                        else:
                            return "What's your main goal?\n1) Study\n2) Work\n3) Study + Work"
                except Exception:
                    pass
            # LLM fallback
            llm_info = self._extract_info_with_llm(message)
            try:
                age_candidate = llm_info.get('age') if isinstance(llm_info, dict) else None
                if isinstance(age_candidate, str) and age_candidate.isdigit():
                    age_candidate = int(age_candidate)
                if isinstance(age_candidate, int) and 10 <= age_candidate <= 80:
                    next_stage = 'underage_decision' if age_candidate < 18 else 'goal_collection'
                    sms_db.update_user_session(phone_number, {'age': age_candidate, 'current_stage': next_stage})
                    if next_stage == 'underage_decision':
                        return "You're under 18. Are you considering studying abroad soon or staying domestically for now?\n1) Study abroad\n2) Stay domestically"
                    else:
                        return "What's your main goal?\n1) Study\n2) Work\n3) Study + Work"
            except Exception:
                pass
            return "Please tell me your age (just the number)."

    async def _handle_underage_decision(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle decision for users under 18"""
        choice = (message or "").strip().lower()
        if choice in ['1', 'study', 'study abroad']:
            sms_db.update_user_session(phone_number, {'goal': 'study', 'current_stage': 'passport_collection'})
            return "Great! Which passport do you hold?"
        if choice in ['2', 'stay', 'stay domestically']:
            sms_db.update_user_session(phone_number, {'goal': 'stay', 'current_stage': 'passport_collection'})
            return "Understood. Which passport do you hold?"
        return "Please choose:\n1) Study abroad\n2) Stay domestically"

    async def _handle_goal_collection(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle main goal for users 18+"""
        choice = (message or "").strip().lower()
        mapping = {
            '1': 'study', 'study': 'study',
            '2': 'work', 'work': 'work',
            '3': 'study+work', 'study + work': 'study+work'
        }
        goal = mapping.get(choice)
        if goal:
            sms_db.update_user_session(phone_number, {'goal': goal, 'current_stage': 'passport_collection'})
            return "Thanks! Which passport do you hold?"
        return "What's your main goal?\n1) Study\n2) Work\n3) Study + Work"
    
    async def _handle_passport_collection(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle passport/nationality collection"""
        info = self._extract_user_info(message)
        
        if 'nationality' in info:
            sms_db.update_user_session(phone_number, {'nationality': info['nationality'], 'current_stage': 'education_collection'})
            return "Perfect. What's your current education level?\n1) Completing 10th grade\n2) Completing 12th grade\n3) Other"
        else:
            return "Please tell me which passport you hold (e.g., Indian, Chinese, etc.)."
    
    async def _handle_education_collection(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle education level collection"""
        info = self._extract_user_info(message)
        
        if 'education_choice' in info:
            education_levels = {1: '10th grade', 2: '12th grade', 3: 'Other'}
            level = education_levels.get(info['education_choice'], 'Other')
            sms_db.update_user_session(phone_number, {'education_level': level, 'current_stage': 'field_collection'})
            return "Excellent! What field interests you for university?\n1) Engineering/Tech\n2) Business\n3) Medicine\n4) Arts/Humanities\n5) Other"
        else:
            return "Please choose your education level:\n1) Completing 10th grade\n2) Completing 12th grade\n3) Other"
    
    async def _handle_field_collection(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle field of interest collection"""
        info = self._extract_user_info(message)
        
        if 'field_choice' in info:
            sms_db.update_user_session(phone_number, {'field_of_interest': info['field_choice'], 'current_stage': 'english_test_collection'})
            return "Smart choice! Do you have any English test scores (IELTS/TOEFL) or plan to take them?"
        else:
            return "Please choose your field:\n1) Engineering/Tech\n2) Business\n3) Medicine\n4) Arts/Humanities\n5) Other"
    
    async def _handle_english_test_collection(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle English test status collection"""
        info = self._extract_user_info(message)
        
        if 'english_test' in info:
            sms_db.update_user_session(phone_number, {'english_test_status': info['english_test'], 'current_stage': 'priorities_collection'})
            return "What's most important for your destination country?\n1) Low tuition fees\n2) Work opportunities during study\n3) Easy path to permanent residence\n4) All of the above"
        else:
            return "Please tell me about your English test status: 'yes', 'no', or 'planning'"
    
    async def _handle_priorities_collection(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle priorities collection"""
        info = self._extract_user_info(message)
        
        if 'priorities_choice' in info:
            sms_db.update_user_session(phone_number, {'priorities': info['priorities_choice'], 'current_stage': 'budget_collection'})
            return "I understand! How much can your family invest in education annually (in rupees)?\n1) Under 10 lakhs\n2) 10-20 lakhs\n3) 20+ lakhs"
        else:
            return "Please choose your priority:\n1) Low tuition fees\n2) Work opportunities during study\n3) Easy path to permanent residence\n4) All of the above"
    
    async def _handle_budget_collection(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle budget collection"""
        info = self._extract_user_info(message)
        
        if 'budget_choice' in info:
            sms_db.update_user_session(phone_number, {'budget_range': info['budget_choice'], 'current_stage': 'recommendations'})
            return "Analyzing your profile... 📊"
        else:
            return "Please choose your budget:\n1) Under 10 lakhs\n2) 10-20 lakhs\n3) 20+ lakhs"
    
    async def _handle_recommendations(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle recommendations stage"""
        # Generate recommendations based on user profile
        recommendations = self._generate_recommendations(session)
        
        # Update stage to country_details
        sms_db.update_user_session(phone_number, {'current_stage': 'country_details'})
        
        return recommendations
    
    async def _handle_country_details(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle country details request"""
        info = self._extract_user_info(message)
        
        if 'country_code' in info:
            country = info['country_code']
            details = self._get_country_details(country, session)
            
            # Update stage to university_list
            sms_db.update_user_session(phone_number, {'current_stage': 'university_list'})
            
            return details
        else:
            return "Want details on any country? Reply CA, AU, NZ, US, or UK"
    
    async def _handle_university_list(self, phone_number: str, message: str, session: Dict[str, Any]) -> str:
        """Handle university list request"""
        if message.lower() in ['yes', 'y', '1']:
            universities = self._get_university_recommendations(session)
            return universities
        else:
            return "Thanks! Start IELTS prep now, maintain good grades, and text me with questions. Your engineering dreams are achievable! 🚀"
    
    def _generate_recommendations(self, session: Dict[str, Any]) -> str:
        """Generate country recommendations based on user profile"""
        # This is a simplified version - in production, you'd use the knowledge base
        return "Great news! I found 5 strong matches:\n🇨🇦 CANADA: Engineering programs with co-op, post-grad work permits lead to PR\n🇦🇺 AUSTRALIA: Skills shortage in engineering, clear PR pathway\n🇳🇿 NEW ZEALAND: Affordable tuition, post-study work visas\n🇺🇸 USA: STEM programs offer extended work opportunities\n🇬🇧 UK: World-class engineering, graduate visa route\n\nWant details on any country? Reply CA, AU, NZ, US, or UK"
    
    def _get_country_details(self, country: str, session: Dict[str, Any]) -> str:
        """Get detailed country information"""
        country_details = {
            'Australia': "🇦🇺 AUSTRALIA DETAILS:\n• Student visa allows 48hrs/fortnight work\n• 2-4 year post-study work visa after engineering degree\n• Skilled migration pathway favors engineers under 25\n• Tuition: 35-45k AUD/year\n• Scholarships + lower living costs in regional areas\n\nNext steps:\n1) Take IELTS (target 6.5+)\n2) Research universities\n3) Apply for Feb/July 2026 intake\n\nWant university recommendations? Reply YES",
            'Canada': "🇨🇦 CANADA DETAILS:\n• Co-op programs provide work experience\n• Post-graduation work permit up to 3 years\n• Express Entry system for PR\n• Tuition: 15-35k CAD/year\n• Strong job market for engineers\n\nNext steps:\n1) Take IELTS (target 6.5+)\n2) Research universities\n3) Apply for Fall 2026 intake\n\nWant university recommendations? Reply YES"
        }
        
        return country_details.get(country, "Country details not available. Please try CA, AU, NZ, US, or UK")
    
    def _get_university_recommendations(self, session: Dict[str, Any]) -> str:
        """Get university recommendations"""
        return "TOP 5 AFFORDABLE AUSTRALIAN UNIVERSITIES FOR ENGINEERING:\n1) University of Tasmania - 32k AUD/year + scholarships\n2) Federation University - 31k AUD/year\n3) Charles Darwin University - 33k AUD/year\n4) University of Southern Queensland - 34k AUD/year\n5) CQUniversity - 30k AUD/year\n\nAll are regional unis with migration benefits + industry connections.\n\nI'll text you application deadlines in Oct 2025. Save this number and text HELP anytime!"

# Global SMS chat manager instance
sms_chat_manager = SMSChatManager()