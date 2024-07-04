from typing import Literal
from uuid import uuid4

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field


class BaseStreamingMessage(PydanticBaseModel):
    id: str = Field(default_factory=uuid4)
    message_type: Literal["start", "token", "end", "error"] = Field(frozen=True)


class StreamingStartMessage(BaseStreamingMessage):
    message_type: Literal["start"] = Field(default="start", frozen=True)


class StreamingTokenMessage(BaseStreamingMessage):
    message: str
    message_type: Literal["token"] = Field(default="token", frozen=True)


class StreamingEndMessage(BaseStreamingMessage):
    message_type: Literal["end"] = Field(default="end", frozen=True)


class StreamingErrorMessage(BaseStreamingMessage):
    message: str
    message_type: Literal["error"] = Field(default="error", frozen=True)
