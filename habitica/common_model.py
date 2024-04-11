from pydantic import BaseModel, Field
from pydantic.datetime_parse import datetime
from pydantic.types import UUID4, Dict, List


def to_lower_camel_case(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


class HabiticaBaseModel(BaseModel):
    class Config:
        alias_generator = to_lower_camel_case


class Response(HabiticaBaseModel):
    from habitica.notification_model import Notification

    success: bool
    app_version: str
    notifications: List[Notification] = Field(default_factory=list)
    message: str = Field(default=None)


class Message(HabiticaBaseModel):
    message: str = Field(default=None)


class ResponseWithMessage(Response):
    data: Message


class EmptyResponse(Response):
    data: Dict


class InboxItem(HabiticaBaseModel):
    sent: bool
    flagCount: int
    secret_id: UUID4 = Field(alias="_id")
    owner_id: UUID4
    flags: Dict
    id: UUID4
    text: str
    unformatted_text: str
    info: Dict
    timestamp: datetime
    likes: Dict
    uuid: UUID4
    contributor: Dict
    backer: Dict
    user: str
    username: str
    user_styles: Dict


class InboxResponse(Response):
    data: List[InboxItem]
