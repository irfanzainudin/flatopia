# Flatopia SMS System

A comprehensive SMS-based conversation system for immigration and study abroad consultation with 160-character message limits and database integration.

## 🚀 Features

- **SMS Conversation Flow**: Structured conversation with 160-character limit
- **User Profile Management**: SQLite database for user data storage
- **Knowledge Base Integration**: FAISS vector database synchronization
- **Multi-API LLM Support**: Groq and OpenAI with automatic failover
- **REST API**: FastAPI endpoints for SMS processing
- **Data Retention**: 12-month data retention policy
- **Character Limit Enforcement**: All responses under 160 characters

## 📱 SMS Conversation Flow

### Stage 1: Greeting
```
Welcome to Flatopia! I'm your AI visa assistant. I'll help you find study abroad opportunities with pathways to permanent residence. What's your age?
```

### Stage 2: Passport/Nationality
```
Great! As a student, you have many options. Which passport do you hold?
```

### Stage 3: Education Level
```
Perfect. What's your current education level?
1) Completing 10th grade
2) Completing 12th grade
3) Other
```

### Stage 4: Field of Interest
```
Excellent! What field interests you for university?
1) Engineering/Tech
2) Business
3) Medicine
4) Arts/Humanities
5) Other
```

### Stage 5: English Test
```
Smart choice! Do you have any English test scores (IELTS/TOEFL) or plan to take them?
```

### Stage 6: Priorities
```
What's most important for your destination country?
1) Low tuition fees
2) Work opportunities during study
3) Easy path to permanent residence
4) All of the above
```

### Stage 7: Budget
```
I understand! How much can your family invest in education annually (in rupees)?
1) Under 10 lakhs
2) 10-20 lakhs
3) 20+ lakhs
```

### Stage 8: Recommendations
```
Great news! I found 5 strong matches:
🇨🇦 CANADA: Engineering programs with co-op, post-grad work permits lead to PR
🇦🇺 AUSTRALIA: Skills shortage in engineering, clear PR pathway
🇳🇿 NEW ZEALAND: Affordable tuition, post-study work visas
🇺🇸 USA: STEM programs offer extended work opportunities
🇬🇧 UK: World-class engineering, graduate visa route

Want details on any country? Reply CA, AU, NZ, US, or UK
```

### Stage 9: Country Details
```
🇦🇺 AUSTRALIA DETAILS:
• Student visa allows 48hrs/fortnight work
• 2-4 year post-study work visa after engineering degree
• Skilled migration pathway favors engineers under 25
• Tuition: 35-45k AUD/year
• Scholarships + lower living costs in regional areas

Next steps:
1) Take IELTS (target 6.5+)
2) Research universities
3) Apply for Feb/July 2026 intake

Want university recommendations? Reply YES
```

### Stage 10: University List
```
TOP 5 AFFORDABLE AUSTRALIAN UNIVERSITIES FOR ENGINEERING:
1) University of Tasmania - 32k AUD/year + scholarships
2) Federation University - 31k AUD/year
3) Charles Darwin University - 33k AUD/year
4) University of Southern Queensland - 34k AUD/year
5) CQUniversity - 30k AUD/year

All are regional unis with migration benefits + industry connections.
```

## 🗄️ Database Schema

### Users Table
- `phone_number` (PRIMARY KEY)
- `name`
- `created_at`
- `last_active`
- `status`

### User Profiles Table
- `phone_number` (PRIMARY KEY)
- `age`
- `nationality`
- `education_level`
- `field_of_interest`
- `english_test_status`
- `budget_range`
- `priorities`
- `country_interest`
- `updated_at`

### Conversation Sessions Table
- `session_id` (PRIMARY KEY)
- `phone_number`
- `session_start`
- `current_stage`
- `status`

### User Choices Table
- `choice_id` (PRIMARY KEY)
- `phone_number`
- `session_id`
- `stage`
- `choice_value`
- `timestamp`

### Recommendations Table
- `recommendation_id` (PRIMARY KEY)
- `phone_number`
- `session_id`
- `country_code`
- `university_name`
- `created_at`

## 🔧 Installation

1. **Install Dependencies**
```bash
pip install fastapi uvicorn sqlite3
```

2. **Set Environment Variables**
```bash
export GROQ_API_KEY="your-groq-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

3. **Initialize Database**
```python
from core.sms_database import sms_db
sms_db.init_database()
```

## 🚀 Usage

### 1. Start SMS API Server
```bash
python sms_api.py
```

### 2. Test SMS System
```bash
python test_sms_system.py
```

### 3. API Endpoints

#### Process SMS Message
```bash
POST /sms/process
{
    "phone_number": "+1234567890",
    "message": "16"
}
```

#### Get User Profile
```bash
GET /sms/profile/+1234567890
```

#### Get Conversation Stats
```bash
GET /sms/stats
```

#### Health Check
```bash
GET /sms/health
```

## 📊 API Response Format

### SMS Response
```json
{
    "phone_number": "+1234567890",
    "response": "Great! As a student, you have many options. Which passport do you hold?",
    "session_id": "sms_1234567890",
    "message_length": 85,
    "success": true
}
```

### User Profile Response
```json
{
    "phone_number": "+1234567890",
    "profile": {
        "age": "16",
        "nationality": "Indian",
        "education_level": "12th grade",
        "field_of_interest": "Engineering/Tech"
    },
    "choices_history": [
        {
            "stage": "greeting",
            "choice_value": "16",
            "timestamp": "2024-01-01 12:00:00"
        }
    ]
}
```

## 🔄 Knowledge Base Integration

The SMS system automatically syncs user data with the FAISS knowledge base:

1. **User Profile Sync**: User characteristics are stored as vectors
2. **Conversation Insights**: Choice patterns are analyzed and stored
3. **Personalized Recommendations**: Based on user profile and knowledge base
4. **Feedback Integration**: User feedback updates the knowledge base

## 📱 SMS Message Handling

### Special Commands
- `HELP` or `H`: Show help message
- `YES` or `Y`: Confirm action
- `CA`, `AU`, `NZ`, `US`, `UK`: Country selection

### Character Limits
- All responses are limited to 160 characters
- Long responses are truncated with "..."
- Messages are optimized for SMS delivery

### Input Validation
- Age: 16-50 years
- Options: 1-5 for multiple choice
- Country codes: CA, AU, NZ, US, UK
- Text responses: Processed by LLM

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python test_sms_system.py
```

Tests include:
- Complete conversation flow
- Help functionality
- Invalid input handling
- Character limit enforcement
- Database operations

## 📈 Monitoring

### Logs
- All SMS processing is logged
- Error tracking and debugging
- Performance monitoring

### Statistics
- Total users
- Active sessions
- Total choices recorded
- Response times

## 🔒 Security

- Phone numbers are used as unique identifiers
- No sensitive data stored in plain text
- 12-month data retention policy
- Automatic cleanup of old data

## 🚀 Deployment

### Production Setup
1. Use PostgreSQL instead of SQLite
2. Set up Redis for session management
3. Configure proper logging
4. Set up monitoring and alerts
5. Implement rate limiting

### Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port
GROQ_API_KEY=your-key
OPENAI_API_KEY=your-key
```

## 📞 Support

For technical support or questions:
- Check the API documentation at `/docs`
- Review logs for error details
- Test with the provided test suite
- Monitor conversation statistics

## 🔄 Updates

The system supports:
- Dynamic conversation flow
- Real-time knowledge base updates
- User profile evolution
- A/B testing of responses
- Analytics and insights

---

**Flatopia SMS System** - Making immigration consultation accessible through SMS! 📱🌍
