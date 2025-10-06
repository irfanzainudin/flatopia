"""
FastAPI app: Agent 2 Action Plan Designer with Streaming (SSE)
--------------------------------------------------------------
- Exposes /stream endpoint
- Accepts JSON payload with retrieved_info and optional user_profile
- Streams the action plan progressively to the client
"""

import os
import json
from typing import Dict, Any, Optional

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import uvicorn
import httpx
from message_media_messages.message_media_messages_client import MessageMediaMessagesClient
import json

app = FastAPI()

# Allow only your Next.js frontend during development
origins = [
    "http://localhost:3000",  # Next.js dev server
    "http://127.0.0.1:3000",  # Some setups use 127.0.0.1 instead of localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # allowed origins
    allow_credentials=True,
    allow_methods=["*"],            # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],            # allow all headers
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AGENT2_SYSTEM_PROMPT = """You are an Action Plan Designer AI agent.

Your role is to:
1. **Interpret the retrieved information** (visa categories, eligibility requirements, conditions, timelines, costs, risks, and advantages).
2. **Design a clear, step-by-step action plan** tailored to the user’s situation (based only on the provided information).
3. Present the plan in a **structured, practical, and easy-to-follow format**, highlighting:
   - Immediate next steps the user should take
   - Medium-term preparations (tests, documents, qualifications, or work experience)
   - Long-term considerations (visa progression, permanent residency, citizenship pathways)
4. If multiple pathways are viable, provide a **comparison with pros and cons** and recommend the most promising option.
5. Keep your tone **professional, concise, and supportive**. Avoid speculation outside the retrieved information.

**Output format:**
- A short introduction (1–2 sentences summarizing the visa pathway(s)).
- A numbered step-by-step action plan.
- (Optional) A comparison table if multiple options exist.
- A closing recommendation.

Do not generate new visa rules — rely only on the retrieved information. If information is incomplete, explicitly state what is missing and suggest what the user should clarify or research further.

**Fallback Rules**
- If the JSON is empty, incomplete, or unclear:
  - Politely tell the user that enough information wasn’t found.
  - Suggest how they might rephrase their query (e.g., specify country, visa type, or job role).
  - Recommend visiting the relevant official immigration website.
  - Never fabricate visa or job details.

**Constraints**
- Never expose or repeat the JSON directly to the user.
- Never invent information that isn’t in the JSON.
- Keep tone clear, simple, and helpful.
"""


def build_summary(retrieved_info: Dict[str, Any], user_profile: Optional[Dict[str, Any]] = None) -> str:
    """Convert retrieved JSON into a safe human-readable summary (no raw JSON)."""
    profile_summary = ""
    if user_profile:
        parts = [f"{k.replace('_',' ')}: {v}" for k, v in user_profile.items()]
        profile_summary = "User profile: " + "; ".join(parts)

    visa_summary = []
    if "visa_options" in retrieved_info:
        for idx, opt in enumerate(retrieved_info["visa_options"], start=1):
            visa_summary.append(f"Option {idx}: {opt.get('name','Unnamed visa')}")
            for key in ("eligibility", "key_requirements", "estimated_timeline", "costs", "advantages", "risks"):
                if key in opt:
                    visa_summary.append(f"  - {key}: {opt[key]}")
    else:
        visa_summary.append("No structured visa options found.")

    return profile_summary + "\n\n" + "\n".join(visa_summary)


# @app.post("/stream")
# async def stream_action_plan(request: Request):
#     """Stream the action plan as SSE events."""

#     payload = await request.json()
#     retrieved_info = payload.get("retrieved_info", {})
#     user_profile = payload.get("user_profile", {})

#     # Fallback if no info
#     if not retrieved_info:
#         async def fallback_gen():
#             msg = (
#                 "I couldn’t find enough specific visa pathway information. "
#                 "Please include details such as the country, visa type, or your job role. "
#                 "Also check the official immigration website of your target country."
#             )
#             yield f"data: {msg}\n\n"
#         return StreamingResponse(fallback_gen(), media_type="text/event-stream")

#     content = build_summary(retrieved_info, user_profile)

#     def event_stream():
#         with client.responses.stream(
#             model="gpt-4.1",  # or gpt-4o
#             input=[
#                 {"role": "system", "content": AGENT2_SYSTEM_PROMPT},
#                 {
#                     "role": "user",
#                     "content": (
#                         "Agent 1 retrieved the following visa pathway information. "
#                         "Use only this information to create a clear, step-by-step action plan.\n\n"
#                         f"{content}"
#                     ),
#                 },
#             ],
#         ) as stream:
#             for event in stream:
#                 if event.type == "response.output_text.delta":
#                     yield f"data: {event.delta}\n\n"
#                 elif event.type == "response.completed":
#                     yield "data: [DONE]\n\n"

#     return StreamingResponse(event_stream(), media_type="text/event-stream")

# @app.post("/recommend")
# async def get_action_plan(request: Request):
#     """Return the action plan as JSON."""
#     payload = await request.json()
#     retrieved_info = payload.get("retrieved_info", {})
#     user_profile = payload.get("user_profile", {})

#     if not retrieved_info:
#         return {
#             "status": "error",
#             "message": (
#                 "I couldn’t find enough specific visa pathway information. "
#                 "Please include details such as the country, visa type, or your job role. "
#                 "Also check the official immigration website of your target country."
#             ),
#             "action_plan": None,
#         }

#     content = build_summary(retrieved_info, user_profile)

#     response = client.responses.create(
#         model="gpt-4.1",  # or gpt-4o if available
#         input=[
#             {"role": "system", "content": AGENT2_SYSTEM_PROMPT},
#             {
#                 "role": "user",
#                 "content": (
#                     "Agent 1 retrieved the following visa pathway information. "
#                     "Use only this information to create a clear, step-by-step action plan.\n\n"
#                     f"{content}"
#                 ),
#             },
#         ],
#     )

#     return {
#         "status": "success",
#         "action_plan": response.output_text,  # plain text (often Markdown)
#     }

@app.post("/recommend")
async def get_action_plan(request: Request):
    """Return the action plan as structured JSON."""
    payload = await request.json()
    retrieved_info = payload.get("retrieved_info", {})
    user_profile = payload.get("user_profile", {})

    if not retrieved_info:
        return {
            "status": "error",
            "message": (
                "I couldn’t find enough specific visa pathway information. "
                "Please include details such as the country, visa type, or your job role. "
                "Also check the official immigration website of your target country."
            ),
            "action_plan": None,
        }

    content = build_summary(retrieved_info, user_profile)

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "system", "content": AGENT2_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Agent 1 retrieved the following visa pathway information. "
                    "Use only this information to create the structured action plan JSON.\n\n"
                    f"{content}"
                ),
            },
        ],
    )

    # Try parsing the response as JSON
    try:
        plan_json = json.loads(response.output_text)
    except json.JSONDecodeError:
        # fallback if model outputs invalid JSON
        plan_json = {
            "introduction": "",
            "steps": [],
            "comparison_table": [],
            "recommendation": response.output_text.strip(),
        }

    return {
        "status": "success",
        "action_plan": plan_json,
    }

# System prompt for chatbot
CHATBOT_SYSTEM_PROMPT = """
You are an Action Plan Designer AI agent.
You help users understand visa pathways and create action plans.
Keep answers structured, concise, supportive, and accurate.
Do not fabricate rules — rely only on user-provided info or your knowledge.

Output format:
- Plain text because you are interacting in SMS. Do not output response in Markdown or any format, just plain text.
- Try to keep responses under 160 characters because you are interacting in SMS.
"""


@app.post("/chat")
async def chat_with_agent(request: Request):
    """
    Accept free text from the user and return the AI's reply.
    """
    payload = await request.json()
    user_message = payload.get("message")

    if not user_message:
        return {"status": "error", "message": "No user message provided."}

    response = client.responses.create(
        model="gpt-4.1",  # or gpt-4o
        input=[
            {"role": "system", "content": CHATBOT_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    return {
        "status": "success",
        "reply": response.output_text,
    }

def format_ai_response(ai_data: dict) -> str:
    """
    Convert structured AI JSON into an SMS-friendly text.
    """
    parts = []

    intro = ai_data.get("introduction")
    if intro:
        parts.append(f"Intro: {intro}")

    steps = ai_data.get("steps")
    if steps:
        # If steps is a list, join them; otherwise just stringify
        if isinstance(steps, list):
            step_text = "; ".join(steps)
        else:
            step_text = str(steps)
        parts.append(f"Steps: {step_text}")

    table = ai_data.get("comparison_table")
    if table:
        # Simplify table into key: value pairs (SMS doesn't handle tables well)
        table_lines = []
        for row in table:
            row_text = " | ".join(f"{k}:{v}" for k, v in row.items())
            table_lines.append(row_text)
        parts.append("Table: " + "; ".join(table_lines))

    recommendation = ai_data.get("recommendation")
    if recommendation:
        parts.append(f"Recommendation: {recommendation}")

    # Join everything with line breaks
    sms_text = "\n".join(parts)

    # Trim to ~480 chars (3 SMS segments max, tweak as needed)
    return sms_text[:480]


# Environment variables for security
MESSAGEMEDIA_API_KEY = os.getenv("MESSAGEMEDIA_API_KEY")
MESSAGEMEDIA_API_SECRET = os.getenv("MESSAGEMEDIA_API_SECRET")
MESSAGEMEDIA_BASE_URL = "https://api.messagemedia.com/v1"  # check docs for AU endpoint
AI_BACKEND_URL = "https://api.flatopia.co/chat"

def split_sms(text: str, segment_size: int = 160) -> list[str]:
    """
    Splits long text into multiple SMS-sized chunks.
    """
    return [text[i:i+segment_size] for i in range(0, len(text), segment_size)]

@app.post("/sms/inbound")
async def inbound_sms(request: Request):
    """
    Webhook endpoint for inbound SMS from MessageMedia.
    """
    data = await request.json()
    print("Inbound SMS:", data)

    # Extract sender & message text
    message = data.get("content", "")
    sender_number = data.get("source_number")

    if not sender_number or not message:
        return {"status": "ignored"}

    print("Inbound webhook payload:", data)
    print("Extracted message:", message)

    # Forward message to AI backend
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model="gpt-4.1",  # or gpt-4o
        input=[
            {"role": "system", "content": CHATBOT_SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
    )

    #return {
    #    "status": "success",
    #    "reply": response.output_text,
    #}
    #async with httpx.AsyncClient() as client:
    #    ai_response = await client.post(AI_BACKEND_URL, json={"message": message})
    #    ai_data = ai_response.json()

    ai_response = response.output_text
    ai_data = ai_response

    # Convert AI JSON into SMS text
    reply_text = ai_data
    print("reply text: ", reply_text)

    # Split into multiple SMS messages if needed
    segments = split_sms(reply_text)
    print("segments: ", segments)

    # Build payload with multiple messages
    sms_payload = {
        "messages": [
            {
                "content": seg,
                "destination_number": sender_number,
                "format": "SMS"
            } for seg in segments
        ]
    }
    print("sms_payload: ", sms_payload)

    # Send via MessageMedia
    auth_user_name = 'iPS70TaoBJNLmotJqCuf'
    auth_password = 'R8InBGglUYDz3IT7fUip86VgXL39rI'
    use_hmac_authentication = False

    client = MessageMediaMessagesClient(auth_user_name, auth_password, use_hmac_authentication)
    messages_client = client.messages

    body_value = json.dumps(sms_payload)
    print(body_value)

    body = json.loads(body_value)

    result = messages_client.send_messages(body)
    #async with httpx.AsyncClient() as client:
    #    await client.post(
    #        f"{MESSAGEMEDIA_BASE_URL}/messages",
    #        auth=(MESSAGEMEDIA_API_KEY, MESSAGEMEDIA_API_SECRET),
    #        json=sms_payload
    #    )

def main():
    uvicorn.run("fastapi_chatgpt_wrapper:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
