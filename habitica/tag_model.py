from pydantic import UUID4
from pydantic.types import List

from habitica.common_model import HabiticaBaseModel, Response


class Tag(HabiticaBaseModel):
    name: str
    id: UUID4


class TagsListResponse(Response):
    data: List[Tag]


class TagResponse(Response):
    data: Tag
