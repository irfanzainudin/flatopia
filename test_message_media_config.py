"""
Test MessageMedia Configuration
验证MessageMedia配置是否正确
"""
import requests
import json

def test_webhook_configuration():
    """测试webhook配置"""
    print("🧪 Testing MessageMedia Webhook Configuration")
    print("=" * 60)
    
    # 测试webhook端点
    webhook_url = "http://localhost:8001/sms/webhook"
    
    # 模拟MessageMedia发送的webhook数据
    test_data = {
        "message_id": "msg_123456789",
        "from": "+61477619672",  # 使用您提供的代理号码
        "content": "hi",
        "timestamp": "2025-01-15T10:30:00Z",
        "to": "0477619672"  # 您的代理号码
    }
    
    print(f"📱 代理号码: 0477619672")
    print(f"🔗 Webhook URL: {webhook_url}")
    print(f"📞 测试号码: {test_data['from']}")
    print(f"💬 测试消息: {test_data['content']}")
    print()
    
    try:
        response = requests.post(
            webhook_url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 响应成功: {result.get('response', 'No response')}")
            return True
        else:
            print(f"❌ 响应失败: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败！请确保SMS服务正在运行")
        print("   运行: python start_simple_sms.py")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_agent_number_format():
    """测试代理号码格式"""
    print("\n📱 测试代理号码格式")
    print("=" * 40)
    
    agent_number = "0477619672"
    
    # 检查号码格式
    if agent_number.startswith("0"):
        print(f"✅ 代理号码格式正确: {agent_number}")
        print("   这是澳大利亚本地号码格式")
    else:
        print(f"⚠️  代理号码格式: {agent_number}")
        print("   建议使用澳大利亚本地格式 (0xxxxxxxxx)")
    
    # 显示国际格式
    if agent_number.startswith("0"):
        international = "+61" + agent_number[1:]
        print(f"🌍 国际格式: {international}")
    
    return True

def test_full_conversation_flow():
    """测试完整对话流程"""
    print("\n🔄 测试完整对话流程")
    print("=" * 40)
    
    webhook_url = "http://localhost:8001/sms/webhook"
    agent_number = "0477619672"
    
    # 测试对话步骤
    conversation = [
        ("hi", "开始对话"),
        ("16", "提供年龄"),
        ("Indian", "提供国籍"),
        ("2", "选择教育水平"),
        ("1", "选择专业领域"),
        ("planning ielts", "英语测试状态"),
        ("4", "选择优先级"),
        ("1", "选择预算"),
        ("AU", "选择国家"),
        ("yes", "请求大学列表")
    ]
    
    for i, (message, description) in enumerate(conversation, 1):
        print(f"\n📱 步骤 {i}: {description}")
        print(f"👤 用户: {message}")
        
        test_data = {
            "message_id": f"test_{i}",
            "from": "+61477619672",
            "content": message,
            "timestamp": "2025-01-15T10:30:00Z",
            "to": agent_number
        }
        
        try:
            response = requests.post(
                webhook_url,
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                bot_response = result.get('response', 'No response')
                print(f"🤖 机器人: {bot_response}")
            else:
                print(f"❌ 错误: {response.status_code}")
                break
                
        except Exception as e:
            print(f"❌ 错误: {e}")
            break

def main():
    """主测试函数"""
    print("🚀 MessageMedia配置测试工具")
    print("=" * 60)
    
    # 测试代理号码格式
    test_agent_number_format()
    
    # 测试webhook配置
    if test_webhook_configuration():
        print("\n✅ Webhook配置测试通过！")
        
        # 测试完整对话流程
        test_full_conversation_flow()
        
        print("\n🎉 所有测试完成！")
        print("\n📋 下一步操作：")
        print("1. 在MessageMedia控制台设置代理号码: 0477619672")
        print("2. 配置webhook URL指向您的ngrok地址")
        print("3. 从手机发送短信到MessageMedia号码进行真实测试")
    else:
        print("\n❌ 请先启动SMS服务：")
        print("   python start_simple_sms.py")

if __name__ == "__main__":
    main()
