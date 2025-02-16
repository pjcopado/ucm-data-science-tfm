from __future__ import annotations as _annotations

import asyncio
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="", tags=["chat"])


from fastapi.responses import StreamingResponse

import asyncio
import json
import random
import loguru
import uuid


LONG_TEXT = (
    "This is a long text that will be streamed in chunks."
    # "Streaming large responses is useful when dealing with AI-generated text, "
    # "news articles, or other lengthy content. "
    # "Each sentence is sent as a JSON object to simulate real-time generation."
)


async def event_stream():
    record_id = str(uuid.uuid4())
    chunks = LONG_TEXT.split(" ")

    """Envía un objeto JSON en partes como eventos SSE."""
    data = {"id": record_id, "content": ""}

    yield f"data: {json.dumps({'id': data['id']})}\n\n"
    await asyncio.sleep(1)

    for word in chunks:
        data["content"] += word + " "
        loguru.logger.info(f"Enviando chunk: {data["content"].strip()}")
        yield f"data: {json.dumps({'content': data['content']})}\n\n"
        sleep_time = random.randint(1, 5) / 10
        await asyncio.sleep(sleep_time)

    yield f"data: {json.dumps({'end': True})}\n\n"


@router.get("/event_stream")
async def stream_long_json():
    """Streams long text in JSON format."""
    return StreamingResponse(event_stream(), media_type="text/event-stream")
