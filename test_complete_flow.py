"""
Test complete conversation flow
"""
import asyncio
from core.flatopia_chat_manager import flatopia_chat_manager

async def test_complete_flow():
    """Test the complete conversation flow"""
    
    print("🚀 Testing Complete Conversation Flow")
    print("=" * 50)
    
    # Test conversation steps
    test_steps = [
        ("hi！my name is yogri", "Greeting with name"),
        ("I'm 25 years old", "Age information"),
        ("I'm from India", "Nationality"),
        ("I want to study abroad", "Goal"),
        ("Engineering", "Field of interest"),
        ("I have IELTS 6.5", "English test"),
        ("Low tuition fees and work opportunities", "Priorities"),
        ("Under 10 lakhs", "Budget"),
        ("Canada", "Country interest"),
        ("Tell me about universities", "University recommendations")
    ]
    
    for i, (user_input, description) in enumerate(test_steps, 1):
        print(f"\n📱 Step {i}: {description}")
        print(f"User: {user_input}")
        
        try:
            # Process the input
            response = await flatopia_chat_manager.chat(user_input)
            
            print(f"Bot: {response['answer']}")
            print(f"Stage: {response['conversation_stage']}")
            print(f"Profile: {flatopia_chat_manager.user_profile}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            break
        
        print("-" * 30)
    
    print("\n✅ Complete flow test finished!")

if __name__ == "__main__":
    asyncio.run(test_complete_flow())
