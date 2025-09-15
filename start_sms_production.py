"""
Production SMS Service for Flatopia
稳定版本，关闭文件监控
"""
import uvicorn
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from api.simple_sms_api import sms_app

if __name__ == "__main__":
    print("🚀 Starting Flatopia Production SMS Service")
    print("=" * 60)
    print("📱 SMS API will be available at: http://localhost:8001")
    print("🔗 Webhook endpoint: http://localhost:8001/sms/webhook")
    print("📊 Health check: http://localhost:8001/sms/health")
    print("🔧 Production mode: File monitoring disabled")
    print("=" * 60)
    
    # Load credentials from env only (do not hardcode secrets in code)
    os.environ.setdefault("MESSAGEMEDIA_SOURCE_NUMBER", os.environ.get("MESSAGEMEDIA_SOURCE_NUMBER", "+61499352828"))
    
    # Run the SMS API service in production mode
    uvicorn.run(
        "api.simple_sms_api:sms_app",
        host="0.0.0.0",
        port=8001,
        reload=False,  # 关闭文件监控
        log_level="info"
    )
