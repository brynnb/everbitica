from pydantic import UUID4, Field
from pydantic.types import List

from habitica.consts import NotificationType
from habitica.common_model import HabiticaBaseModel


class GroupNotification(HabiticaBaseModel):
    id: UUID4
    name: str


class NotificationData(HabiticaBaseModel):
    header_text: str = Field(default=None)
    body_text: str = Field(default=None)
    group: GroupNotification = Field(default=None)


class Notification(HabiticaBaseModel):
    notification_type: NotificationType = Field(alias="type")
    data: NotificationData
    seen: bool
    id: str


class NotificationsListResponse(HabiticaBaseModel):
    # TODO fix circle imports with class Response

    success: bool
    app_version: str
    notifications: List[Notification] = Field(default_factory=list)
    data: List[Notification]
