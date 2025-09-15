"""
Simple SMS API Service for Flatopia
Handles SMS webhook processing without MessageMedia SDK dependency
"""
import os
import json
import logging
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from core.sms_chat_manager import sms_chat_manager
from core.sms_database import sms_db

logger = logging.getLogger(__name__)

# Create FastAPI app for SMS
sms_app = FastAPI(
    title="Flatopia SMS API",
    description="SMS API for Flatopia immigration advisor",
    version="1.0.0"
)

def _normalize_phone(num: str) -> str:
    try:
        import re
        digits = re.sub(r"\D", "", num or "")
        # Keep as-is for now; DB使用不带'+'的国际格式（如 614xxxxxxxx）
        return digits
    except Exception:
        return num or ""

def _get_mm_credentials():
    """Fetch MessageMedia credentials from environment variables."""
    api_key = os.environ.get("MESSAGEMEDIA_API_KEY", "").strip()
    api_secret = os.environ.get("MESSAGEMEDIA_SECRET_KEY", "").strip()
    return api_key, api_secret

def _get_hmac_secret():
    return os.environ.get("MESSAGEMEDIA_HMAC_SECRET", "").strip()

def _verify_hmac(raw_body: bytes, provided_sig: str, secret: str) -> bool:
    """Verify HMAC signature. Accepts sha256(base64) or sha1(hex) forms.
    - provided_sig: header value (e.g., X-MessageMedia-Signature)
    """
    try:
        import hmac, hashlib, base64
        if not raw_body:
            raw_body = b""
        # Try sha256 base64
        mac256 = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).digest()
        sig256 = base64.b64encode(mac256).decode("utf-8").strip()
        if hmac.compare_digest(sig256, (provided_sig or "").strip()):
            return True
        # Try sha1 hex (some providers use this canonical)
        mac1 = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha1).hexdigest().strip()
        if hmac.compare_digest(mac1, (provided_sig or "").strip().lower()):
            return True
    except Exception:
        return False
    return False

def _send_via_messagemedia(to_number: str, message: str) -> bool:
    """Send SMS using MessageMedia REST API via Basic Auth.
    Returns True if accepted, False otherwise.
    """
    api_key, api_secret = _get_mm_credentials()
    if not api_key or not api_secret:
        logger.warning("MessageMedia credentials missing; skipping real send.")
        return False

def _forward_to_backend(forward_url: str, from_number: str, message_text: str) -> Optional[str]:
    """Forward the message to external Flatopia backend and return its response text.
    Expects backend to accept JSON {"from":"+61...","content":"..."} and return either
    JSON with a 'response'/'message' field or raw text.
    """
    try:
        payload = {"from": from_number, "content": message_text}
        # Include helpful headers for downstream services
        headers = {
            "Content-Type": "application/json",
            "X-From-Number": from_number,
            "X-Message-Content": message_text,
            "X-Flatopia-From": from_number
        }
        resp = requests.post(forward_url, json=payload, headers=headers, timeout=15)
        # Prefer JSON
        try:
            data = resp.json()
            if isinstance(data, dict):
                return (data.get("response") or data.get("message") or "").strip()
        except Exception:
            pass
        # Fallback text
        return (resp.text or "").strip()
    except Exception as exc:
        logger.error("Forward to backend failed: %s", exc)
        return None

    try:
        url = "https://api.messagemedia.com/v1/messages"
        source_number = os.environ.get("MESSAGEMEDIA_SOURCE_NUMBER", "+61499352828").strip()
        # Normalize destination to E.164 (ensure leading '+')
        dest = (to_number or "").strip()
        import re as _re
        digits = _re.sub(r"\D", "", dest)
        if digits:
            # If already has '+', keep; else add '+'
            if not dest.startswith('+'):
                # Special-case: Australian 61..., US 1..., else just prefix '+'
                if digits.startswith('61') or digits.startswith('1'):
                    dest = "+" + digits
                else:
                    dest = "+" + digits
        else:
            dest = to_number
        payload = {
            "messages": [
                {
                    "content": message,
                    "destination_number": dest,
                    "source_number": source_number
                }
            ]
        }
        resp = requests.post(url, auth=(api_key, api_secret), json=payload, timeout=15)
        if resp.status_code in (200, 201, 202):
            logger.info("MessageMedia send accepted [dest=%s, src=%s, http=%s]: %s", dest, source_number, resp.status_code, resp.text)
            return True
        logger.error("MessageMedia send failed [http=%s, dest=%s, src=%s]: %s | payload=%s", resp.status_code, dest, source_number, resp.text, json.dumps(payload))
        return False
    except Exception as exc:
        logger.error("Error sending via MessageMedia: %s", exc)
        return False

@sms_app.post("/sms/webhook")
async def sms_webhook(request: Request):
    """Handle incoming SMS webhook from MessageMedia and similar providers."""
    try:
        # Quick-path: read query params first (highest reliability on some consoles)
        qp_from = (
            request.query_params.get('from')
            or request.query_params.get('source_number')
            or request.query_params.get('source-number')
            or request.query_params.get('msisdn')
            or request.query_params.get('sender')
            or request.query_params.get('number')
            or request.query_params.get('phone')
            or request.query_params.get('mobile')
        )
        qp_text = (
            request.query_params.get('content')
            or request.query_params.get('text')
            or request.query_params.get('body')
            or request.query_params.get('message')
            or request.query_params.get('message_content')
            or request.query_params.get('message-content')
        )

        # Read raw body once for HMAC and parsing
        raw_bytes = await request.body()
        raw_text = raw_bytes.decode("utf-8", errors="ignore").strip()

        # Optional HMAC verification
        hmac_secret = _get_hmac_secret()
        header_sig = (
            request.headers.get('x-messagemedia-signature')
            or request.headers.get('x-messagemedia-signature'.title())
            or request.headers.get('x-messagemedia-signature'.upper())
            or request.headers.get('x-signature')
        )
        if hmac_secret and header_sig:
            ok = _verify_hmac(raw_bytes, header_sig, hmac_secret)
            if not ok:
                return JSONResponse({"status": "unauthorized", "message": "invalid hmac"}, status_code=401)

        # 1) Try JSON body
        data: Dict[str, Any] = {}
        try:
            if raw_text:
                data = json.loads(raw_text)
            else:
                data = {}
        except Exception:
            data = {}

        # 2) Try raw body (form-encoded or payload=<json>)
        if not data:
            if raw_text:
                try:
                    # payload=<json>
                    if raw_text.startswith("payload="):
                        from urllib.parse import parse_qs
                        parsed = parse_qs(raw_text)
                        payload_list = parsed.get("payload") or []
                        if payload_list:
                            data = json.loads(payload_list[0])
                    else:
                        # direct JSON
                        data = json.loads(raw_text)
                except Exception:
                    try:
                        # parse as query-string style body
                        from urllib.parse import parse_qs
                        form = parse_qs(raw_text)
                        data = {k: (v[0] if isinstance(v, list) and v else v) for k, v in form.items()}
                    except Exception:
                        data = {}

        # 3) Merge in request.form() if available
        try:
            form = await request.form()
            for k, v in form.items():
                if k not in data or not data.get(k):
                    data[k] = v
        except Exception:
            pass

        # 4) Merge in query params
        try:
            for k, v in request.query_params.items():
                if k not in data or not data.get(k):
                    data[k] = v
        except Exception:
            pass

        # 5) Case-insensitive lookup helper
        def pick(d: Dict[str, Any], keys):
            for key in keys:
                for k in d.keys():
                    if k.lower() == key:
                        val = d.get(k)
                        if isinstance(val, str):
                            return val.strip()
                        return val
            return ""

        # 5.1) Deep search helper over nested structures
        def deep_pick(obj, want_key_parts):
            try:
                from collections.abc import Mapping, Sequence
                def _match_key(k: str):
                    kl = (k or '').lower().replace('-', '').replace('_', '')
                    return all(p in kl for p in want_key_parts)
                stack = [obj]
                while stack:
                    cur = stack.pop()
                    if isinstance(cur, Mapping):
                        for k, v in cur.items():
                            if isinstance(k, str) and _match_key(k):
                                if isinstance(v, str):
                                    return v.strip()
                                try:
                                    return str(v).strip()
                                except Exception:
                                    pass
                            stack.append(v)
                    elif isinstance(cur, Sequence) and not isinstance(cur, (str, bytes)):
                        stack.extend(cur)
            except Exception:
                pass
            return ''

        # 6) Extract from nested or flat structures
        from_number = (qp_from or "").strip()
        message_text = (qp_text or "").strip()
        message_id = ""

        # Nested messages array
        if not from_number and isinstance(data, dict) and 'messages' in data and isinstance(data['messages'], list) and data['messages']:
            msg = data['messages'][0]
            from_number = pick(msg, ['source_number', 'from', 'sender', 'msisdn', 'origin', 'originating_address', 'originatingaddress']) or ""
            message_text = pick(msg, ['content', 'text', 'body', 'message', 'message_content', 'messagecontent']) or ""
            message_id = pick(msg, ['message_id', 'id']) or ""
        elif not from_number and isinstance(data, dict):
            from_number = pick(data, ['from', 'source_number', 'sender', 'msisdn', 'origin', 'originating_address', 'originatingaddress']) or ""
            message_text = pick(data, ['content', 'text', 'body', 'message', 'message_content', 'messagecontent']) or ""
            message_id = pick(data, ['message_id', 'id']) or ""

        # 6.1) As a final attempt, deep search any key variants in the entire payload
        if not from_number and data:
            from_number = deep_pick(data, ['source','number']) or deep_pick(data, ['from']) or deep_pick(data, ['msisdn']) or deep_pick(data, ['sender'])
        if not message_text and data:
            message_text = deep_pick(data, ['content']) or deep_pick(data, ['text']) or deep_pick(data, ['body']) or deep_pick(data, ['message'])

        # 7) Final fallbacks: headers (some providers map into headers)
        if not from_number:
            try:
                hdr = request.headers
                # check a wide set of common keys (case-insensitive)
                candidates = ['x-source-number','x-from','x-msisdn','x-sender','x-phone','x-mobile','from','source_number','source-number','msisdn','sender']
                for ck in candidates:
                    val = hdr.get(ck)
                    if not val:
                        # try alternate case
                        val = hdr.get(ck.upper()) or hdr.get(ck.title())
                    if val:
                        from_number = val.strip()
                        break
            except Exception:
                pass
        if not message_text:
            try:
                hdr = request.headers
                candidates = ['x-message-content','x-text','x-body','content','text','body','message']
                for ck in candidates:
                    val = hdr.get(ck) or hdr.get(ck.upper()) or hdr.get(ck.title())
                    if val:
                        message_text = val.strip()
                        break
            except Exception:
                pass

        # Log with capped raw for debugging
        try:
            safe_raw = json.dumps(data)[:500]
        except Exception:
            safe_raw = str(data)[:500]
        logger.info(f"Received SMS | from='{from_number}' | text='{message_text}' | raw={safe_raw} | qp_from='{qp_from}' qp_text='{qp_text}' | env_fallback='{os.environ.get('FALLBACK_FROM','')}'")

        # If still missing, allow optional env fallback for testing
        if not from_number:
            fallback_from = os.environ.get('FALLBACK_FROM', '').strip()
            if fallback_from:
                from_number = fallback_from

        # If still missing, decide behavior
        if not from_number:
            return JSONResponse({"status": "ignored", "message": "missing from"}, status_code=200)
        if not message_text:
            # Default to hi to trigger greeting
            message_text = "hi"

        # Process the SMS: forward-to-backend if configured, else local manager
        forward_url = os.environ.get("FLATOPIA_FORWARD_URL", "").strip()
        if forward_url:
            response = _forward_to_backend(forward_url, from_number, message_text) or "Sorry, there was an error. Please try again."
        else:
            response = await sms_chat_manager.process_sms(from_number, message_text)

        # Attempt to send reply via MessageMedia if credentials exist
        _send_via_messagemedia(from_number, response)

        return JSONResponse({
            "status": "success",
            "message": "SMS processed successfully",
            "response": response
        })
    except Exception as e:
        logger.error(f"Error processing SMS webhook: {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# Alias route to support external webhook path
@sms_app.post("/webhook/sms")
async def sms_webhook_alias(request: Request):
    return await sms_webhook(request)

# Allow GET/HEAD for provider verification
@sms_app.get("/webhook/sms")
async def sms_webhook_alias_get():
    return JSONResponse({"status": "ok", "message": "webhook alive"})

@sms_app.head("/webhook/sms")
async def sms_webhook_alias_head():
    return JSONResponse({"status": "ok"})

@sms_app.get("/sms/webhook")
async def sms_webhook_get():
    return JSONResponse({"status": "ok", "message": "webhook alive"})

@sms_app.head("/sms/webhook")
async def sms_webhook_head():
    return JSONResponse({"status": "ok"})

@sms_app.get("/sms/mm-auth-test")
async def mm_auth_test():
    """Validate MessageMedia credentials with a harmless request."""
    api_key, api_secret = _get_mm_credentials()
    if not api_key or not api_secret:
        return JSONResponse({"status": "error", "message": "Missing MESSAGEMEDIA_API_KEY/SECRET_KEY"}, status_code=400)
    try:
        url = "https://api.messagemedia.com/v1/delivery_reports"
        resp = requests.get(url, auth=(api_key, api_secret), timeout=15)
        return JSONResponse({
            "status": "ok" if resp.status_code == 200 else "error",
            "http_status": resp.status_code,
            "body": resp.text[:500]
        }, status_code=200)
    except Exception as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=500)

@sms_app.post("/sms/send")
async def send_sms(request: Request):
    """Send SMS manually (simulation)"""
    try:
        data = await request.json()
        to_number = data.get('to_number')
        message = data.get('message')
        
        if not to_number or not message:
            raise HTTPException(status_code=400, detail="to_number and message are required")
        
        # Real send via MessageMedia
        accepted = _send_via_messagemedia(to_number, message)
        status = "success" if accepted else "error"
        msg = "SMS sent successfully" if accepted else "Failed to send SMS"
        return JSONResponse({"status": status, "message": msg, "to_number": to_number, "content": message})
            
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

@sms_app.post("/sms/reset/{phone_number}")
async def reset_conversation(phone_number: str):
    """Reset conversation state and clear records for a phone number"""
    try:
        pn = _normalize_phone(phone_number)
        # Clear session row
        session = sms_db.get_user_session(pn)
        if session:
            # Overwrite fields to None/defaults and set stage to greeting
            sms_db.update_user_session(pn, {
                'name': None,
                'age': None,
                'nationality': None,
                'education_level': None,
                'field_of_interest': None,
                'english_test_status': None,
                'budget_range': None,
                'priorities': None,
                'country_interest': None,
                'current_stage': 'greeting'
            })
        # Best-effort: remove conversation/history/choices/recommendations via direct SQL
        import sqlite3
        with sqlite3.connect(sms_db.db_path) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM conversation_history WHERE phone_number = ?", (pn,))
            cur.execute("DELETE FROM user_choices WHERE phone_number = ?", (pn,))
            cur.execute("DELETE FROM recommendations WHERE phone_number = ?", (pn,))
            conn.commit()
        return JSONResponse({"status": "success", "message": f"Conversation reset for {pn}"})
    except Exception as e:
        logger.error(f"Error resetting conversation: {e}")
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
