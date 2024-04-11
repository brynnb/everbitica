from pydantic import UUID4, Field
from pydantic.types import Dict, List

from habitica.consts import GroupType, Privacy
from habitica.common_model import HabiticaBaseModel, Response


class LeaderOnly(HabiticaBaseModel):
    challenges: bool
    get_gems: bool


class TasksOrder(HabiticaBaseModel):
    habits: List
    dailys: List
    todos: List
    rewards: List


class Plan(HabiticaBaseModel):
    consecutive: Dict
    #                 "consecutive": {
    #                     "count": 0,
    #                     "offset": 0,
    #                     "gemCapExtra": 0,
    #                     "trinkets": 0
    #                 },
    quantity: int
    extra_months: int
    gems_bought: int
    mystery_items: List


class Purchased(HabiticaBaseModel):
    plan: Plan = Field(default=None)


class Leader(HabiticaBaseModel):
    id: UUID4 = Field(default=None)
    secret_id: UUID4 = Field(alias="_id")
    auth: Dict = Field(default=None)
    # {
    #    "auth": {
    #       "local": {
    #          "username": "second_test_api"
    #       }
    #    },
    flags: Dict = Field(default=None)
    #    "flags": {
    #       "verifiedUsername": true
    #    },
    profile: Dict = Field(default=None)
    #    "profile": {
    #       "name": "second_test_api"
    #    },
    # },


class GroupBaseInfo(HabiticaBaseModel):
    id: UUID4
    secret_id: UUID4 = Field(alias="_id")
    summary: str = Field(default=None)
    privacy: Privacy
    member_count: int = Field(default=0, gt=-1)
    balance: int = Field(default=None, gt=-1)
    group_type: GroupType = Field(alias="type")
    name: str
    categories: List
    leader: UUID4
    managers: Dict = Field(default=None)


class GroupFullInfo(GroupBaseInfo):
    from habitica.quest_model import QuestInfo

    leader_only: LeaderOnly
    quest: QuestInfo
    challenge_count: int
    tasks_order: TasksOrder
    purchased: Purchased
    chat: List
    leader: Leader


class GetGroupsResponse(Response):
    data: List[GroupBaseInfo]


class GroupShortInfoDataResponse(Response):
    data: GroupBaseInfo


class GroupInfoDataResponse(Response):
    data: GroupFullInfo


class Invite(HabiticaBaseModel):
    secret_id: str = Field(alias="_id")  # No idea what this ID is
    id: UUID4
    name: str
    inviter: UUID4


class InviteResponse(Response):
    data: List[Invite]

class GetGroupMembersResponse(Response):
    members: Dict
