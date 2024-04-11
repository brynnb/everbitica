from typing import Optional

from pydantic import UUID4, Field
from pydantic.types import Dict

from habitica.common_model import HabiticaBaseModel
from habitica.group_model import Response


class ProgressInfo(HabiticaBaseModel):
    collect: Dict
    hp: Optional[float]


class QuestInfo(HabiticaBaseModel):
    progress: ProgressInfo
    active: bool
    members: Dict
    extra: Optional[Dict]
    key: Optional[str] = ""
    quest_leader: UUID4 = Field(default=None, alias="leader")


class QuestResponse(Response):
    data: QuestInfo
