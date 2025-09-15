"""
Start Simple SMS Service for Flatopia
Runs the SMS API service without MessageMedia SDK dependency
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
    print("🚀 Starting Flatopia Simple SMS Service")
    print("=" * 50)
    print("📱 SMS API will be available at: http://localhost:8001")
    print("🔗 Webhook endpoint: http://localhost:8001/sms/webhook")
    print("📊 Health check: http://localhost:8001/sms/health")
    print("=" * 50)
    
    # Set environment variables
    os.environ.setdefault("GROQ_API_KEY", "GROQ_KEY_REMOVED")
    os.environ.setdefault("OPENAI_API_KEY", "OPENAI_KEY_REMOVED")
    
    # Run the SMS API service
    uvicorn.run(
        "api.simple_sms_api:sms_app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
