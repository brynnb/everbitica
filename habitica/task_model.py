from pydantic import UUID4, Field
from pydantic.datetime_parse import datetime
from pydantic.types import Dict, List

from habitica.consts import AttributeType, PriorityType, TaskType
from habitica.common_model import HabiticaBaseModel
from habitica.group_model import Response


class TaskHistory(HabiticaBaseModel):
    value: float
    date: str  # TODO check format


class Task(HabiticaBaseModel):
    id: UUID4
    secret_id: UUID4 = Field(alias="_id")
    user_id: UUID4
    text: str
    alias: str = Field(default=None)
    type: TaskType
    notes: str
    tags: List
    value: float
    priority: PriorityType = Field(default=None)
    attribute: AttributeType
    reminders: List  # TODO List of reminders
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)
    down: bool = Field(default=None)
    up: bool = Field(default=None)
    challenge: Dict  # TODO Challenge class
    group: Dict  # TODO no ideas what it means yet
    history: List[TaskHistory] = Field(default=None)


class TaskResponse(Response):
    data: Task


class TasksResponse(Response):
    data: List[Task]


class TaskScoreResponse(Response):
    data: Dict


class TaskPositionsResponse(Response):
    data: List
