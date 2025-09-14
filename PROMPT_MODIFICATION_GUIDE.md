# Flatopia AI Prompt Modification Guide

## 📋 Overview
This guide explains how to modify prompts in the Flatopia AI system to improve conversation flow, user experience, and response quality.

## 🗂️ Files Containing Prompts

### 1. **`prompts/platopia_prompts.py`** - Main Prompt Templates
This is the **primary file** for all prompt modifications.

**Key Methods:**
- `get_system_prompt()` - Main AI personality and behavior rules
- `get_greeting_prompt()` - Initial greeting message
- `get_nationality_prompt()` - Nationality collection
- `get_profession_prompt()` - Profession collection
- `get_priorities_prompt()` - Priority collection
- `get_country_recommendations_prompt()` - TOP 5 country recommendations
- `get_detailed_analysis_prompt()` - Detailed country analysis
- `get_action_plan_prompt()` - Step-by-step action plans
- `get_follow_up_prompt()` - General question handling

### 2. **`core/platopia_chat_manager.py`** - Conversation Flow Logic
Controls when and how prompts are used.

**Key Methods:**
- `_handle_age_collection()` - Age collection logic
- `_handle_nationality_collection()` - Nationality collection logic
- `_handle_family_collection()` - Family information collection
- `_handle_profession_collection()` - Profession collection
- `_handle_priorities_collection()` - Priority collection
- `_handle_country_recommendations()` - Country recommendation handling
- `_handle_country_analysis()` - Detailed country analysis

### 3. **`llm_config.py`** - System Configuration
Contains system-level prompts and configuration.

**Key Variables:**
- `SYSTEM_PROMPT` - Global system behavior
- `APP_NAME` - Application name
- `MODEL_NAME` - AI model selection

## 🎯 Current Prompt Structure

### Step-by-Step Conversation Flow:
1. **Greeting** → Ask for age
2. **Age Collection** → Ask for nationality
3. **Nationality Collection** → Ask for family status
4. **Family Collection** → Ask for profession
5. **Profession Collection** → Ask for priorities
6. **Priority Collection** → Show TOP 5 country recommendations
7. **Country Selection** → Provide detailed analysis
8. **Follow-up** → Handle additional questions

## 🔧 How to Modify Prompts

### 1. **Modify Conversation Flow**

**File:** `prompts/platopia_prompts.py`

**Example - Add a new question step:**
```python
@staticmethod
def get_education_prompt() -> str:
    """Get education level prompt"""
    return """**Flatopia AI**: Great! What's your highest level of education?
    
- High School
- Bachelor's Degree
- Master's Degree
- PhD/Doctorate
- Professional Certification

Please let me know your education level."""
```

**Then add to chat manager:**
```python
async def _handle_education_collection(self, user_input: str) -> str:
    """Handle education collection"""
    self._extract_user_info(user_input)
    self.collected_info["education"] = True
    self.conversation_stage = "next_step"
    return self.prompts.get_next_prompt()
```

### 2. **Modify Country Recommendations**

**File:** `prompts/platopia_prompts.py`

**Current format:**
```python
def get_country_recommendations_prompt(user_profile: str, priorities: str) -> str:
    return f"""Provide TOP 5 country recommendations following this EXACT format:

**Flatopia AI**: 🔍 **Perfect! I've analyzed your profile and found 5 excellent matches for your family:**

1. 🇨🇦 **CANADA** - [Brief reason why it matches their priorities - 1-2 sentences]
2. 🇦🇺 **AUSTRALIA** - [Brief reason why it matches their priorities - 1-2 sentences]
3. 🇳🇿 **NEW ZEALAND** - [Brief reason why it matches their priorities - 1-2 sentences]
4. 🇬🇧 **UK** - [Brief reason why it matches their priorities - 1-2 sentences]
5. 🇩🇪 **GERMANY** - [Brief reason why it matches their priorities - 1-2 sentences]

**Which country interests you most?** I'll provide a detailed analysis for your chosen destination! 🎯"""
```

**To modify:**
- Change the number of recommendations (TOP 3, TOP 7, etc.)
- Add/remove countries
- Modify the format
- Change the emojis or styling

### 3. **Modify AI Personality**

**File:** `prompts/platopia_prompts.py`

**Current personality rules:**
```python
def get_system_prompt() -> str:
    return """Your personality and style:
- Warm, professional, and encouraging
- Use emojis strategically to make conversations engaging
- Ask ONE question at a time to avoid overwhelming users
- Provide detailed, actionable advice
- Always consider family needs and priorities
- Be realistic about timelines and costs
- Offer TOP 5 country recommendations with clear reasons
- Guide users step-by-step through the process"""
```

**To modify:**
- Change tone (formal, casual, friendly, etc.)
- Modify emoji usage
- Adjust response length
- Change conversation style

### 4. **Modify Response Format**

**File:** `prompts/platopia_prompts.py`

**Example - Change detailed analysis format:**
```python
def get_detailed_analysis_prompt(country: str, user_profile: str) -> str:
    return f"""Provide a detailed analysis for {country} using this format:

**{country.upper()} - YOUR PERFECT DESTINATION** 🇨🇦

**Why {country} is ideal for you:**
✅ **Safety**: [safety information]
✅ **Democracy**: [political stability]
✅ **Education**: [education system]
✅ **Healthcare**: [healthcare system]
✅ **Job opportunities**: [employment prospects]

**Immigration pathway - [Program Name]:**
- [Specific requirements and process]
- [Timeline estimates]
- [Cost breakdown]

**Next steps:**
1. [Specific action items]
2. [Document requirements]
3. [Timeline recommendations]

Be encouraging, detailed, and professional."""
```

## 🎨 Prompt Design Best Practices

### 1. **One Question at a Time**
```python
# ❌ Bad - Multiple questions
return "What's your age, nationality, and profession?"

# ✅ Good - Single question
return "What's your age?"
```

### 2. **Clear Formatting**
```python
# ✅ Good - Clear structure
return """**Flatopia AI**: 🔍 **Perfect! I've analyzed your profile:**

1. 🇨🇦 **CANADA** - [Reason]
2. 🇦🇺 **AUSTRALIA** - [Reason]

**Which country interests you most?**"""
```

### 3. **Consistent Tone**
```python
# ✅ Good - Consistent warm tone
return """**Flatopia AI**: Great! Thank you for sharing your age. 

What is your nationality?"""
```

### 4. **Use Emojis Strategically**
```python
# ✅ Good - Meaningful emojis
return """**Flatopia AI**: 👋 Hello! I'm your AI immigration advisor.

🔍 **Perfect! I've analyzed your profile:**

1. 🇨🇦 **CANADA** - [Reason]
2. 🇦🇺 **AUSTRALIA** - [Reason]

**Which country interests you most?** 🎯"""
```

## 🚀 Testing Your Changes

### 1. **Restart the Application**
```bash
# Stop current app
pkill -f "streamlit run platopia_app.py"

# Start with new prompts
export GROQ_API_KEY="your_key" && streamlit run platopia_app.py --server.port 8502
```

### 2. **Test Conversation Flow**
1. Start a new conversation
2. Follow the step-by-step process
3. Check if prompts appear correctly
4. Verify country recommendations format
5. Test detailed analysis

### 3. **Debug Common Issues**
- **Prompts not updating**: Restart the application
- **Wrong conversation flow**: Check `collected_info` logic
- **Format issues**: Verify prompt templates
- **Missing responses**: Check error handling

## 📝 Common Modifications

### 1. **Add New Countries**
```python
# In get_country_recommendations_prompt()
6. 🇳🇱 **NETHERLANDS** - [Brief reason why it matches their priorities - 1-2 sentences]
7. 🇸🇬 **SINGAPORE** - [Brief reason why it matches their priorities - 1-2 sentences]
```

### 2. **Change Recommendation Count**
```python
# Change from TOP 5 to TOP 3
return f"""Provide TOP 3 country recommendations following this EXACT format:

**Flatopia AI**: 🔍 **Perfect! I've analyzed your profile and found 3 excellent matches for your family:**

1. 🇨🇦 **CANADA** - [Reason]
2. 🇦🇺 **AUSTRALIA** - [Reason]
3. 🇳🇿 **NEW ZEALAND** - [Reason]
```

### 3. **Modify Question Order**
```python
# In chat manager, change the order
elif not self.collected_info["profession"]:
    response = await self._handle_profession_collection(user_input)
elif not self.collected_info["family"]:
    response = await self._handle_family_collection(user_input)
```

### 4. **Add New Information Collection**
```python
# Add to collected_info
self.collected_info = {
    "age": False,
    "nationality": False,
    "family": False,
    "profession": False,
    "priorities": False,
    "education": False,  # New field
    "budget": False      # New field
}
```

## 🔍 Troubleshooting

### 1. **Prompts Not Working**
- Check file syntax
- Restart application
- Verify method names match

### 2. **Conversation Flow Issues**
- Check `collected_info` logic
- Verify conversation stages
- Test step-by-step

### 3. **Format Problems**
- Check markdown formatting
- Verify emoji usage
- Test in browser

## 📚 Additional Resources

- **Streamlit Documentation**: https://docs.streamlit.io/
- **LangChain Documentation**: https://python.langchain.com/
- **Prompt Engineering Guide**: https://www.promptingguide.ai/

---

**Remember**: Always test your changes thoroughly and maintain the step-by-step conversation flow for the best user experience! 🚀
