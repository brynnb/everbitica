import requests

from habitica import error
from habitica.common import HabiticaEndpointsProcessor
from habitica.chat_model import (
    CreateMessageResponse,
    GetAllMessagesResponse,
    MarkMessageResponse,
)
from habitica.common_model import EmptyResponse
from habitica.group_model import Response


class ChatClient(HabiticaEndpointsProcessor):
    @staticmethod
    def _map_error(data, schema) -> Response:
        if data["success"] is False:
            e = getattr(error, f"{data['error']}Error")
            raise e(data["message"])
        return schema.parse_obj(data)

    def delete_message_from_group(self, group_id: str = "party", chat_id: str = None, previous_msg: str = None):
        url = self._build_url(f"groups/{group_id}/chat/{chat_id}")
        params = {}
        if previous_msg:
            params["previousMsg"] = previous_msg
        response = requests.delete(url=url, headers=self._get_auth_headers(), params=params)
        return self._map_error(response.json(), EmptyResponse)

    def mark_as_spam(self, group_id: str = "party", chat_id: str = None, comment: str = None):
        url = self._build_url(f"groups/{group_id}/chat/{chat_id}/flag")
        data = {}
        if comment:
            data["comment"] = comment
        response = requests.post(url=url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), MarkMessageResponse)

    def get_all(self, group_id: str = "party"):
        url = self._build_url(f"groups/{group_id}/chat")
        response = requests.get(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), GetAllMessagesResponse)

    def like(self, group_id: str = "party", chat_id: str = None):
        url = self._build_url(f"groups/{group_id}/chat/{chat_id}/like")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), MarkMessageResponse)

    def read_all(self, group_id: str = "party"):
        url = self._build_url(f"groups/{group_id}/chat/seen")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), EmptyResponse)

    def create(self, group_id: str = "party", message: str = None, previous_msg: str = None):
        url = self._build_url(f"groups/{group_id}/chat/")
        data = {}
        if message:
            data["message"] = message
        params = {}
        if previous_msg:
            params["previousMsg"] = previous_msg
        response = requests.post(url=url, headers=self._get_auth_headers(), json=data, params=params)
        return self._map_error(response.json(), CreateMessageResponse)