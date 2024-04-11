import requests

from habitica import error
from habitica.common import HabiticaEndpointsProcessor
from habitica.chat_model import CreateMessageResponse
from habitica.common_model import EmptyResponse, Response
from habitica.user_model import GetAchievementsResponse, GetUserInfoResponse


class MemberClient(HabiticaEndpointsProcessor):
    @staticmethod
    def _map_error(data, schema) -> Response:
        if data["success"] is False:
            e = getattr(error, f"{data['error']}Error")
            raise e(data["message"])
        return schema.parse_obj(data)

    def get_member_profile(self, member_id: str):
        url = self._build_url(f"members/{member_id}")
        response = requests.get(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), GetUserInfoResponse)

    def get_member_achievements(self, member_id: str):
        url = self._build_url(f"members/{member_id}/achievements")
        response = requests.get(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), GetAchievementsResponse)

    def send_gem_gift(self, message: str, to_user: str, amount: int):
        url = self._build_url("members/transfer-gems")
        data = {"message": message, "toUserId": to_user, "gemAmount": amount}
        response = requests.post(url=url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), EmptyResponse)

    def send_private_message(self, message: str, to_user: str):
        url = self._build_url("members/send-private-message")
        data = {"message": message, "toUserId": to_user}
        response = requests.post(url=url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), CreateMessageResponse)