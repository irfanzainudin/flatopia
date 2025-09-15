"""
Mobile SMS Testing Tool for Flatopia
Simulates mobile phone SMS interactions
"""
import requests
import json
import time

class MobileSMSTester:
    """Mobile SMS testing tool"""
    
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.webhook_url = f"{base_url}/sms/webhook"
        self.send_url = f"{base_url}/sms/send"
        self.status_url = f"{base_url}/sms/status"
        self.history_url = f"{base_url}/sms/history"
    
    def send_sms(self, phone_number: str, message: str):
        """Send SMS via webhook (simulating MessageMedia)"""
        data = {
            "message_id": f"test_{int(time.time())}",
            "from": phone_number,
            "content": message,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response')
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Connection error: {e}"
    
    def get_status(self, phone_number: str):
        """Get user session status"""
        try:
            response = requests.get(f"{self.status_url}/{phone_number}")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_history(self, phone_number: str, limit: int = 10):
        """Get conversation history"""
        try:
            response = requests.get(f"{self.history_url}/{phone_number}?limit={limit}")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def test_conversation(self, phone_number: str):
        """Test a complete conversation flow"""
        print(f"📱 Testing SMS conversation with {phone_number}")
        print("=" * 60)
        
        # Test conversation steps
        steps = [
            ("hi", "Start conversation"),
            ("16", "Provide age"),
            ("Indian", "Provide nationality"),
            ("2", "Select education level"),
            ("1", "Select field of interest"),
            ("planning ielts", "English test status"),
            ("4", "Select priorities"),
            ("1", "Select budget"),
            ("AU", "Select country"),
            ("yes", "Request university list")
        ]
        
        for i, (message, description) in enumerate(steps, 1):
            print(f"\n📱 Step {i}: {description}")
            print(f"👤 User: {message}")
            
            response = self.send_sms(phone_number, message)
            print(f"🤖 Bot: {response}")
            
            # Add delay between messages
            time.sleep(1)
        
        # Show final status
        print(f"\n📊 Final Status:")
        status = self.get_status(phone_number)
        print(json.dumps(status, indent=2, default=str))
        
        # Show conversation history
        print(f"\n📜 Conversation History:")
        history = self.get_history(phone_number, 20)
        if 'history' in history:
            for msg in history['history']:
                print(f"  {msg['message_type']}: {msg['content']}")
    
    def interactive_test(self, phone_number: str):
        """Interactive SMS testing"""
        print(f"📱 Interactive SMS Testing with {phone_number}")
        print("=" * 60)
        print("Type 'quit' to exit, 'status' to check status, 'history' to see history")
        print()
        
        while True:
            message = input("👤 You: ").strip()
            
            if message.lower() == 'quit':
                break
            elif message.lower() == 'status':
                status = self.get_status(phone_number)
                print(f"📊 Status: {json.dumps(status, indent=2, default=str)}")
                continue
            elif message.lower() == 'history':
                history = self.get_history(phone_number)
                if 'history' in history:
                    for msg in history['history']:
                        print(f"  {msg['message_type']}: {msg['content']}")
                continue
            elif not message:
                continue
            
            response = self.send_sms(phone_number, message)
            print(f"🤖 Bot: {response}")

def main():
    """Main testing function"""
    print("🚀 Flatopia Mobile SMS Testing Tool")
    print("=" * 60)
    
    # Check if service is running
    try:
        response = requests.get("http://localhost:8001/sms/health")
        if response.status_code == 200:
            print("✅ SMS service is running")
        else:
            print("❌ SMS service is not responding")
            return
    except:
        print("❌ SMS service is not running. Please start it first:")
        print("   python start_simple_sms.py")
        return
    
    tester = MobileSMSTester()
    
    # Test phone number
    test_phone = "+1234567890"
    
    print(f"\n选择测试模式:")
    print("1. 自动完整对话测试")
    print("2. 交互式测试")
    print("3. 自定义测试")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == "1":
        tester.test_conversation(test_phone)
    elif choice == "2":
        tester.interactive_test(test_phone)
    elif choice == "3":
        phone = input("输入测试手机号: ").strip()
        if phone:
            tester.interactive_test(phone)
    else:
        print("无效选择")

if __name__ == "__main__":
    main()
