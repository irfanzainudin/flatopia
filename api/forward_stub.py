"""
Minimal Forward Backend for Flatopia SMS
Accepts JSON {"from":"+61...","content":"..."} and optional headers, returns a short response.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import re

forward_app = FastAPI(title="Flatopia Forward Stub", version="1.0.0")


@forward_app.post("/sms/ingest")
async def ingest(request: Request):
    try:
        data = {}
        try:
            data = await request.json()
        except Exception:
            data = {}

        headers = request.headers
        from_header = headers.get("X-From-Number") or headers.get("x-from-number") or ""
        text_header = headers.get("X-Message-Content") or headers.get("x-message-content") or ""

        phone = (data.get("from") or from_header or "").strip()
        text = (data.get("content") or text_header or "").strip()

        # Very small demo logic: greet on hi; detect age 10-80; otherwise echo
        reply = ""
        if not text:
            reply = "Hi! Please tell me your age."
        else:
            low = text.lower().strip()
            if low in ["hi", "hello", "hey"]:
                reply = "Welcome to Flatopia! What's your age?"
            else:
                m = re.search(r"\b(\d{1,2})\b", text)
                if m:
                    age = int(m.group(1))
                    if 10 <= age <= 80:
                        reply = "Got it. Which passport do you hold?"
                if not reply:
                    reply = "Thanks! Please share your age (number)."

        # Ensure <=160 chars
        if len(reply) > 160:
            reply = reply[:157] + "..."

        return JSONResponse({"status": "ok", "response": reply, "echo_from": phone})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.forward_stub:forward_app", host="0.0.0.0", port=9000)


