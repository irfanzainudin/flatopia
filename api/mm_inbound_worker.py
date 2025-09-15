"""
MessageMedia Inbound Polling Worker
- Periodically fetches inbound SMS from MessageMedia REST API
- Feeds messages into sms_chat_manager, then replies via MessageMedia
- Deduplicates by message_id to avoid reprocessing
"""
import os
import json
import time
import logging
import asyncio
import requests
from pathlib import Path
from typing import Dict, Any, List
import sys

# Ensure project root on sys.path for core imports
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from core.sms_chat_manager import sms_chat_manager
from core.sms_database import sms_db
from api.simple_sms_api import _send_via_messagemedia

logger = logging.getLogger(__name__)

RUN_DIR = ROOT / ".run"
RUN_DIR.mkdir(exist_ok=True)
SEEN_FILE = RUN_DIR / "mm_inbound_seen.json"


def _get_mm_credentials():
    api_key = os.environ.get("MESSAGEMEDIA_API_KEY", "").strip()
    api_secret = os.environ.get("MESSAGEMEDIA_SECRET_KEY", "").strip()
    return api_key, api_secret


def _load_seen_ids() -> set:
    try:
        if not SEEN_FILE.exists():
            return set()
        data = json.loads(SEEN_FILE.read_text())
        return set(data or [])
    except Exception:
        return set()


def _save_seen_ids(seen: set):
    try:
        SEEN_FILE.write_text(json.dumps(list(seen)) )
    except Exception:
        pass


def _normalize_from(num: str) -> str:
    import re
    digits = re.sub(r"\D", "", num or "")
    return digits


def _pick(d: Dict[str, Any], names: List[str]) -> str:
    for n in names:
        v = d.get(n)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def _fetch_inbound_once(api_key: str, api_secret: str) -> List[Dict[str, Any]]:
    """Try multiple endpoints to fetch inbound messages."""
    sess = requests.Session()
    sess.auth = (api_key, api_secret)
    urls = [
        "https://api.messagemedia.com/v1/replies",
        "https://api.messagemedia.com/v1/messages/inbound",
    ]
    for url in urls:
        try:
            resp = sess.get(url, timeout=15)
            if resp.status_code == 200:
                try:
                    data = resp.json()
                except Exception:
                    continue
                # Normalize list of messages
                if isinstance(data, dict):
                    if "replies" in data and isinstance(data["replies"], list):
                        return data["replies"]
                    if "messages" in data and isinstance(data["messages"], list):
                        return data["messages"]
                elif isinstance(data, list):
                    return data
        except Exception as e:
            logger.error(f"Inbound fetch error from {url}: {e}")
    return []


async def _process_message(item: Dict[str, Any]):
    """Process a single inbound message through chat manager and reply."""
    # Extract fields
    msg_id = _pick(item, ["message_id", "reply_id", "id"]) or ""
    from_number = _pick(item, ["source_number", "from", "msisdn", "sender", "originating_address"]) or ""
    content = _pick(item, ["content", "text", "body", "message"]) or ""

    if not from_number or not content:
        logger.info(f"Inbound message ignored (missing from/content): {json.dumps(item)[:400]}")
        return

    # Feed into chat logic
    response = await sms_chat_manager.process_sms(from_number, content)
    # Send reply via MessageMedia
    _send_via_messagemedia(from_number, response)


async def run_worker():
    api_key, api_secret = _get_mm_credentials()
    if not api_key or not api_secret:
        logger.error("MessageMedia credentials missing for inbound worker.")
        return

    interval = max(3, int(os.environ.get("MM_INBOUND_POLL_INTERVAL", "5") or 5))
    seen = _load_seen_ids()
    logger.info(f"Inbound worker started. Interval={interval}s, seen={len(seen)}")

    while True:
        try:
            items = _fetch_inbound_once(api_key, api_secret) or []
            new_count = 0
            for it in items:
                msg_id = _pick(it, ["message_id", "reply_id", "id"]) or ""
                if msg_id and msg_id in seen:
                    continue
                await _process_message(it)
                if msg_id:
                    seen.add(msg_id)
                    new_count += 1
            if new_count:
                _save_seen_ids(seen)
                logger.info(f"Processed {new_count} new inbound messages.")
        except Exception as e:
            logger.error(f"Inbound worker loop error: {e}")

        await asyncio.sleep(interval)


if __name__ == "__main__":
    asyncio.run(run_worker())


