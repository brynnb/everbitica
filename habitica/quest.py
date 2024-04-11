import requests

from habitica import error
from habitica.common import HabiticaEndpointsProcessor
from habitica.common_model import Response
from habitica.group_model import GroupInfoDataResponse
from habitica.quest_model import QuestResponse


class QuestClient(HabiticaEndpointsProcessor):
    @staticmethod
    def _map_error(data, schema) -> Response:
        if data["success"] is False:
            e = getattr(error, f"{data['error']}Error")
            raise e(data["message"])
        return schema.parse_obj(data)

    def abort(self, group_id: str = "party"):
        url = self._build_url(f"groups/{group_id}/quests/abort")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), QuestResponse)

    def accept(self, group_id: str = "party"):
        url = self._build_url(f"groups/{group_id}/quests/accept")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), QuestResponse)

    def cancel(self, group_id: str = "party"):
        url = self._build_url(f"groups/{group_id}/quests/cancel")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), QuestResponse)

    def invite(self, quest_key: str, group_id: str = "party"):
        url = self._build_url(f"groups/{group_id}/quests/invite/{quest_key}")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), QuestResponse)

    def leave(self, group_id: str = "party"):
        url = self._build_url(f"groups/{group_id}/quests/leave")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), QuestResponse)

    def reject(self, group_id: str = "party"):
        url = self._build_url(f"groups/{group_id}/quests/reject")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), QuestResponse)

    def force_start(self, group_id: str = "party"):
        url = self._build_url(f"groups/{group_id}/quests/force-start")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), QuestResponse)

    def get_info(self):
        # TODO: Think about data.group.quest.key go to data.quest.key.

        url = self._build_url("groups/party")
        response = requests.get(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), GroupInfoDataResponse)
