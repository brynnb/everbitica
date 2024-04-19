from datetime import datetime
from urllib.parse import urljoin

import requests

from habitica import error
from habitica.challenge import ChallengeClient
from habitica.common import HabiticaEndpointsProcessor
from habitica.group import GroupClient
from habitica.member import MemberClient
from habitica.notification import NotificationClient
from habitica.tag import TagClient
from habitica.task import TaskClient
from habitica.user import UserClient
from habitica.chat import ChatClient
from habitica.common_model import EmptyResponse, InboxResponse, Response


class NotAuthClient:
    base_url = "https://habitica.com/api/v3/"

    def _build_url(self, relative_url: str):
        return urljoin(self.base_url, relative_url)

    def __init__(self):
        self.world_state = None
        self.meta = None

    def get_status(self):
        """Returns 'up' if habitica API is working."""
        url = self._build_url("status")
        response = requests.get(url=url)
        return response.json().get("status")

    def get_content(self, language: str = "en"):
        """Returns all available content objects in selected language."""
        url = self._build_url("content")
        response = requests.get(url=url, params={"language": language})
        return response.json()


class Client(HabiticaEndpointsProcessor):

    def __init__(self, user_id: str, token: str) -> None:
        super(Client, self).__init__(user_id, token)
        self.user = UserClient(user_id, token)
        self.group = GroupClient(user_id, token)
        self.task = TaskClient(user_id, token)
        self.tag = TagClient(user_id, token)
        self.notification = NotificationClient(user_id, token)
        self.challenge = ChallengeClient(user_id, token)
        self.members = MemberClient(user_id, token)
        self.chat = ChatClient(user_id, token)

    @staticmethod
    def _map_error(data: dict, schema) -> Response:
        if data["success"] is False:
            e = getattr(error, f"{data['error']}Error")
            raise e(data["message"])
        return schema.parse_obj(data)

    def export_data(self):
        url = "https://habitica.com/export/userdata.json"
        response = requests.get(url=url, headers=self._get_auth_headers())
        cur_time = datetime.now()
        # TODO - assemble the path to save
        # TODO - save pretty json, not raw
        with open(f"userdata-{cur_time}.json", "w") as f:
            f.write(response.text)

    def run_cron(self) -> Response:
        url = self._build_url("cron")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), EmptyResponse)

    def get_inbox(self, page: int, conversation: str = None):
        url = self._build_url("inbox/messages")
        params = {page: page}
        if conversation is not None:
            params["conversation"] = conversation
        response = requests.get(url=url, headers=self._get_auth_headers(), params=params)
        return self._map_error(response.json(), InboxResponse)
