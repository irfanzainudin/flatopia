"""
SMS监控工具
监控SMS服务状态和对话
"""
import requests
import json
import time
from datetime import datetime

class SMSMonitor:
    """SMS监控工具"""
    
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.agent_number = "0477619672"
    
    def check_service_health(self):
        """检查服务健康状态"""
        try:
            response = requests.get(f"{self.base_url}/sms/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 服务状态: {data['status']}")
                print(f"🕐 时间: {data['timestamp']}")
                return True
            else:
                print(f"❌ 服务异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False
    
    def get_user_status(self, phone_number):
        """获取用户状态"""
        try:
            response = requests.get(f"{self.base_url}/sms/status/{phone_number}")
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    session = data.get('session', {})
                    print(f"📱 用户: {phone_number}")
                    print(f"📊 当前阶段: {session.get('current_stage', 'unknown')}")
                    print(f"👤 姓名: {session.get('name', 'N/A')}")
                    print(f"🎂 年龄: {session.get('age', 'N/A')}")
                    print(f"🌍 国籍: {session.get('nationality', 'N/A')}")
                    print(f"🎓 教育: {session.get('education_level', 'N/A')}")
                    print(f"🔬 专业: {session.get('field_of_interest', 'N/A')}")
                    return session
                else:
                    print(f"❌ 用户未找到: {phone_number}")
                    return None
            else:
                print(f"❌ 获取状态失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ 错误: {e}")
            return None
    
    def get_conversation_history(self, phone_number, limit=10):
        """获取对话历史"""
        try:
            response = requests.get(f"{self.base_url}/sms/history/{phone_number}?limit={limit}")
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    history = data.get('history', [])
                    print(f"\n📜 对话历史 ({len(history)} 条消息):")
                    print("-" * 50)
                    for msg in reversed(history):  # 显示最新的消息
                        timestamp = msg.get('timestamp', 'N/A')
                        msg_type = msg.get('message_type', 'unknown')
                        content = msg.get('content', '')
                        print(f"[{timestamp}] {msg_type}: {content}")
                    return history
                else:
                    print(f"❌ 获取历史失败")
                    return []
            else:
                print(f"❌ 获取历史失败: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ 错误: {e}")
            return []
    
    def monitor_realtime(self, phone_number, duration=300):
        """实时监控（5分钟）"""
        print(f"🔍 开始实时监控 {phone_number}")
        print(f"⏱️  监控时长: {duration} 秒")
        print("=" * 50)
        
        start_time = time.time()
        last_message_count = 0
        
        while time.time() - start_time < duration:
            try:
                # 检查服务状态
                if not self.check_service_health():
                    print("❌ 服务不可用，停止监控")
                    break
                
                # 获取对话历史
                history = self.get_conversation_history(phone_number, 5)
                current_count = len(history)
                
                if current_count > last_message_count:
                    print(f"\n🆕 新消息！当前共 {current_count} 条消息")
                    last_message_count = current_count
                
                # 等待10秒
                time.sleep(10)
                
            except KeyboardInterrupt:
                print("\n⏹️  监控已停止")
                break
            except Exception as e:
                print(f"❌ 监控错误: {e}")
                time.sleep(5)
    
    def send_test_message(self, phone_number, message):
        """发送测试消息"""
        try:
            response = requests.post(
                f"{self.base_url}/sms/webhook",
                json={
                    "message_id": f"test_{int(time.time())}",
                    "from": phone_number,
                    "content": message,
                    "timestamp": datetime.now().isoformat()
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 测试消息发送成功")
                print(f"🤖 机器人回复: {result.get('response', 'No response')}")
                return True
            else:
                print(f"❌ 发送失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 发送错误: {e}")
            return False

def main():
    """主监控函数"""
    print("📱 SMS监控工具")
    print("=" * 40)
    
    monitor = SMSMonitor()
    
    # 检查服务状态
    if not monitor.check_service_health():
        print("❌ 请先启动SMS服务：python start_simple_sms.py")
        return
    
    print("\n选择操作:")
    print("1. 检查用户状态")
    print("2. 查看对话历史")
    print("3. 发送测试消息")
    print("4. 实时监控")
    print("5. 退出")
    
    while True:
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == "1":
            phone = input("输入手机号: ").strip()
            if phone:
                monitor.get_user_status(phone)
        
        elif choice == "2":
            phone = input("输入手机号: ").strip()
            if phone:
                monitor.get_conversation_history(phone)
        
        elif choice == "3":
            phone = input("输入手机号: ").strip()
            message = input("输入消息: ").strip()
            if phone and message:
                monitor.send_test_message(phone, message)
        
        elif choice == "4":
            phone = input("输入手机号: ").strip()
            if phone:
                monitor.monitor_realtime(phone)
        
        elif choice == "5":
            print("👋 再见！")
            break
        
        else:
            print("❌ 无效选择")

if __name__ == "__main__":
    main()
