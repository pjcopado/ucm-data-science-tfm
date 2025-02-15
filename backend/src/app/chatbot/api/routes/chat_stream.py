from __future__ import annotations as _annotations

import asyncio
import json
import sqlite3
from collections.abc import AsyncIterator
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import partial
from pathlib import Path
from typing import Annotated, Any, Callable, Literal, TypeVar

import fastapi
from fastapi import Depends, Request, APIRouter, Query
from fastapi.responses import StreamingResponse
from typing_extensions import LiteralString, ParamSpec, TypedDict

from pydantic_ai import Agent
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.messages import (
    ModelMessage,
    ModelMessagesTypeAdapter,
    ModelRequest,
    ModelResponse,
    TextPart,
    UserPromptPart,
)


router = APIRouter(prefix="", tags=["chat"])


from fastapi.responses import StreamingResponse

# import ollama
import asyncio
import json
import random
import logging
import loguru
import uuid


LONG_TEXT = (
    "This is a long text that will be streamed in chunks. "
    # "Streaming large responses is useful when dealing with AI-generated text, "
    # "news articles, or other lengthy content. "
    # "Each sentence is sent as a JSON object to simulate real-time generation."
)


async def long_json_stream():
    """Simulates a long text response, streamed in JSON format."""

    # Split text into chunks (simulating AI response generation)
    chunks = LONG_TEXT.split(" ")

    current_text = ""
    for word in chunks:
        current_text += word + " "
        loguru.logger.info(current_text)
        yield json.dumps({"content": current_text.strip()}) + "\n"
        sleep_time = random.randint(1, 5) / 10
        await asyncio.sleep(sleep_time)  # Simulate streaming delay


@router.get("/stream_long_json")
async def stream_long_json():
    """Streams long text in JSON format."""
    return StreamingResponse(long_json_stream(), media_type="application/json")


########################################################################


async def long_text_stream():
    """Simulates a long text response, streamed in JSON format."""

    # Split text into chunks (simulating AI response generation)
    chunks = LONG_TEXT.split(" ")

    current_text = ""
    for word in chunks:
        current_text += word + " "
        # logging.info(current_text)
        loguru.logger.info(current_text)
        yield current_text.strip() + "\n"
        sleep_time = random.randint(1, 5) / 10
        await asyncio.sleep(sleep_time)  # Simulate streaming delay


@router.get("/stream_long_text")
async def stream_long_json():
    """Streams long text in JSON format."""
    return StreamingResponse(long_text_stream(), media_type="text/plain")


########################################################################


async def long_text_and_json_stream():
    """Simulates a long text response, streamed in JSON format."""

    # Split text into chunks (simulating AI response generation)
    chunks = LONG_TEXT.split(" ")

    current_text = ""
    for word in chunks:
        current_text += word + " "
        # logging.info(current_text)
        loguru.logger.info(current_text)
        yield current_text.strip() + "\n"
        sleep_time = random.randint(1, 5) / 10
        await asyncio.sleep(sleep_time)  # Simulate streaming delay

    record_id = uuid.uuid4()

    json_response = json.dumps({"record_id": str(record_id), "status": "completed", "text": current_text})
    yield json_response


@router.get("/stream_long_text_and_json")
async def stream_long_json():
    """Streams long text in JSON format."""
    return StreamingResponse(long_text_and_json_stream(), media_type="text/plain")


########################################################################
# application/x-ndjson


async def ndjson():
    """Simulates a long text response, streamed in JSON format."""

    # Split text into chunks (simulating AI response generation)
    chunks = LONG_TEXT.split(" ")

    current_text = ""
    for word in chunks:
        current_text += word + " "
        # logging.info(current_text)
        loguru.logger.info(current_text)
        yield json.dumps({"content": current_text.strip()}) + "\n"
        sleep_time = random.randint(1, 5) / 10
        await asyncio.sleep(sleep_time)  # Simulate streaming delay

    record_id = uuid.uuid4()

    json_response = json.dumps({"record_id": str(record_id), "status": "completed", "text": current_text})
    yield json_response


@router.get("/ndjson")
async def stream_long_json():
    """Streams long text in JSON format."""
    return StreamingResponse(ndjson(), media_type="application/x-ndjson")


########################################################################


async def event_stream():
    """Simulates a long text response, streamed in JSON format."""

    # Split text into chunks (simulating AI response generation)
    chunks = LONG_TEXT.split(" ")

    current_text = ""
    for word in chunks:
        current_text += word + " "
        # logging.info(current_text)
        loguru.logger.info(current_text)
        yield json.dumps({"content": current_text.strip()}) + "\n"
        sleep_time = random.randint(1, 5) / 10
        await asyncio.sleep(sleep_time)  # Simulate streaming delay

    record_id = uuid.uuid4()

    json_response = json.dumps({"record_id": str(record_id), "status": "completed", "text": current_text})
    yield json_response


@router.get("/event_stream")
async def stream_long_json():
    """Streams long text in JSON format."""
    return StreamingResponse(event_stream(), media_type="text/event-stream")


########################################################################


async def event_stream_2():
    """Simulates a long text response, streamed in JSON format."""

    # Split text into chunks (simulating AI response generation)
    chunks = LONG_TEXT.split(" ")

    current_text = ""
    for word in chunks:
        current_text += word + " "
        # logging.info(current_text)
        loguru.logger.info(current_text)
        yield json.dumps({"content": current_text.strip()}) + "\n"
        sleep_time = random.randint(1, 5) / 10
        await asyncio.sleep(sleep_time)  # Simulate streaming delay


@router.get("/event_stream_2")
async def stream_long_json():
    """Streams long text in JSON format."""
    return StreamingResponse(event_stream_2(), media_type="text/event-stream")


# agent = Agent("openai:gpt-4o")
# THIS_DIR = Path(__file__).parent


# async def get_db(request: Request) -> Database:
#     return request.state.db


# class ChatMessage(TypedDict):
#     """Format of messages sent to the browser."""

#     role: Literal["user", "model"]
#     timestamp: str
#     content: str


# def to_chat_message(m: ModelMessage) -> ChatMessage:
#     first_part = m.parts[0]
#     if isinstance(m, ModelRequest):
#         if isinstance(first_part, UserPromptPart):
#             return {
#                 "role": "user",
#                 "timestamp": first_part.timestamp.isoformat(),
#                 "content": first_part.content,
#             }
#     elif isinstance(m, ModelResponse):
#         if isinstance(first_part, TextPart):
#             return {
#                 "role": "model",
#                 "timestamp": m.timestamp.isoformat(),
#                 "content": first_part.content,
#             }
#     raise UnexpectedModelBehavior(f"Unexpected message type for chat app: {m}")


# @router.post("/stream/")
# async def post_chat(prompt: Annotated[str, fastapi.Form()], database: Database = Depends(get_db)) -> StreamingResponse:
#     async def stream_messages():
#         """Streams new line delimited JSON `Message`s to the client."""
#         # stream the user prompt so that can be displayed straight away
#         yield (
#             json.dumps(
#                 {
#                     "role": "user",
#                     "timestamp": datetime.now(tz=timezone.utc).isoformat(),
#                     "content": prompt,
#                 }
#             ).encode("utf-8")
#             + b"\n"
#         )
#         # get the chat history so far to pass as context to the agent
#         messages = await database.get_messages()
#         # run the agent with the user prompt and the chat history
#         async with agent.run_stream(prompt, message_history=messages) as result:
#             async for text in result.stream(debounce_by=0.01):
#                 # text here is a `str` and the frontend wants
#                 # JSON encoded ModelResponse, so we create one
#                 m = ModelResponse(parts=[TextPart(text)], timestamp=result.timestamp())
#                 yield json.dumps(to_chat_message(m)).encode("utf-8") + b"\n"

#         # add new messages (e.g. the user prompt and the agent response in this case) to the database
#         await database.add_messages(result.new_messages_json())

#     return StreamingResponse(stream_messages(), media_type="text/plain")


# P = ParamSpec("P")
# R = TypeVar("R")


# @dataclass
# class Database:
#     """Rudimentary database to store chat messages in SQLite.

#     The SQLite standard library package is synchronous, so we
#     use a thread pool executor to run queries asynchronously.
#     """

#     con: sqlite3.Connection
#     _loop: asyncio.AbstractEventLoop
#     _executor: ThreadPoolExecutor

#     @classmethod
#     @asynccontextmanager
#     async def connect(cls, file: Path = THIS_DIR / ".chat_app_messages.sqlite") -> AsyncIterator[Database]:
#         with logfire.span("connect to DB"):
#             loop = asyncio.get_event_loop()
#             executor = ThreadPoolExecutor(max_workers=1)
#             con = await loop.run_in_executor(executor, cls._connect, file)
#             slf = cls(con, loop, executor)
#         try:
#             yield slf
#         finally:
#             await slf._asyncify(con.close)

#     @staticmethod
#     def _connect(file: Path) -> sqlite3.Connection:
#         con = sqlite3.connect(str(file))
#         cur = con.cursor()
#         cur.execute("CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, message_list TEXT);")
#         con.commit()
#         return con

#     async def add_messages(self, messages: bytes):
#         await self._asyncify(
#             self._execute,
#             "INSERT INTO messages (message_list) VALUES (?);",
#             messages,
#             commit=True,
#         )
#         await self._asyncify(self.con.commit)

#     async def get_messages(self) -> list[ModelMessage]:
#         c = await self._asyncify(self._execute, "SELECT message_list FROM messages order by id")
#         rows = await self._asyncify(c.fetchall)
#         messages: list[ModelMessage] = []
#         for row in rows:
#             messages.extend(ModelMessagesTypeAdapter.validate_json(row[0]))
#         return messages

#     def _execute(self, sql: LiteralString, *args: Any, commit: bool = False) -> sqlite3.Cursor:
#         cur = self.con.cursor()
#         cur.execute(sql, args)
#         if commit:
#             self.con.commit()
#         return cur

#     async def _asyncify(self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> R:
#         return await self._loop.run_in_executor(  # type: ignore
#             self._executor,
#             partial(func, **kwargs),
#             *args,  # type: ignore
#         )
