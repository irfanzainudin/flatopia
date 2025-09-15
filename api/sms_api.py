"""
SMS API Service for Flatopia
Handles MessageMedia SMS integration and webhook processing
"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from messagemedia_messages_sdk.controllers.messages_controller import MessagesController
from messagemedia_messages_sdk.models.send_messages_request import SendMessagesRequest
from messagemedia_messages_sdk.models.message import Message
from messagemedia_messages_sdk.configuration import Configuration
from messagemedia_messages_sdk.auth.auth_manager import AuthManager
from core.sms_chat_manager import sms_chat_manager
from core.sms_database import sms_db

logger = logging.getLogger(__name__)

# MessageMedia Configuration
# Per user: API name = "Flatopia", secret as below
MESSAGEMEDIA_API_KEY = "Flatopia"
MESSAGEMEDIA_SECRET_KEY = "cCrxz1ODWHgiWlr9axVT"

# Configure MessageMedia
Configuration.basic_auth_user_name = MESSAGEMEDIA_API_KEY
Configuration.basic_auth_password = MESSAGEMEDIA_SECRET_KEY

class SMSService:
    """SMS Service for handling MessageMedia integration"""
    
    def __init__(self):
        self.messages_controller = MessagesController()
        self.sms_chat_manager = sms_chat_manager
        self.sms_db = sms_db
    
    async def send_sms(self, to_number: str, message: str) -> bool:
        """Send SMS via MessageMedia"""
        try:
            # Create message object
            message_obj = Message(
                content=message,
                destination_number=to_number
            )
            
            # Create send request
            send_request = SendMessagesRequest(
                messages=[message_obj]
            )
            
            # Send message
            result = self.messages_controller.send_messages(send_request)
            
            if result:
                logger.info(f"SMS sent successfully to {to_number}")
                return True
            else:
                logger.error(f"Failed to send SMS to {to_number}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            return False
    
    async def process_incoming_sms(self, from_number: str, message: str) -> str:
        """Process incoming SMS and generate response"""
        try:
            # Process SMS through chat manager
            response = await self.sms_chat_manager.process_sms(from_number, message)
            
            # Send response back
            await self.send_sms(from_number, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing incoming SMS: {e}")
            return "Error processing message"

# Create SMS service instance
sms_service = SMSService()

# Create FastAPI app for SMS
sms_app = FastAPI(
    title="Flatopia SMS API",
    description="SMS API for Flatopia immigration advisor",
    version="1.0.0"
)

@sms_app.post("/sms/webhook")
async def sms_webhook(request: Request):
    """Handle incoming SMS webhook from MessageMedia"""
    try:
        # Parse webhook data
        data = await request.json()
        
        # Extract message details
        from_number = data.get('from', '')
        message_text = data.get('content', '')
        message_id = data.get('message_id', '')
        
        logger.info(f"Received SMS from {from_number}: {message_text}")
        
        # Process the SMS
        response = await sms_service.process_incoming_sms(from_number, message_text)
        
        return JSONResponse({
            "status": "success",
            "message": "SMS processed successfully",
            "response": response
        })
        
    except Exception as e:
        logger.error(f"Error processing SMS webhook: {e}")
        return JSONResponse(
            {"status": "error", "message": str(e)},
            status_code=500
        )

@sms_app.post("/sms/send")
async def send_sms(request: Request):
    """Send SMS manually"""
    try:
        data = await request.json()
        to_number = data.get('to_number')
        message = data.get('message')
        
        if not to_number or not message:
            raise HTTPException(status_code=400, detail="to_number and message are required")
        
        success = await sms_service.send_sms(to_number, message)
        
        if success:
            return JSONResponse({"status": "success", "message": "SMS sent successfully"})
        else:
            return JSONResponse({"status": "error", "message": "Failed to send SMS"}, status_code=500)
            
    except Exception as e:
        logger.error(f"Error sending SMS: {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@sms_app.get("/sms/status/{phone_number}")
async def get_sms_status(phone_number: str):
    """Get SMS conversation status for a phone number"""
    try:
        session = sms_db.get_user_session(phone_number)
        if not session:
            return JSONResponse({"status": "not_found", "message": "No session found"})
        
        return JSONResponse({
            "status": "success",
            "session": session
        })
        
    except Exception as e:
        logger.error(f"Error getting SMS status: {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@sms_app.get("/sms/history/{phone_number}")
async def get_sms_history(phone_number: str, limit: int = 10):
    """Get SMS conversation history for a phone number"""
    try:
        history = sms_db.get_conversation_history(phone_number, limit)
        
        return JSONResponse({
            "status": "success",
            "history": history
        })
        
    except Exception as e:
        logger.error(f"Error getting SMS history: {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@sms_app.post("/sms/cleanup")
async def cleanup_old_data():
    """Clean up old SMS data (older than 12 months)"""
    try:
        sms_db.cleanup_old_data()
        return JSONResponse({"status": "success", "message": "Old data cleaned up"})
        
    except Exception as e:
        logger.error(f"Error cleaning up data: {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@sms_app.get("/sms/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Flatopia SMS API"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(sms_app, host="0.0.0.0", port=8001)
