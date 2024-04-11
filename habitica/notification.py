from typing import List

import requests

from habitica import error
from habitica.common import HabiticaEndpointsProcessor
from habitica.group_model import Response
from habitica.notification_model import NotificationsListResponse


class NotificationClient(HabiticaEndpointsProcessor):
    @staticmethod
    def _map_error(data, schema) -> Response:
        if data["success"] is False:
            e = getattr(error, f"{data['error']}Error")
            raise e(data["message"])
        return schema.parse_obj(data)

    def read_all(self):
        url = self._build_url("notifications/read")
        response = requests.post(url=url, headers=self._get_auth_headers())
        # return self._map_error(response.json(), Response)

    def see_all(self, notification_ids: List[str]):
        url = self._build_url("notifications/see")
        data = {"notificationIds": notification_ids}
        response = requests.post(url=url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), NotificationsListResponse)

    def read(self, notification_id: str):
        url = self._build_url(f"notifications/{notification_id}/read")
        response = requests.post(url=url, headers=self._get_auth_headers())
        # return self._map_error(response.json(), NotificationsListResponse)

    def see(self, notification_id: str):
        url = self._build_url(f"notifications/{notification_id}/see")
        response = requests.post(url=url, headers=self._get_auth_headers())
        # return self._map_error(response.json(), Response)
