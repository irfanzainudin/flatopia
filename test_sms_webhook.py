"""
Test SMS Webhook locally
Simulates MessageMedia webhook calls for testing
"""
import requests
import json

def test_sms_webhook():
    """Test SMS webhook with sample data"""
    
    # Webhook URL (adjust if using different port)
    webhook_url = "http://localhost:8001/sms/webhook"
    
    # Sample webhook data from MessageMedia
    test_data = {
        "message_id": "test_123456",
        "from": "+1234567890",  # Your test phone number
        "content": "hi",
        "timestamp": "2025-01-15T10:30:00Z"
    }
    
    print("🧪 Testing SMS Webhook")
    print("=" * 50)
    print(f"📱 Sending to: {webhook_url}")
    print(f"📞 From: {test_data['from']}")
    print(f"💬 Message: {test_data['content']}")
    print()
    
    try:
        # Send POST request to webhook
        response = requests.post(
            webhook_url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Webhook test successful!")
        else:
            print("❌ Webhook test failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure SMS service is running on port 8001")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_full_conversation():
    """Test a full SMS conversation flow"""
    
    webhook_url = "http://localhost:8001/sms/webhook"
    phone_number = "+1234567890"
    
    # Test conversation steps
    conversation = [
        "hi",
        "16",
        "Indian", 
        "2",
        "1",
        "planning ielts",
        "4",
        "1",
        "AU",
        "yes"
    ]
    
    print("\n🔄 Testing Full Conversation Flow")
    print("=" * 50)
    
    for i, message in enumerate(conversation, 1):
        print(f"\n📱 Step {i}: Sending '{message}'")
        
        test_data = {
            "message_id": f"test_{i}",
            "from": phone_number,
            "content": message,
            "timestamp": "2025-01-15T10:30:00Z"
        }
        
        try:
            response = requests.post(
                webhook_url,
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"🤖 Bot: {result.get('response', 'No response')}")
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            break

if __name__ == "__main__":
    # Test single webhook call
    test_sms_webhook()
    
    # Test full conversation
    test_full_conversation()
