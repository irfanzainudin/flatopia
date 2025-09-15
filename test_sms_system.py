"""
Test SMS System for Flatopia
Simulates SMS conversations to test the system
"""
import asyncio
import sys
import os
import json

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.sms_chat_manager import sms_chat_manager
from core.sms_database import sms_db

async def test_sms_conversation():
    """Test a complete SMS conversation flow"""
    print("🧪 Testing SMS Conversation System")
    print("=" * 50)
    
    # Test phone number
    test_phone = "+1234567890"
    
    # Simulate the conversation from the example
    conversation = [
        ("16", "age_collection"),
        ("Indian", "passport_collection"),
        ("2", "education_collection"),
        ("1", "field_collection"),
        ("planning ielts", "english_test_collection"),
        ("4", "priorities_collection"),
        ("1", "budget_collection"),
        ("AU", "country_details"),
        ("yes", "university_list")
    ]
    
    print(f"📱 Testing with phone number: {test_phone}")
    print()
    
    # Start with greeting
    response = await sms_chat_manager.process_sms(test_phone, "hi")
    print(f"🤖 Bot: {response}")
    print()
    
    # Process each step
    for user_input, expected_stage in conversation:
        print(f"👤 User: {user_input}")
        response = await sms_chat_manager.process_sms(test_phone, user_input)
        print(f"🤖 Bot: {response}")
        print()
        
        # Check if we're in the right stage
        session = sms_db.get_user_session(test_phone)
        if session:
            current_stage = session.get('current_stage', 'unknown')
            print(f"📊 Current stage: {current_stage}")
        else:
            print(f"📊 Current stage: session not found")
        print("-" * 30)
    
    # Get final session data
    final_session = sms_db.get_user_session(test_phone)
    print("📋 Final Session Data:")
    print(json.dumps(final_session, indent=2, default=str))
    
    # Get conversation history
    history = sms_db.get_conversation_history(test_phone, 20)
    print(f"\n📜 Conversation History ({len(history)} messages):")
    for msg in history:
        print(f"  {msg['message_type']}: {msg['content']}")

async def test_character_limit():
    """Test SMS character limit handling"""
    print("\n🔤 Testing Character Limit Handling")
    print("=" * 50)
    
    test_phone = "+1234567891"
    
    # Test with a very long message
    long_message = "This is a very long message that should be truncated because it exceeds the 160 character limit for SMS messages. This message is intentionally long to test the truncation functionality."
    
    response = await sms_chat_manager.process_sms(test_phone, long_message)
    print(f"📱 Long message length: {len(long_message)}")
    print(f"🤖 Response length: {len(response)}")
    print(f"🤖 Response: {response}")

async def test_multiple_users():
    """Test multiple users with different conversations"""
    print("\n👥 Testing Multiple Users")
    print("=" * 50)
    
    users = [
        ("+1111111111", "18", "Chinese"),
        ("+2222222222", "25", "Indian"),
        ("+3333333333", "30", "American")
    ]
    
    for phone, age, nationality in users:
        print(f"\n📱 User {phone}:")
        
        # Start conversation
        response = await sms_chat_manager.process_sms(phone, "hi")
        print(f"  🤖 Bot: {response}")
        
        # Provide age
        response = await sms_chat_manager.process_sms(phone, age)
        print(f"  👤 User: {age}")
        print(f"  🤖 Bot: {response}")
        
        # Provide nationality
        response = await sms_chat_manager.process_sms(phone, nationality)
        print(f"  👤 User: {nationality}")
        print(f"  🤖 Bot: {response}")

async def test_error_handling():
    """Test error handling"""
    print("\n⚠️ Testing Error Handling")
    print("=" * 50)
    
    test_phone = "+9999999999"
    
    # Test with invalid input
    invalid_inputs = ["", "invalid", "999", "xyz"]
    
    for invalid_input in invalid_inputs:
        print(f"👤 User: '{invalid_input}'")
        response = await sms_chat_manager.process_sms(test_phone, invalid_input)
        print(f"🤖 Bot: {response}")
        print()

async def main():
    """Run all tests"""
    print("🚀 Starting SMS System Tests")
    print("=" * 60)
    
    try:
        # Test basic conversation
        await test_sms_conversation()
        
        # Test character limits
        await test_character_limit()
        
        # Test multiple users
        await test_multiple_users()
        
        # Test error handling
        await test_error_handling()
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())