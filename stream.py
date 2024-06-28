import asyncio
from uuid import UUID

from stream_model import BaseStreamingMessage
from stream_model import StreamingEndMessage


class Stream:
    def __init__(self, ai_message_id: UUID) -> None:
        self._queue = asyncio.Queue[BaseStreamingMessage]()
        self._end = False
        self.ai_message_id = ai_message_id

    def __aiter__(self) -> "Stream":
        return self

    async def __anext__(self):
        if self._end:
            raise StopAsyncIteration
        message = await self._queue.get()
        if isinstance(message, StreamingEndMessage):
            self._end = True
        return {"event": message.message_type, "data": message.model_dump_json()}

    async def asend(self, value) -> None:
        value.id = str(self.ai_message_id)
        await self._queue.put(value)
