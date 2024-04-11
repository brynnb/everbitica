from typing import Optional

import requests

from habitica.consts import GroupType, KeepChallengesType, KeepType, Privacy
from habitica import error
from habitica.chat import ChatClient
from habitica.common import HabiticaEndpointsProcessor
from habitica.quest import QuestClient
from habitica.common_model import EmptyResponse, Response
from habitica.group_model import (
    GetGroupsResponse,
    GroupInfoDataResponse,
    GroupShortInfoDataResponse,
    InviteResponse,
    GetGroupMembersResponse
)


class GroupClient(HabiticaEndpointsProcessor):
    def __init__(self, user_id, token):
        super(GroupClient, self).__init__(user_id, token)
        self.quest = QuestClient(user_id, token)
        self.chat = ChatClient(user_id, token)

    @staticmethod
    def _map_error(data, schema) -> Response:
        if data["success"] is False:
            e = getattr(error, f"{data['error']}Error")
            raise e(data["message"])
        return schema.parse_obj(data)

    def _invite(self, data: dict, group_id: str = "party") -> Response:
        url = self._build_url(f"groups/{group_id}/invite")
        response = requests.post(url=url, json=data, headers=self._get_auth_headers())
        return self._map_error(response.json(), InviteResponse)

    def invite_by_uuid(self, user_id: str, group_id: str = "party") -> Response:
        data = {"uuids": [user_id]}
        return self._invite(data, group_id)

    def invite_by_email(self, email: str, name: str = "", group_id: str = "party") -> Response:
        data = {"emails": {"email": email, "name": name}}
        return self._invite(data, group_id)

    def reject_invite(self, group_id: str = "party") -> Response:
        url = self._build_url(f"groups/{group_id}/reject-invite")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), EmptyResponse)

    def join(self, group_id: str = "party") -> Response:
        url = self._build_url(f"groups/{group_id}/join")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), GroupInfoDataResponse)

    def leave(
        self,
        group_id: str = "party",
        keep: Optional[KeepType] = None,
        keep_challenges: Optional[KeepChallengesType] = None,
    ) -> Response:
        url = self._build_url(f"groups/{group_id}/leave")
        params, data = {}, {}
        if keep is not None and keep in list(KeepType):
            params = {"keep": keep.value}
        if keep_challenges is not None and keep_challenges in list(KeepChallengesType):
            data = {"keepChallenges": keep_challenges.value}
        response = requests.post(url=url, headers=self._get_auth_headers(), params=params, json=data)
        return self._map_error(response.json(), EmptyResponse)

    def remove_member(self, user_id: str, group_id: str = "party") -> Response:
        url = self._build_url(f"groups/{group_id}/removeMember/{user_id}")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), EmptyResponse)

    def get_info(self, group_id: str = "party"):
        url = self._build_url(f"groups/{group_id}")
        response = requests.get(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), GroupInfoDataResponse)

    def get_groups(self, group_types: str, paginate: bool = None, page: int = None) -> Response:
        url = self._build_url("groups")
        params = {"type": group_types}
        if paginate is not None:
            params["paginate"] = str(paginate)
        if page is not None:
            params["page"] = str(page)
        response = requests.get(url, headers=self._get_auth_headers(), params=params)
        return self._map_error(response.json(), GetGroupsResponse)

    def create(self, name: str, group_type: GroupType, privacy: GroupType) -> Response:
        if group_type not in list(GroupType):
            raise error.BadRequestError("Incorrect group type.")
        if privacy not in list(Privacy):
            raise error.BadRequestError("Incorrect privacy type.")

        url = self._build_url("groups")
        data = {
            "name": name,
            "type": group_type.value,
            "privacy": privacy.value,
        }
        response = requests.post(url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), GroupInfoDataResponse)

    def update(self, data: dict, group_id: str = "party") -> Response:
        url = self._build_url(f"groups/{group_id}")
        response = requests.put(url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), GroupInfoDataResponse)

    def add_manager(self, user_id: str, group_id: str = "party") -> Response:
        url = self._build_url(f"groups/{group_id}/add-manager")
        data = {"managerId": user_id}
        response = requests.post(url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), GroupShortInfoDataResponse)

    def remove_manager(self, user_id: str, group_id: str = "party") -> Response:
        url = self._build_url(f"groups/{group_id}/remove-manager")
        data = {"managerId": user_id}
        response = requests.post(url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), GroupShortInfoDataResponse)

    def get_members(self, group_id: str) -> Response:
        url = self._build_url(f"groups/{group_id}/members")
        response = requests.get(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), GetGroupMembersResponse)