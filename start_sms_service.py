"""
Start SMS Service for Flatopia
Runs the SMS API service with MessageMedia integration
"""
import uvicorn
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from api.sms_api import sms_app

if __name__ == "__main__":
    print("🚀 Starting Flatopia SMS Service")
    print("=" * 50)
    print("📱 SMS API will be available at: http://localhost:8001")
    print("🔗 Webhook endpoint: http://localhost:8001/sms/webhook")
    print("📊 Health check: http://localhost:8001/sms/health")
    print("=" * 50)
    
    # Load credentials from env only (no hardcoded secrets)
    
    # Run the SMS API service
    uvicorn.run(
        sms_app,
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
