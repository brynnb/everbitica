from typing import Dict, List, Union

from pydantic import UUID4, Field

from habitica.common_model import HabiticaBaseModel, Response
from habitica.user_model import Items, Preferences, Stats


class UserStyle(HabiticaBaseModel):
    items: Items = Field(default=None)
    preferences: Preferences = Field(default=None)
    stats: Stats = Field(default=None)


class Message(HabiticaBaseModel):
    flag_count: int = Field(default=None)
    flags: Dict = Field(default=None)  # TODO: Flag schema
    secret_id: UUID4 = Field(alias="_id")
    id: UUID4
    text: str
    unformattedText: str
    info: Dict = Field(default=None)  # TODO Info schema
    timestamp: str  # TODO past date
    likes: Dict = Field(default=None)  # TODO Likes schema
    client: str = Field(default=None)
    uuid: Union[UUID4, str]
    contributor: Dict = Field(default=None)
    backer: Dict = Field(default=None)
    user: str = Field(default=None)
    username: str = Field(default=None)
    group_id: UUID4 = Field(default=None)
    userStyles: UserStyle = Field(default=None)


class MessageData(HabiticaBaseModel):
    message: Message


class CreateMessageResponse(Response):
    data: MessageData


class GetAllMessagesResponse(Response):
    data: List[Message]


class MarkMessageResponse(Response):
    data: Message
